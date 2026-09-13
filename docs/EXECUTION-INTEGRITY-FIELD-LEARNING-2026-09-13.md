# Execution Integrity Field Learning — 2026-09-13

## Why this learning exists

Sustained SGFP work through OpenClaw + Adaptive AI Orchestrator exposed a class of failures that did not come from the business code itself. Workers sometimes stopped after only part of a checklist, stale runtime state looked active, ordinary authorized implementation work was reported as a blocker, test-environment defects were initially indistinguishable from production defects, and historical handoff text contradicted the actual current state.

The useful response is not another generic skill. The lessons belong in the existing skills that already own planning, execution, testing, debugging, bridge behavior, and continuity.

## Cross-skill lessons

### Completion integrity

Runtime termination is not semantic completion. A worker that says work remains, returns a partial checklist, or still has unmet acceptance criteria must not be treated as complete merely because the runtime ended successfully.

Distributed to:
- `engineering-lifecycle`;
- `implementation`;
- `adaptive-orchestrator-bridge`.

### Blocker integrity

A missing repository dependency, transaction seam, wiring change, test, or small architecture adjustment that is already inside the authorized Work Unit is implementation work, not a blocker.

Reserve blockers for real boundaries such as:
- human decision;
- missing authority;
- unavailable environment/runtime;
- external dependency outside the worker's control.

Distributed to:
- `engineering-lifecycle`;
- `implementation`;
- `debugging`;
- `adaptive-orchestrator-bridge`.

### Bounded work lots

Large independent checklists repeatedly produced premature partial stopping. Prefer bounded, closed Work Units/lots with a finishable acceptance surface and explicit fan-in when needed.

Distributed to:
- `work-decomposition`;
- `engineering-lifecycle`.

### Checkable evidence

"Tests added" is weak evidence when the requested test count does not change and no exact existing test can be named. When coverage is part of the objective, report a checkable delta or map the criterion to the exact existing test.

Distributed to:
- `testing`;
- `implementation`.

### Failure classification

Environment/tooling defects, stale fixtures, test-double errors, runtime transport failures, and production defects need separate classifications before code changes are made.

Distributed to:
- `debugging`;
- `testing`;
- `project-discovery` already carries environment-resolution rules.

### Runtime truth

A persisted `RUNNING` dashboard row is not enough to prove active work. Reconcile execution/run/session identifiers and current runtime activity before recovery or redispatch. Repeated uncertain/orphan attempts should reach a bounded circuit breaker rather than create endless equivalent work.

Distributed to:
- `debugging`;
- `adaptive-orchestrator-bridge`;
- `engineering-lifecycle`.

### Handoff authority

A continuity document can preserve history without allowing several contradictory sections to appear current. The handoff must expose one unmistakable current-authority block/pointer with branch, exact HEAD, dirty/WIP state, verified evidence baseline, and exact next action.

Distributed to:
- `project-handoff`.

## Design decision

No new "execution integrity" skill was created. The ecosystem intentionally prefers a compact set of orthogonal skills. These rules are more effective when loaded only by the worker role that needs them, while deterministic terminal-state enforcement remains the responsibility of Adaptive core.
