---
name: technical-research
description: Resolve technical uncertainty with primary sources, explicit evidence quality, and bounded experiments when documentation alone is insufficient.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Technical Research

Use for questions that materially affect architecture, implementation, compatibility, security, recovery, or tool choice.

## Workflow

1. Write the question and decision it informs.
2. Prefer primary/vendor/specification sources; use secondary discussion to discover edge cases, not as sole authority for critical claims.
3. Track version/date when behavior can change.
4. Distinguish sourced fact, observed runtime state, historical/search evidence, inference, and recommendation.
5. Match authority to the question. Repository HEAD is authoritative for current code, CI/status APIs for check state, and the active runtime/run state for whether asynchronous work has actually finished. Session/search text is evidence, not a substitute for terminal runtime state.
6. If evidence remains ambiguous, build the smallest disposable experiment that can falsify a competing hypothesis. Do not turn the prototype into production by accident.
7. When investigating interrupted asynchronous work, search for the existing task/run/session first and reconcile it before recommending redispatch.
8. Record findings with source pointers, identifiers needed for reproduction/recovery, and remaining uncertainty.

## Learned operating invariants

- A text fragment such as `APPROVE`, `done`, or `completed` is not authoritative if the underlying run is still active or the referenced code HEAD has changed.
- Separate transport, environment, tool, authentication, orchestrator, and model-quality failures. Do not attribute an infrastructure failure to the LLM merely because it happened during an LLM task.
- Prefer bounded experiments that preserve prior state and avoid contaminating persistent operational logs unless the experiment explicitly targets persistence.

Material research that governs architecture, security, recovery, compatibility, or other high-impact decisions should use a strong reasoning tier when model routing is available.

## Completion gate

Research is complete when the decision owner can see the evidence, its authority, freshness and limits, the recommended action, the identifiers or experiment needed to reproduce the finding when applicable, and what would invalidate that recommendation.
