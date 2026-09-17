#!/usr/bin/env python3
"""Validate the project-handoff canonical naming contract."""

from pathlib import Path

SKILL = Path(__file__).resolve().parents[1] / "SKILL.md"


def require(text: str, fragment: str) -> None:
    if fragment not in text:
        raise SystemExit(f"VALIDATION ERROR: project-handoff missing required contract: {fragment}")


def main() -> None:
    text = SKILL.read_text(encoding="utf-8")
    require(text, "HANDOFF.md")
    require(text, "docs/governanca/handoffs/HANDOFF-YYYY-MM-DD-HHMM-<SCOPE>.md")
    require(text, "Update it in place")
    require(text, "Do not choose the current handoff by sorting dated filenames")
    require(text, "migrate its current authoritative content into the canonical path")
    print("OK: project-handoff canonical naming and legacy migration contract validated")


if __name__ == "__main__":
    main()
