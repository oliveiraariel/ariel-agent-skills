#!/usr/bin/env python3
"""Validate the canonical documentation catalog and its governing skill."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "documentation-governance"
SKILL = BASE / "SKILL.md"
REF = BASE / "references"
catalog = (REF / "artifact-catalog.md").read_text(encoding="utf-8")
skill = SKILL.read_text(encoding="utf-8")
elicitation = (REF / "elicitation-coverage.md").read_text(encoding="utf-8")
contracts = (REF / "artifact-contracts.md").read_text(encoding="utf-8")

rows = re.findall(r"(?m)^\| (DOC-\d{2}) \|", catalog)
expected = [f"DOC-{i:02d}" for i in range(1, 21)]
assert rows == expected, f"catalog must contain ordered 20 unique IDs: {rows!r}"
area_headers = re.findall(r"(?m)^### \d{2} —", catalog)
assert len(area_headers) == 6, f"expected six logical areas, got {len(area_headers)}"
for id_ in expected:
    assert id_ in elicitation or id_ == "DOC-20", f"missing elicitation coverage: {id_}"
for filename in ("artifact-catalog.md", "elicitation-coverage.md", "artifact-contracts.md"):
    assert filename in skill, f"skill does not link its reference: {filename}"
for required in ("AUTHORITY_CONFLICT", "IMPLEMENTATION_GAP", "TEST_GAP", "DOC_STALE"):
    assert required in contracts, f"missing reconciliation category: {required}"
assert "documentation-governance" in skill
print("OK: 6 areas, 20 unique artifact IDs, elicitation coverage, contract and audit categories")
