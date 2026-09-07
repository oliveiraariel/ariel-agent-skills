# Ariel Agent Skills

A collection of public AI agent skills created and maintained by Ariel Oliveira.

This repository is dedicated to the development, experimentation, documentation, and continuous improvement of reusable skills for AI agents.

The goal is to create practical, structured, and evolving skills that can be used, adapted, studied, and improved by other developers and AI enthusiasts.

## Skills currently present

| Skill | Description | Status |
|---|---|---|
| [Frontend Design + WordPress](./frontend-design-wordpress/) | Framework-neutral frontend design skill specialized in UI/UX, responsive design, accessibility, and WordPress architecture. | `0.1.0` — reviewed baseline / field testing |

## Planned migration

**Orchestrator** is planned for this collection but is **not currently present in this repository**. It should only be added to the skills table and repository tree after its files are actually migrated here.

## Repository structure

```text
ariel-agent-skills/
├── .github/
│   └── workflows/
│       └── validate-skills.yml
├── README.md
├── LICENSE
└── frontend-design-wordpress/
    ├── SKILL.md
    ├── README.md
    ├── CHANGELOG.md
    ├── references/
    │   ├── accessibility.md
    │   ├── audit-checklist.md
    │   ├── design-quality.md
    │   ├── responsive-design.md
    │   ├── source-analysis.md
    │   └── wordpress-adapter.md
    └── scripts/
        └── validate_skill.py
```

The tree above describes files/directories that actually exist in this repository; planned skills should not be represented as present until they are migrated.

## Validation

Pull requests and pushes that touch skill files run `.github/workflows/validate-skills.yml`. The workflow discovers bundled `scripts/validate_skill.py` validators and executes each with Python 3.

Each skill may also document runtime-specific validation commands in its own README.

## Design philosophy

Skills in this repository should prefer:

- clear activation scope and boundaries;
- progressive disclosure through focused references;
- project-context detection instead of hard-coded stack assumptions;
- verifiable workflows and explicit quality gates;
- portability across compatible agent runtimes where practical;
- documented provenance when external projects materially influence a skill;
- normative standards kept distinct from platform guidance and author heuristics;
- version-sensitive platform features documented with explicit compatibility boundaries.

## Multi-skill repository note

This repository is intended to contain multiple skills over time. Some agent runtimes can scan nested `SKILL.md` files from a configured skill root, while installers may expect a `SKILL.md` at the source directory root. Follow each skill's README for runtime-specific installation guidance.

See each skill's own README and `SKILL.md` for its operating contract.