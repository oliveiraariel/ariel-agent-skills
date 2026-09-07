---
name: project-discovery
description: Discover project truth, constraints, conventions, unresolved decisions, and authoritative artifacts before planning or editing.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Project Discovery

Inspect before interrogating. Prefer evidence already present in the repository, connected systems, configuration, tests, ADRs, specs, and history.

## Workflow

1. Identify the authoritative entry points and precedence rules.
2. Map stack, architecture, execution model, tests, CI, deployment, coding conventions, and relevant domain language.
3. Separate facts, inferred assumptions, and genuinely unanswered questions.
4. Ask only questions whose answers materially change the plan. Attach a recommended answer and rationale when possible.
5. Reuse or update the project's existing context artifact instead of creating a competing source of truth.
6. Record pointers to large or specialized material rather than copying it into always-loaded context.

## Completion gate

Discovery is complete when another agent could state what exists, what must be preserved, what remains uncertain, and where the authoritative evidence lives without re-exploring the repository.
