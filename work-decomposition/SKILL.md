---
name: work-decomposition
description: Decompose a specification into independently verifiable work units, explicit blocking edges, and safe parallel execution frontiers.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.1"
---

# Work Decomposition

Prefer tracer-bullet Work Units that cross enough layers to produce observable value while remaining reviewable and reversible.

## Workflow

1. Identify decisions and contracts that truly must be resolved before execution work can start.
2. Create Work Units with objective, scope, inputs, expected outputs, acceptance criteria, required capabilities, and any side effects they require.
3. Add blocking edges only where a real prerequisite exists. Optional information flow is not a blocking dependency.
4. Reject cycles in required dependencies.
5. Compute the initial ready frontier and identify units safe to run in parallel.
6. When a shared checkout may be edited concurrently, give every `filesystem.write` Work Unit precise literal repository-relative write scopes. Absolute paths, parent traversal, globs, broad unknown ownership, or overlapping scopes are not safe concurrency seams.
7. Do not serialize by layer name. Backend/backend, frontend/frontend, frontend/backend, testing/review/research, or other combinations may share a frontier when their inputs are ready and write/resource scopes do not conflict.
8. Treat an approved interface/API/schema contract as a potential concurrency seam: once stable enough, it may unlock producers and consumers on multiple layers without waiting for an entire backend or frontend phase to finish.
9. Model dependencies so a scheduler can refill capacity continuously. A Work Unit that depends only on fast producer A should be eligible as soon as A is accepted even if unrelated worker B, dispatched earlier, is still running.
10. Add explicit fan-in Work Units when parallel results require integration, synthesis, cross-layer testing, conflict resolution, or review.
11. Mark human-only or approval-required actions explicitly rather than assigning them to an agent.
12. Keep units large enough to avoid token-expensive micro-fragmentation but small enough that failure or revision does not invalidate unrelated completed work.

## Parallel-safety signals

When the orchestrator supports them, provide or infer:

- `required_capabilities` — what expertise the Work Unit actually needs;
- `requested_side_effects` — read-only versus write/external effects;
- `write_paths` — precise literal path prefixes owned by the Work Unit;
- `parallel_safe` — whether the unit may overlap another active execution;
- priority/criticality — scheduling hints, not fake dependencies.

Do not create a large worker pool merely because concurrency is available. The useful ready frontier should determine worker count. `max_concurrency` is a ceiling, not a target.

## Replanning signal

During execution, newly discovered necessary work should be returned to the orchestrator as a planning fact rather than silently expanding the worker's own scope. The orchestrator decides whether to add a new Work Unit, dependency, or human decision and then recomputes the frontier.

A replanning system must not retroactively attach an unsatisfied mandatory prerequisite to work already executing or accepted unless it first establishes a safe governed recovery/reopen transition.

## Completion gate

The graph is ready when every Work Unit is independently understandable and verifiable, required edges are acyclic, real concurrency seams are visible, write/resource conflicts are bounded, required fan-in points are represented, and the executable frontier is unambiguous at every dependency transition.
