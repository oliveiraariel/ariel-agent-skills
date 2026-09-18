#!/usr/bin/env python3
"""Locate and invoke the real Adaptive AI Orchestrator CLI.

The bridge never handles Gateway credentials directly. They remain in the
inherited process environment supplied by OpenClaw or the trusted host.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
import threading
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
ORCHESTRATION_ID_ALREADY_ADMITTED = 124


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


def _resolved_code_root(
    *,
    command: list[str],
    environment: dict[str, str],
    preflight: dict[str, object],
) -> str | None:
    found = preflight.get("found")
    if isinstance(found, dict):
        module_path = found.get("adaptive_orchestrator")
        if isinstance(module_path, str) and module_path:
            path = Path(module_path).expanduser().resolve()
            # .../<repo>/src/adaptive_orchestrator/__init__.py -> <repo>
            if len(path.parents) >= 3:
                return str(path.parents[2])

    pythonpath = environment.get("PYTHONPATH")
    if pythonpath:
        first = pythonpath.split(os.pathsep)[0].strip()
        if first:
            return str(Path(first).expanduser().resolve().parent)

    if command:
        executable = Path(command[0]).expanduser().resolve()
        # .../<repo>/.venv/bin/python -> <repo>
        if executable.parent.name == "bin" and executable.parent.parent.name == ".venv":
            return str(executable.parent.parent.parent)

    return None


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


def _argument_value(arguments: list[str], name: str) -> str | None:
    for index, argument in enumerate(arguments):
        if argument == name:
            if index + 1 >= len(arguments):
                return None
            value = arguments[index + 1].strip()
            return value or None
        if argument.startswith(name + "="):
            value = argument.split("=", 1)[1].strip()
            return value or None
    return None


def _checkpoint_path(project_root: Path, orchestration_id: str) -> Path:
    digest = hashlib.sha256(orchestration_id.encode("utf-8")).hexdigest()
    return project_root / ".adaptive" / "orchestrations" / f"{digest}.json"


def _project_status(
    *,
    command: list[str],
    environment: dict[str, str],
    project_root: Path,
    orchestration_id: str,
) -> tuple[dict[str, object] | None, str | None]:
    try:
        completed = subprocess.run(
            [
                *command,
                "project-status",
                "--orchestration-id",
                orchestration_id,
                "--project-root",
                str(project_root),
            ],
            check=False,
            capture_output=True,
            text=True,
            env=environment,
        )
    except OSError as exc:
        return None, f"project-status launch failed: {type(exc).__name__}"
    if completed.returncode != 0:
        return None, f"project-status exited {completed.returncode}"
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None, "project-status returned invalid JSON"
    if not isinstance(payload, dict) or payload.get("orchestration_id") != orchestration_id:
        return None, "project-status identity mismatch"
    return payload, None


def _watch_durable_admission(
    *,
    checkpoint_path: Path,
    stop_event: threading.Event,
    emit,
) -> None:
    while not stop_event.wait(0.1):
        if checkpoint_path.is_file():
            emit()
            return


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
    orchestration_id: str | None = None,
    checkpoint_ref: str | None = None,
) -> None:
    payload: dict[str, object] = {
        "event": event,
        # Kept for compatibility with existing log consumers. It is a Bridge
        # invocation correlation id, not proof of durable project admission.
        "admission_id": admission_id,
        "bridge_invocation_id": admission_id,
        "attempt": attempt,
        "adaptive_command": adaptive_command,
    }
    if orchestration_id:
        payload["orchestration_id"] = orchestration_id
    if checkpoint_ref:
        payload["checkpoint_ref"] = checkpoint_ref
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


def _emit_final_event(
    *,
    bridge_invocation_id: str,
    adaptive_command: str,
    returncode: int,
    orchestration_id: str | None,
    project_status: dict[str, object] | None,
    status_error: str | None = None,
) -> None:
    payload: dict[str, object] = {
        "bridge_invocation_id": bridge_invocation_id,
        "adaptive_command": adaptive_command,
        "returncode": returncode,
    }
    if orchestration_id:
        payload["orchestration_id"] = orchestration_id
    if project_status is not None:
        payload["authoritative_project_state"] = True
        for key in (
            "status",
            "terminal",
            "desired_state",
            "work_unit_count",
            "completed_work_unit_ids",
            "blocked_work_unit_ids",
            "recovery_required_work_unit_ids",
            "unfinished_work_unit_ids",
            "active_execution_count",
            "pending_replan",
            "replan_count",
        ):
            if key in project_status:
                payload[key] = project_status[key]
    else:
        payload["authoritative_project_state"] = False
    if status_error:
        payload["status_error"] = status_error
    print(
        "BRIDGE_FINAL " + json.dumps(payload, ensure_ascii=False, sort_keys=True),
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
    """Run Adaptive with exact project identity and pre-admission-only retry.

    For normal project orchestration the Bridge allocates the orchestration id
    before launching Adaptive. That id names the exact durable checkpoint and
    remains the only project identity used for admission, reconciliation and
    final reporting.
    """
    bridge_invocation_id = uuid4().hex
    project_root = _project_root_from_arguments(guarded_arguments)
    plan_only = "--plan-only" in guarded_arguments
    requires_durable_checkpoint = (
        adaptive_command == "orchestrate"
        and project_root is not None
        and not plan_only
    )

    orchestration_id = _argument_value(guarded_arguments, "--orchestration-id")
    if requires_durable_checkpoint and orchestration_id is None:
        orchestration_id = uuid4().hex
        guarded_arguments = [
            *guarded_arguments,
            "--orchestration-id",
            orchestration_id,
        ]

    checkpoint_path = (
        _checkpoint_path(project_root, orchestration_id)
        if requires_durable_checkpoint
        and project_root is not None
        and orchestration_id is not None
        else None
    )
    if checkpoint_path is not None and checkpoint_path.exists():
        _emit_admission_event(
            event="existing-durable-orchestration",
            admission_id=bridge_invocation_id,
            attempt=0,
            adaptive_command=adaptive_command,
            checkpoint_created=False,
            durable_admission_verified=True,
            orchestration_id=orchestration_id,
            checkpoint_ref=checkpoint_path.name,
            error=(
                "Fresh orchestrate will not reuse an admitted orchestration id; "
                "use project-status/resume-project."
            ),
        )
        status, status_error = _project_status(
            command=command,
            environment=environment,
            project_root=project_root,
            orchestration_id=orchestration_id,
        )
        _emit_final_event(
            bridge_invocation_id=bridge_invocation_id,
            adaptive_command=adaptive_command,
            returncode=ORCHESTRATION_ID_ALREADY_ADMITTED,
            orchestration_id=orchestration_id,
            project_status=status,
            status_error=status_error,
        )
        return ORCHESTRATION_ID_ALREADY_ADMITTED

    max_attempts = 2 if adaptive_command == "orchestrate" else 1

    for attempt in range(1, max_attempts + 1):
        checkpoint_existed_before = bool(
            checkpoint_path is not None and checkpoint_path.exists()
        )
        _emit_admission_event(
            event="invocation-start",
            admission_id=bridge_invocation_id,
            attempt=attempt,
            adaptive_command=adaptive_command,
            durable_admission_verified=False if requires_durable_checkpoint else None,
            orchestration_id=orchestration_id,
            checkpoint_ref=(checkpoint_path.name if checkpoint_path is not None else None),
        )

        stop_event = threading.Event()
        admission_emitted = threading.Event()

        def emit_materialized() -> None:
            if admission_emitted.is_set():
                return
            admission_emitted.set()
            _emit_admission_event(
                event="durable-admission-materialized",
                admission_id=bridge_invocation_id,
                attempt=attempt,
                adaptive_command=adaptive_command,
                checkpoint_created=True,
                durable_admission_verified=True,
                orchestration_id=orchestration_id,
                checkpoint_ref=(
                    checkpoint_path.name if checkpoint_path is not None else None
                ),
            )

        watcher = None
        if checkpoint_path is not None:
            watcher = threading.Thread(
                target=_watch_durable_admission,
                kwargs={
                    "checkpoint_path": checkpoint_path,
                    "stop_event": stop_event,
                    "emit": emit_materialized,
                },
                name=f"adaptive-admission-{orchestration_id}",
                daemon=True,
            )
            watcher.start()

        try:
            completed = subprocess.run(
                [*command, adaptive_command, *guarded_arguments],
                check=False,
                env=environment,
            )
        except OSError as exc:
            stop_event.set()
            if watcher is not None:
                watcher.join(timeout=1.0)
            _emit_admission_event(
                event="launch-error",
                admission_id=bridge_invocation_id,
                attempt=attempt,
                adaptive_command=adaptive_command,
                checkpoint_created=False,
                durable_admission_verified=False if requires_durable_checkpoint else None,
                orchestration_id=orchestration_id,
                checkpoint_ref=(
                    checkpoint_path.name if checkpoint_path is not None else None
                ),
                error=str(exc),
            )
            if attempt < max_attempts:
                continue
            _emit_final_event(
                bridge_invocation_id=bridge_invocation_id,
                adaptive_command=adaptive_command,
                returncode=127,
                orchestration_id=orchestration_id,
                project_status=None,
                status_error="Adaptive child process could not be launched.",
            )
            return 127
        finally:
            stop_event.set()

        if watcher is not None:
            watcher.join(timeout=1.0)

        checkpoint_created = bool(
            checkpoint_path is not None
            and checkpoint_path.exists()
            and not checkpoint_existed_before
        )
        if checkpoint_created and not admission_emitted.is_set():
            emit_materialized()

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
            orchestration_id=orchestration_id,
            checkpoint_ref=(checkpoint_path.name if checkpoint_path is not None else None),
        )

        project_status = None
        status_error = None
        if (
            checkpoint_path is not None
            and checkpoint_path.exists()
            and project_root is not None
            and orchestration_id is not None
        ):
            project_status, status_error = _project_status(
                command=command,
                environment=environment,
                project_root=project_root,
                orchestration_id=orchestration_id,
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
                    orchestration_id=orchestration_id,
                    checkpoint_ref=(
                        checkpoint_path.name if checkpoint_path is not None else None
                    ),
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
                    orchestration_id=orchestration_id,
                    checkpoint_ref=(
                        checkpoint_path.name if checkpoint_path is not None else None
                    ),
                    error=(
                        "Adaptive exited successfully but created no durable "
                        "project checkpoint."
                    ),
                )
                _emit_final_event(
                    bridge_invocation_id=bridge_invocation_id,
                    adaptive_command=adaptive_command,
                    returncode=DURABLE_ADMISSION_NOT_MATERIALIZED,
                    orchestration_id=orchestration_id,
                    project_status=None,
                    status_error="Durable project admission did not materialize.",
                )
                return DURABLE_ADMISSION_NOT_MATERIALIZED
            _emit_final_event(
                bridge_invocation_id=bridge_invocation_id,
                adaptive_command=adaptive_command,
                returncode=completed.returncode,
                orchestration_id=orchestration_id,
                project_status=None,
                status_error="Adaptive exited before durable project admission.",
            )
            return completed.returncode

        _emit_final_event(
            bridge_invocation_id=bridge_invocation_id,
            adaptive_command=adaptive_command,
            returncode=completed.returncode,
            orchestration_id=orchestration_id,
            project_status=project_status,
            status_error=status_error,
        )

        if completed.returncode == 0:
            return 0

        # Once the exact project checkpoint exists, never retry automatically:
        # the same orchestration may already have durable work that must be
        # reconciled/resumed.
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
                orchestration_id=orchestration_id,
                checkpoint_ref=(
                    checkpoint_path.name if checkpoint_path is not None else None
                ),
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
        payload.update(
            {
                "resolved_code_root": _resolved_code_root(
                    command=command,
                    environment=environment,
                    preflight=preflight,
                ),
                "configured_python": os.environ.get("ADAPTIVE_ORCHESTRATOR_PYTHON"),
                "invoked_python": command[0],
                "runtime_preflight": preflight,
            }
        )
        print(json.dumps(payload, sort_keys=True))
        return 0

    multi_agent = MULTI_AGENT_FLAG in arguments
    arguments = [argument for argument in arguments if argument != MULTI_AGENT_FLAG]
    explicit_commands = {
        "dispatch",
        "wait",
        "resume-project",
        "pause-project",
        "project-status",
        "supervise-projects",
    }
    explicit_command = (
        arguments[0]
        if arguments and arguments[0] in explicit_commands
        else None
    )
    adaptive_command = "orchestrate" if multi_agent else "run"
    if explicit_command and not multi_agent:
        adaptive_command = explicit_command
    if explicit_command:
        arguments = arguments[1:]

    # Every delegated OpenClaw worker can see this bridge skill too. Always add a
    # runtime constraint so a nested task cannot recursively re-enter Adaptive.
    guarded_arguments = list(arguments)
    if adaptive_command in {"run", "dispatch", "orchestrate"}:
        guarded_arguments.extend(("--constraint", RECURSION_GUARD))

    return _run_adaptive_with_admission_retry(
        command=command,
        adaptive_command=adaptive_command,
        guarded_arguments=guarded_arguments,
        environment=environment,
    )


if __name__ == "__main__":
    raise SystemExit(main())
