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


RECURSION_GUARD = (
    "This task is already executing under Adaptive AI Orchestrator control. "
    "Do not invoke adaptive-orchestrator-bridge or recursively start another "
    "Adaptive orchestration run. Execute only the delegated objective."
)
MULTI_AGENT_FLAG = "--multi-agent"


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

    if diagnose:
        probe = subprocess.run([command[0], "-c", "import adaptive_orchestrator,sys; import websockets,cryptography; print(__import__('json').dumps({'adaptive_version':getattr(adaptive_orchestrator,'__version__',None),'adaptive_module_path':adaptive_orchestrator.__file__,'python_prefix':sys.prefix,'python_base_prefix':sys.base_prefix,'venv_active':sys.prefix != sys.base_prefix,'gateway_dependencies_available':True}))"], check=False, capture_output=True, text=True, env=environment)
        if probe.returncode != 0:
            print(probe.stderr, file=sys.stderr)
            return probe.returncode
        payload = json.loads(probe.stdout.strip())
        payload.update({"resolved_code_root": str(Path(environment["PYTHONPATH"].split(os.pathsep)[0]).parent), "configured_python": os.environ.get("ADAPTIVE_ORCHESTRATOR_PYTHON"), "invoked_python": command[0]})
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

    completed = subprocess.run(
        [*command, adaptive_command, *guarded_arguments],
        check=False,
        env=environment,
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
