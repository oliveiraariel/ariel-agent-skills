#!/usr/bin/env python3
"""Static validation for the Adaptive Orchestrator bridge skill."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
INVOKER = ROOT / "scripts" / "invoke.py"


def main() -> None:
    skill_text = SKILL.read_text(encoding="utf-8")
    if "name: adaptive-orchestrator-bridge" not in skill_text:
        raise SystemExit("bridge SKILL.md has the wrong name")
    if "OPENCLAW_GATEWAY_TOKEN" not in skill_text:
        raise SystemExit("bridge must declare the Gateway token environment contract")
    if "thin invocation bridge" not in skill_text.lower():
        raise SystemExit("bridge must explicitly remain thin")
    if "--multi-agent" not in skill_text or "adaptive-orchestrator orchestrate" not in skill_text:
        raise SystemExit("bridge must document the Adaptive multiagent project mode")

    source = INVOKER.read_text(encoding="utf-8")
    ast.parse(source, filename=str(INVOKER))
    if "shell=True" in source:
        raise SystemExit("bridge invoker must not execute through a shell")
    if "RECURSION_GUARD" not in source or "--constraint" not in source:
        raise SystemExit("bridge invoker must append a recursion-guard constraint")
    if "MULTI_AGENT_FLAG" not in source or '"orchestrate" if multi_agent else "run"' not in source:
        raise SystemExit("bridge invoker must route multiagent work to orchestrate")

    print("OK: adaptive-orchestrator-bridge contract validated")


if __name__ == "__main__":
    main()
