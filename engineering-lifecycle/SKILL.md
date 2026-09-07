---
name: engineering-lifecycle
description: Select and coordinate the minimum evidence-gated engineering flow needed to deliver a software objective safely.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Engineering Lifecycle

Use this as the coordinating entry point when the correct engineering path is not already obvious.

## Workflow

1. Classify the objective: decision, research, design, implementation, defect, review, integration, or continuity work.
2. Inspect existing project truth before inventing process. Use `project-discovery` when context is incomplete.
3. Resolve material uncertainty with `technical-research`; use `domain-modeling` when vocabulary or invariants are part of the uncertainty.
4. Require an implementable contract before substantial construction. Use `software-specification` when the acceptance boundary is not already explicit.
5. For work larger than one safe execution unit, use `work-decomposition` to create an acyclic dependency graph and ready frontier.
6. Use `software-architecture` for boundary, interface, data-flow, or structural decisions that materially affect multiple work units.
7. Execute with `implementation`, `testing`, and `debugging` as needed; do not force TDD where another verification loop is stronger.
8. Review independently. Use `code-review`; add `security-review` when trust boundaries, sensitive data, authorization, external input, dependencies, or deployment risk make it relevant. Add `frontend-design-wordpress` for UI/UX/WordPress scope.
9. Use `integration-release` only after the required evidence gates pass.
10. Use `project-handoff` when work crosses an agent/session boundary.

## Orchestrator integration

When Adaptive AI Orchestrator or another compatible orchestrator is available, treat these skills as capabilities selected for Work Units. Let the orchestrator manage dependencies, claims, concurrency, authority policy, runtime selection, and evaluation. The lifecycle skill must not duplicate those runtime responsibilities.

## Completion gate

The lifecycle is complete when the requested outcome is integrated or intentionally stopped with a documented blocker, required evidence is attached, and the next state is unambiguous.
