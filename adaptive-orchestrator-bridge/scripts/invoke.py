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
from pathlib import Path


def _python_module_command(root: Path) -> list[str] | None:
    python = root / ".venv" / "bin" / "python"
    if python.is_file():
        return [str(python), "-m", "adaptive_orchestrator"]
    return None


def resolve_command() -> list[str]:
    explicit_root = os.environ.get("ADAPTIVE_ORCHESTRATOR_ROOT")
    if explicit_root:
        command = _python_module_command(Path(explicit_root).expanduser().resolve())
        if command is not None:
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
    try:
        command = resolve_command()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 127

    completed = subprocess.run(
        [*command, "run", *arguments],
        check=False,
        env=os.environ.copy(),
    )
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
