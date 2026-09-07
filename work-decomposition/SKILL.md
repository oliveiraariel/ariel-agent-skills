---
name: work-decomposition
description: Decompose a specification into independently verifiable work units, explicit blocking edges, and safe parallel execution frontiers.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Work Decomposition

Prefer tracer-bullet work units that cross enough layers to produce observable value while remaining reviewable and reversible.

## Workflow

1. Identify decisions that must be resolved before execution work can start.
2. Create work units with objective, scope, inputs, expected outputs, acceptance criteria, and required capabilities.
3. Add blocking edges only where a real prerequisite exists. Optional information flow is not a blocking dependency.
4. Reject cycles in required dependencies.
5. Compute the initial ready frontier and identify units safe to run in parallel.
6. Mark human-only or approval-required actions explicitly rather than assigning them to an agent.
7. Keep units small enough that failure or revision does not invalidate unrelated completed work.

## Completion gate

The graph is ready when every work unit is independently understandable and verifiable, required edges are acyclic, and the first executable frontier is unambiguous.
