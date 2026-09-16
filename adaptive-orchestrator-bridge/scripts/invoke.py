#!/usr/bin/env python3
"""Locate and invoke the real Adaptive AI Orchestrator CLI.

The bridge never handles Gateway credentials directly. They remain in the
inherited process environment supplied by OpenClaw or the trusted host.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import json
from pathlib import Path
from uuid import uuid4


RECURSION_GUARD = (
    "This task is already executing under Adaptive AI Orchestrator control. "
    "Do not invoke adaptive-orchestrator-bridge or recursively start another "
    "Adaptive orchestration run. Execute only the delegated objective."
)
MULTI_AGENT_FLAG = "--multi-agent"
RUNTIME_MODULES = ("adaptive_orchestrator", "jsonschema", "websockets", "cryptography")
DURABLE_ADMISSION_NOT_MATERIALIZED = 125


def _runtime_preflight(command: list[str], environment: dict[str, str]) -> dict[str, object]:
    """Validate the exact interpreter/environment before starting Adaptive."""
    if not command or not Path(command[0]).is_file():
        return {"ok": False, "error": "resolved executable is not a file"}
    probe = (
        "import importlib.util, json, site, sys\n"
        f"modules = {RUNTIME_MODULES!r}\n"
        "found = {name: (spec.origin if (spec := importlib.util.find_spec(name)) else None) for name in modules}\n"
        "print(json.dumps({'executable': sys.executable, 'prefix': sys.prefix, "
        "'base_prefix': sys.base_prefix, 'site_packages': site.getsitepackages(), 'found': found}))\n"
    )
    try:
        result = subprocess.run([command[0], "-c", probe], check=False, capture_output=True, text=True, env=environment)
    except OSError as exc:
        return {"ok": False, "error": f"could not start runtime probe: {exc}"}
    if result.returncode != 0:
        return {"ok": False, "error": "runtime probe failed"}
    try:
        details = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "runtime probe returned invalid diagnostics"}
    missing = [name for name, origin in details.get("found", {}).items() if origin is None]
    details["ok"] = not missing
    details["missing"] = missing
    return details


def _print_preflight_failure(details: dict[str, object]) -> int:
    missing = ", ".join(str(item) for item in details.get("missing", []))
    print(
        "BRIDGE_RUNTIME_PREFLIGHT_FAILED: "
        f"missing dependency: {missing or details.get('error', 'unknown runtime error')}; "
        f"python={details.get('executable', '<unavailable>')}; "
        f"prefix={details.get('prefix', '<unavailable>')}",
        file=sys.stderr,
    )
    return 126


def _python_module_command(root: Path) -> list[str] | None:
    python = root / ".venv" / "bin" / "python"
    if python.is_file():
        return [str(python), "-m", "adaptive_orchestrator"]
    return None

def _resolve_explicit_root(root: Path) -> tuple[list[str], dict[str, str]]:
    source = root / "src" / "adaptive_orchestrator"
    if not source.is_dir():
        raise RuntimeError(f"Explicit Adaptive root has no src/adaptive_orchestrator: {root}")
    interpreter = os.environ.get("ADAPTIVE_ORCHESTRATOR_PYTHON")
    if interpreter:
        candidate = Path(os.path.abspath(os.path.expanduser(interpreter)))
    else:
        candidate = root / ".venv" / "bin" / "python"
    if not candidate.is_file() or not os.access(candidate, os.X_OK):
        raise RuntimeError(
            "Explicit Adaptive root is not executable: set "
            "ADAPTIVE_ORCHESTRATOR_PYTHON to an authorized Python interpreter."
        )
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "src") + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    return [str(candidate), "-m", "adaptive_orchestrator"], env


def resolve_command() -> list[str]:
    explicit_root = os.environ.get("ADAPTIVE_ORCHESTRATOR_ROOT")
    if explicit_root:
        command, _ = _resolve_explicit_root(Path(explicit_root).expanduser().resolve())
        return command

    # Common development layout: both repositories are siblings under one Git
    # working directory. This avoids hard-coding a username or localized home path.
    skill_file = Path(__file__).resolve()
    sibling_root = skill_file.parents[3] / "adaptive-ai-orchestrator"
    command = _python_module_command(sibling_root)
    if command is not None:
        return command

    installed = shutil.which("adaptive-orchestrator")
    if installed:
        return [installed]

    raise RuntimeError(
        "Adaptive AI Orchestrator executable not found. Set "
        "ADAPTIVE_ORCHESTRATOR_ROOT to the repository containing .venv, "
        "or install the adaptive-orchestrator console script in PATH."
    )


def _project_root_from_arguments(arguments: list[str]) -> Path | None:
    """Return an explicit project root without guessing from cwd."""
    for index, argument in enumerate(arguments):
        if argument == "--project-root":
            if index + 1 >= len(arguments):
                return None
            value = arguments[index + 1].strip()
            return Path(value).expanduser().resolve() if value else None
        if argument.startswith("--project-root="):
            value = argument.split("=", 1)[1].strip()
            return Path(value).expanduser().resolve() if value else None
    return None


def _checkpoint_snapshot(project_root: Path | None) -> frozenset[str]:
    if project_root is None:
        return frozenset()
    directory = project_root / ".adaptive" / "orchestrations"
    try:
        return frozenset(
            str(path.resolve())
            for path in directory.glob("*.json")
            if path.is_file()
        )
    except OSError:
        return frozenset()


def _emit_admission_event(
    *,
    event: str,
    admission_id: str,
    attempt: int,
    adaptive_command: str,
    returncode: int | None = None,
    checkpoint_created: bool | None = None,
    durable_admission_verified: bool | None = None,
    error: str | None = None,
) -> None:
    payload: dict[str, object] = {
        "event": event,
        "admission_id": admission_id,
        "attempt": attempt,
        "adaptive_command": adaptive_command,
    }
    if returncode is not None:
        payload["returncode"] = returncode
    if checkpoint_created is not None:
        payload["checkpoint_created"] = checkpoint_created
    if durable_admission_verified is not None:
        payload["durable_admission_verified"] = durable_admission_verified
    if error:
        # Error text can include an OS path but must never include the inherited
        # environment or command-line payload, where credentials could exist.
        payload["error"] = error
    print(
        "BRIDGE_ADMISSION " + json.dumps(payload, sort_keys=True),
        file=sys.stderr,
        flush=True,
    )


def _run_adaptive_with_admission_retry(
    *,
    command: list[str],
    adaptive_command: str,
    guarded_arguments: list[str],
    environment: dict[str, str],
) -> int:
    """Run Adaptive and retry exactly once only before durable admission.

    For normal project orchestration with an explicit project root, a new
    project checkpoint is the durable evidence that Adaptive crossed its
    admission boundary. Bridge correlation metadata and child-process startup
    are not admission proof.

    Plan-only mode is intentionally exempt because it does not materialize a
    resumable project checkpoint.
    """
    bridge_invocation_id = uuid4().hex
    project_root = _project_root_from_arguments(guarded_arguments)
    plan_only = "--plan-only" in guarded_arguments
    requires_durable_checkpoint = (
        adaptive_command == "orchestrate"
        and project_root is not None
        and not plan_only
    )
    max_attempts = 2 if adaptive_command == "orchestrate" else 1

    for attempt in range(1, max_attempts + 1):
        before = _checkpoint_snapshot(project_root)
        _emit_admission_event(
            event="invocation-start",
            admission_id=bridge_invocation_id,
            attempt=attempt,
            adaptive_command=adaptive_command,
            durable_admission_verified=False if requires_durable_checkpoint else None,
        )
        try:
            completed = subprocess.run(
                [*command, adaptive_command, *guarded_arguments],
                check=False,
                env=environment,
            )
        except OSError as exc:
            _emit_admission_event(
                event="launch-error",
                admission_id=bridge_invocation_id,
                attempt=attempt,
                adaptive_command=adaptive_command,
                checkpoint_created=False,
                durable_admission_verified=False if requires_durable_checkpoint else None,
                error=str(exc),
            )
            if attempt < max_attempts:
                continue
            return 127

        after = _checkpoint_snapshot(project_root)
        checkpoint_created = bool(after - before)
        durable_admission_verified = (
            checkpoint_created if requires_durable_checkpoint else None
        )
        _emit_admission_event(
            event=(
                "exit-with-durable-admission"
                if durable_admission_verified is True
                else "exit-without-durable-admission"
                if requires_durable_checkpoint
                else "exit"
            ),
            admission_id=bridge_invocation_id,
            attempt=attempt,
            adaptive_command=adaptive_command,
            returncode=completed.returncode,
            checkpoint_created=checkpoint_created,
            durable_admission_verified=durable_admission_verified,
        )

        if requires_durable_checkpoint and not checkpoint_created:
            if attempt < max_attempts:
                _emit_admission_event(
                    event="retrying-pre-admission-failure",
                    admission_id=bridge_invocation_id,
                    attempt=attempt,
                    adaptive_command=adaptive_command,
                    returncode=completed.returncode,
                    checkpoint_created=False,
                    durable_admission_verified=False,
                )
                continue
            if completed.returncode == 0:
                _emit_admission_event(
                    event="durable-admission-not-materialized",
                    admission_id=bridge_invocation_id,
                    attempt=attempt,
                    adaptive_command=adaptive_command,
                    returncode=DURABLE_ADMISSION_NOT_MATERIALIZED,
                    checkpoint_created=False,
                    durable_admission_verified=False,
                    error="Adaptive exited successfully but created no durable project checkpoint.",
                )
                return DURABLE_ADMISSION_NOT_MATERIALIZED
            return completed.returncode

        if completed.returncode == 0:
            return 0

        # Once any new checkpoint exists, never retry automatically: the same
        # orchestration may already have durable state that must be resumed.
        if checkpoint_created:
            return completed.returncode

        safe_pre_admission_failure = (
            adaptive_command == "orchestrate"
            and project_root is not None
            and not checkpoint_created
        )
        if safe_pre_admission_failure and attempt < max_attempts:
            _emit_admission_event(
                event="retrying-pre-admission-failure",
                admission_id=bridge_invocation_id,
                attempt=attempt,
                adaptive_command=adaptive_command,
                returncode=completed.returncode,
                checkpoint_created=False,
                durable_admission_verified=False,
            )
            continue
        return completed.returncode

    return 127


def main(argv: list[str] | None = None) -> int:
    arguments = list(sys.argv[1:] if argv is None else argv)
    diagnose = "--diagnose" in arguments
    arguments = [item for item in arguments if item != "--diagnose"]
    try:
        explicit_root = os.environ.get("ADAPTIVE_ORCHESTRATOR_ROOT")
        if explicit_root:
            command, environment = _resolve_explicit_root(Path(explicit_root).expanduser().resolve())
        else:
            command = resolve_command()
            environment = os.environ.copy()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 127

    preflight = _runtime_preflight(command, environment)
    if not preflight.get("ok"):
        return _print_preflight_failure(preflight)

    if diagnose:
        probe = subprocess.run(
            [
                command[0],
                "-c",
                (
                    "import adaptive_orchestrator,sys; import websockets,cryptography; "
                    "from application.worker_protocol import PROTOCOL_NAME,PROTOCOL_VERSION; "
                    "print(__import__('json').dumps({"
                    "'adaptive_version':getattr(adaptive_orchestrator,'__version__',None),"
                    "'adaptive_module_path':adaptive_orchestrator.__file__,"
                    "'python_prefix':sys.prefix,"
                    "'python_base_prefix':sys.base_prefix,"
                    "'venv_active':sys.prefix != sys.base_prefix,"
                    "'gateway_dependencies_available':True,"
                    "'worker_protocol_name':PROTOCOL_NAME,"
                    "'worker_protocol_version':PROTOCOL_VERSION"
                    "}))"
                ),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
        if probe.returncode != 0:
            print(probe.stderr, file=sys.stderr)
            return probe.returncode
        payload = json.loads(probe.stdout.strip())
        payload.update({"resolved_code_root": str(Path(environment["PYTHONPATH"].split(os.pathsep)[0]).parent), "configured_python": os.environ.get("ADAPTIVE_ORCHESTRATOR_PYTHON"), "invoked_python": command[0], "runtime_preflight": preflight})
        print(json.dumps(payload, sort_keys=True))
        return 0

    multi_agent = MULTI_AGENT_FLAG in arguments
    arguments = [argument for argument in arguments if argument != MULTI_AGENT_FLAG]
    explicit_command = arguments[0] if arguments and arguments[0] in {"dispatch", "wait"} else None
    adaptive_command = "orchestrate" if multi_agent else "run"
    if explicit_command and not multi_agent:
        adaptive_command = explicit_command
    if explicit_command:
        arguments = arguments[1:]

    # Every delegated OpenClaw worker can see this bridge skill too. Always add a
    # runtime constraint so a nested task cannot recursively re-enter Adaptive.
    guarded_arguments = list(arguments)
    if adaptive_command != "wait":
        guarded_arguments.extend(("--constraint", RECURSION_GUARD))

    return _run_adaptive_with_admission_retry(
        command=command,
        adaptive_command=adaptive_command,
        guarded_arguments=guarded_arguments,
        environment=environment,
    )


if __name__ == "__main__":
    raise SystemExit(main())
