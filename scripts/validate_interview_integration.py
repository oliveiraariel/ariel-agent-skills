#!/usr/bin/env python3
"""Regression checks for portable documentation-aware interviewing skill integration."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read(rel: str) -> str:
    p = ROOT / rel
    assert p.is_file(), f"missing file: {rel}"
    return p.read_text(encoding="utf-8")

skills = {x["id"]: x for x in json.loads(read("registry/skills.json"))["skills"]}
caps = {x["id"] for x in json.loads(read("registry/capabilities.json"))["capabilities"]}
names = ("grilling", "grill-me", "grill-with-docs")
for name in names:
    entry = skills[name]
    s = read(f"{name}/SKILL.md")
    assert s.startswith("---\n"), f"frontmatter missing: {name}"
    assert re.search(rf"(?m)^name: {re.escape(name)}$", s), f"wrong name: {name}"
    assert re.search(r"(?m)^license: MIT$", s), f"license missing: {name}"
    version = re.search(r'(?m)^  version: "([^"]+)"$', s)
    assert version and version.group(1) == entry["version"], f"registry version mismatch: {name}"
    assert all(c in caps for c in entry["capabilities"]), f"unknown capability: {name}"
    for dep in entry["dependencies"]:
        assert dep in skills and dep != name, f"invalid skill dependency: {name} -> {dep}"
    assert "Call the Skill tool" not in s, f"vendor-specific invocation in {name}"
    assert "mattpocock-skills-fork" not in s, f"hard-coded upstream dependency in {name}"

grilling = read("grilling/SKILL.md")
alias = read("grill-me/SKILL.md")
writer = read("grill-with-docs/SKILL.md")
governance = read("documentation-governance/SKILL.md")
architecture = read("software-architecture/SKILL.md")
patterns = read("software-architecture/references/pattern-decision-guide.md")
catalog = read("documentation-governance/references/artifact-catalog.md")
coverage = read("documentation-governance/references/elicitation-coverage.md")

# Decision-gathering must use applicable documents, human authority and a bounded unblocked frontier.
for phrase in ("frontier", "bounded", "PROPOSED", "APPROVED", "document", "architect", "DEC-ID"):
    assert phrase.lower() in grilling.lower(), f"interview missing required guard: {phrase}"
for phrase in ("grilling", "grill-with-docs", "Do **not** assume"):
    assert phrase in alias, f"alias routing incomplete: {phrase}"
for phrase in ("NOT_PERSISTED", "write authorization", "glossary", "ADR", "baseline", "approval", "verified"):
    assert phrase.lower() in writer.lower(), f"document interview missing rule: {phrase}"
for phrase in ("grilling", "grill-with-docs", "pattern-decision-guide.md"):
    assert phrase in governance, f"governance integration missing: {phrase}"
assert "pattern-decision-guide.md" in architecture, "architecture does not load pattern guide"
for phrase in ("Modular monolith", "Microservices", "Hexagonal", "CQRS", "API-first", "constraints", "trade-offs"):
    assert phrase.lower() in patterns.lower(), f"architecture pattern coverage missing: {phrase}"
assert len(re.findall(r"(?m)^### \d\d —", catalog)) == 6
assert len(re.findall(r"(?m)^\| DOC-\d\d \|", catalog)) == 20
assert "Architect" in coverage or "Architecture" in coverage
assert "documentation-governance" in skills
assert skills["grill-me"]["dependencies"] == ["grilling"]
assert all(x in skills["grill-with-docs"]["dependencies"] for x in ("grilling","documentation-governance","domain-modeling"))

# Cross-skill dependency graph must be acyclic.
visiting, visited = set(), set()
def visit(name: str) -> None:
    if name in visiting:
        raise AssertionError(f"cyclic skill dependency: {name}")
    if name in visited:
        return
    visiting.add(name)
    for child in skills[name].get("dependencies", []):
        visit(child)
    visiting.remove(name)
    visited.add(name)

for name in skills:
    visit(name)
print("OK: portable skills, question coverage, persisted-decision safeguards, architectural guide and dependency DAG")
