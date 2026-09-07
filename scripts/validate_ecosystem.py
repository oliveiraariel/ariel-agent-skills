#!/usr/bin/env python3
"""Validate the portable skill ecosystem using only the Python standard library."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_REGISTRY = ROOT / "registry" / "skills.json"
CAPABILITIES_REGISTRY = ROOT / "registry" / "capabilities.json"


def fail(message: str) -> None:
    raise SystemExit(f"VALIDATION ERROR: {message}")


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")


def frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)} must start with YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        fail(f"{path.relative_to(ROOT)} has unclosed YAML frontmatter")
    return parts[1]


def field(fm: str, name: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(name)}:\s*[\"']?([^\n\"']+)", fm)
    return match.group(1).strip() if match else None


def main() -> None:
    skills_doc = load_json(SKILLS_REGISTRY)
    caps_doc = load_json(CAPABILITIES_REGISTRY)

    if skills_doc.get("schema_version") != 1:
        fail("registry/skills.json schema_version must be 1")
    if caps_doc.get("schema_version") != 1:
        fail("registry/capabilities.json schema_version must be 1")

    entries = skills_doc.get("skills")
    if not isinstance(entries, list) or not entries:
        fail("skill registry must contain a non-empty skills list")

    capability_entries = caps_doc.get("capabilities")
    if not isinstance(capability_entries, list) or not capability_entries:
        fail("capability registry must contain a non-empty capabilities list")

    capability_ids = [item.get("id") for item in capability_entries]
    if None in capability_ids or len(capability_ids) != len(set(capability_ids)):
        fail("capability ids must be present and unique")
    capability_set = set(capability_ids)

    registry_ids = [entry.get("id") for entry in entries]
    if None in registry_ids or len(registry_ids) != len(set(registry_ids)):
        fail("skill ids must be present and unique")

    discovered = {
        path.parent.name: path
        for path in ROOT.glob("*/SKILL.md")
        if not path.parent.name.startswith(".")
    }

    if set(registry_ids) != set(discovered):
        missing = sorted(set(discovered) - set(registry_ids))
        stale = sorted(set(registry_ids) - set(discovered))
        fail(f"registry/tree mismatch; missing={missing}, stale={stale}")

    used_capabilities: set[str] = set()

    for entry in entries:
        skill_id = entry["id"]
        path = discovered[skill_id]
        fm = frontmatter(path)

        if field(fm, "name") != skill_id:
            fail(f"{path.relative_to(ROOT)} frontmatter name must equal directory name")
        if not field(fm, "description") or len(field(fm, "description") or "") < 20:
            fail(f"{path.relative_to(ROOT)} needs a meaningful description")
        if not field(fm, "license"):
            fail(f"{path.relative_to(ROOT)} must declare a license")
        if not field(fm, "version"):
            fail(f"{path.relative_to(ROOT)} metadata must declare version")

        purpose = entry.get("purpose")
        capabilities = entry.get("capabilities")
        version = entry.get("version")
        if not isinstance(purpose, str) or not purpose.strip():
            fail(f"registry entry {skill_id} needs purpose")
        if not isinstance(capabilities, list) or not capabilities:
            fail(f"registry entry {skill_id} needs capabilities")
        if not isinstance(version, str) or not version.strip():
            fail(f"registry entry {skill_id} needs version")

        unknown = set(capabilities) - capability_set
        if unknown:
            fail(f"registry entry {skill_id} uses unknown capabilities: {sorted(unknown)}")
        used_capabilities.update(capabilities)

        for tuple_field in (
            "inputs",
            "outputs",
            "dependencies",
            "compatible_agents",
            "compatible_models",
            "compatible_runtimes",
            "evidence",
        ):
            if not isinstance(entry.get(tuple_field, []), list):
                fail(f"registry entry {skill_id}.{tuple_field} must be a list")

    unused = capability_set - used_capabilities
    if unused:
        fail(f"capability registry contains unused capabilities: {sorted(unused)}")

    print(
        f"OK: {len(entries)} skills, {len(capability_set)} capabilities, "
        "registry and frontmatter contracts validated"
    )


if __name__ == "__main__":
    main()
