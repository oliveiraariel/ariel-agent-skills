---
name: software-architecture
description: Design software boundaries, interfaces, seams, data flow, and trade-offs that fit the existing project rather than a preferred stack.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Software Architecture

Prefer deep modules: small stable interfaces hiding meaningful implementation complexity. Architecture should reduce coordination cost, not maximize layers.

## Workflow

1. Start from the specification, domain invariants, and existing architecture.
2. Identify responsibilities, boundaries, dependency direction, state ownership, integration points, and trust boundaries.
3. Define seams that are testable through public interfaces.
4. Compare realistic alternatives and record the trade-off that selects one.
5. Preserve established architecture unless evidence shows it blocks the requirement; avoid rewrite reflexes.
6. Record material decisions in the project's existing ADR/architecture mechanism.

## Completion gate

Architecture is ready when implementers know the owning module, public contracts, dependency direction, state/data flow, test seams, and the risks accepted by the decision.
