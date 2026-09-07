# Ariel Agent Skills

A collection of public AI agent skills created and maintained by Ariel Oliveira.

This repository is dedicated to the development, experimentation, documentation, and continuous improvement of reusable skills for AI agents.

The goal is to create practical, structured, and evolving skills that can be used, adapted, studied, and improved by other developers and AI enthusiasts.

## Skills

| Skill | Description | Status |
|---|---|---|
| [Orchestrator](./orchestrator/) | Skill focused on coordinating tasks, workflows, tools, and specialized agents in structured processes. | In development |
| [Frontend Design + WordPress](./frontend-design-wordpress/) | Framework-neutral frontend design skill specialized in UI/UX, responsive design, accessibility, and WordPress architecture. | In development |

More skills may be added as the repository evolves.

## Repository Structure

```text
ariel-agent-skills/
├── README.md
├── LICENSE
│
├── orchestrator/
│   ├── SKILL.md
│   ├── references/
│   ├── scripts/
│   └── assets/
│
├── frontend-design-wordpress/
│   ├── SKILL.md
│   ├── README.md
│   ├── references/
│   │   ├── accessibility.md
│   │   ├── audit-checklist.md
│   │   ├── design-quality.md
│   │   ├── responsive-design.md
│   │   ├── source-analysis.md
│   │   └── wordpress-adapter.md
│   └── scripts/
│       └── validate_skill.py
│
└── future-skills/
```

## Design philosophy

Skills in this repository should prefer:

- clear activation scope and boundaries;
- progressive disclosure through focused references;
- project-context detection instead of hard-coded stack assumptions;
- verifiable workflows and explicit quality gates;
- portability across compatible agent runtimes where practical;
- documented provenance when external projects materially influence a skill.

See each skill's own README and `SKILL.md` for its operating contract.
