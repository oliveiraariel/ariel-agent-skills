#!/usr/bin/env python3
"""Minimal structural validator for frontend-design-wordpress.

No third-party dependencies are required.
"""

from pathlib import Path
import re
import sys

SKILL_DIR = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_DIR / "SKILL.md"

REQUIRED_REFERENCES = [
    "references/accessibility.md",
    "references/audit-checklist.md",
    "references/design-quality.md",
    "references/responsive-design.md",
    "references/source-analysis.md",
    "references/wordpress-adapter.md",
]

REQUIRED_FRONTMATTER_KEYS = {"name", "description", "license"}
EXPECTED_NAME = "frontend-design-wordpress"


def fail(message: str) -> None:
    print(f"ERROR: {message}")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}

    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line[:1].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip()
    return result


def main() -> int:
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

        if frontmatter.get("name") != EXPECTED_NAME:
            fail(
                f"frontmatter name must be {EXPECTED_NAME!r}; "
                f"found {frontmatter.get('name')!r}"
            )
            errors += 1

        if not frontmatter.get("description"):
            fail("frontmatter description must not be empty")
            errors += 1

    for relative in REQUIRED_REFERENCES:
        path = SKILL_DIR / relative
        if not path.is_file():
            fail(f"missing required reference: {relative}")
            errors += 1

    referenced_paths = set(re.findall(r"`(references/[A-Za-z0-9._/-]+\.md)`", text))
    for relative in sorted(referenced_paths):
        if not (SKILL_DIR / relative).is_file():
            fail(f"SKILL.md references missing file: {relative}")
            errors += 1

    if errors:
        print(f"\nValidation failed with {errors} error(s).")
        return 1

    print("frontend-design-wordpress: structure OK")
    print(f"Checked {1 + len(REQUIRED_REFERENCES)} required Markdown files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
