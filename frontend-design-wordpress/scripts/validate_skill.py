#!/usr/bin/env python3
"""Structural validator for frontend-design-wordpress.

Uses only the Python standard library. It validates project-level invariants plus
key Agent Skills naming/description constraints and the stricter OpenClaw
discovery-description convention adopted by this repository.
"""

from pathlib import Path
import re
import sys

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_DIR / "SKILL.md"

REQUIRED_FILES = [
    "README.md",
    "CHANGELOG.md",
    "references/accessibility.md",
    "references/audit-checklist.md",
    "references/design-quality.md",
    "references/responsive-design.md",
    "references/source-analysis.md",
    "references/wordpress-adapter.md",
]

REQUIRED_FRONTMATTER_KEYS = {"name", "description", "license"}
EXPECTED_NAME = SKILL_DIR.name
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REFERENCE_RE = re.compile(r"`((?:references|scripts)/[A-Za-z0-9._/-]+(?:\.md|\.py))`")
AGENT_SKILLS_NAME_MAX = 64
AGENT_SKILLS_DESCRIPTION_MAX = 1024
OPENCLAW_DESCRIPTION_MAX = 160
PROJECT_SKILL_LINE_MAX = 500


def fail(message):
    print(f"ERROR: {message}")


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    result = {}
    for line in text[4:end].splitlines():
        if not line or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip('"').strip("'")
    return result


def main():
    errors = 0

    if not SKILL_FILE.is_file():
        fail(f"missing {SKILL_FILE}")
        return 1

    text = SKILL_FILE.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)

    if not frontmatter:
        fail("SKILL.md is missing valid YAML-style frontmatter delimiters")
        errors += 1
    else:
        missing = REQUIRED_FRONTMATTER_KEYS - set(frontmatter)
        if missing:
            fail(f"missing frontmatter keys: {', '.join(sorted(missing))}")
            errors += 1

        name = frontmatter.get("name", "")
        description = frontmatter.get("description", "")

        if name != EXPECTED_NAME:
            fail(
                f"frontmatter name must match parent directory {EXPECTED_NAME!r}; "
                f"found {name!r}"
            )
            errors += 1

        if not NAME_RE.fullmatch(name):
            fail("frontmatter name must contain lowercase letters/numbers and single hyphens only")
            errors += 1

        if len(name) > AGENT_SKILLS_NAME_MAX:
            fail(f"frontmatter name exceeds {AGENT_SKILLS_NAME_MAX} characters")
            errors += 1

        if not description:
            fail("frontmatter description must not be empty")
            errors += 1
        elif len(description) > AGENT_SKILLS_DESCRIPTION_MAX:
            fail(
                "frontmatter description exceeds the Agent Skills maximum of "
                f"{AGENT_SKILLS_DESCRIPTION_MAX} characters"
            )
            errors += 1
        elif len(description) > OPENCLAW_DESCRIPTION_MAX:
            fail(
                "frontmatter description exceeds this project's OpenClaw discovery "
                f"limit of {OPENCLAW_DESCRIPTION_MAX} characters"
            )
            errors += 1

    line_count = len(text.splitlines())
    if line_count > PROJECT_SKILL_LINE_MAX:
        fail(
            f"SKILL.md has {line_count} lines; project limit is "
            f"{PROJECT_SKILL_LINE_MAX} for progressive disclosure"
        )
        errors += 1

    for relative in REQUIRED_FILES:
        path = SKILL_DIR / relative
        if not path.is_file():
            fail(f"missing required file: {relative}")
            errors += 1

    referenced_paths = set(REFERENCE_RE.findall(text))
    for relative in sorted(referenced_paths):
        if not (SKILL_DIR / relative).is_file():
            fail(f"SKILL.md references missing file: {relative}")
            errors += 1

    if errors:
        print(f"\nValidation failed with {errors} error(s).")
        return 1

    print("frontend-design-wordpress: structure OK")
    print(f"Name: {frontmatter['name']} ({len(frontmatter['name'])} chars)")
    print(f"Description: {len(frontmatter['description'])} chars")
    print(f"SKILL.md: {line_count} lines")
    print(f"Checked {1 + len(REQUIRED_FILES)} required files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
