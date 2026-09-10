---
name: project-discovery
description: Discover project truth, constraints, conventions, unresolved decisions, and authoritative artifacts before planning or editing.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Project Discovery

Inspect before interrogating. Prefer evidence already present in the repository, connected systems, configuration, tests, ADRs, specs, and history.

## Workflow

1. Identify the authoritative entry points and precedence rules.
2. Confirm the actual repository/workspace root, current branch/ref, working-tree state, project owner/agent, and the runtime context that subsequent workers must inherit.
3. Map stack, architecture, execution model, tests, CI, deployment, coding conventions, and relevant domain language.
4. Detect environment entry points before execution: virtual environments, package managers, project-local tool binaries, runtime versions, and expected commands. Do not classify a missing global `PATH` entry as an application defect when a project-local executable exists.
5. Separate facts, inferred assumptions, and genuinely unanswered questions.
6. Distinguish authoritative live state from secondary evidence. Search/history text may help locate a run or decision, but runtime state, repository HEAD, CI state, and canonical project artifacts remain authoritative for their domains.
7. Ask only questions whose answers materially change the plan. Attach a recommended answer and rationale when possible.
8. Reuse or update the project's existing context artifact instead of creating a competing source of truth.
9. Record pointers to large or specialized material rather than copying it into always-loaded context.

## Learned operating invariants

- Never let a generic runtime workspace silently replace the repository selected for the objective. If the effective `cwd` differs from project truth, resolve it before planning or editing.
- Preserve unrelated local changes and generated runtime files unless the user or project governance explicitly includes them in scope.
- When recovering interrupted work, identify the existing orchestration/task/execution/session identifiers before deciding whether anything must be re-run.
- Treat environment/tooling failures separately from model-quality failures so later learning and routing statistics remain meaningful.

For material discovery that determines architecture, governance, recovery, or other high-impact decisions, prefer a strong reasoning tier when model routing is available. Bounded inventory work may use a cheaper tier.

## Completion gate

Discovery is complete when another agent could state what exists, what repository/runtime context owns the work, what must be preserved, what remains uncertain, and where the authoritative evidence lives without re-exploring the project.
