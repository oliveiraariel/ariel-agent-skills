---
name: implementation
description: Implement scoped software work in small vertical slices while preserving architecture, project conventions, and explicit acceptance boundaries.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Implementation

Implement the requested work, not an opportunistic rewrite.

## Workflow

1. Read the Work Unit/spec, relevant architecture, local project instructions, and any structured review/debugging findings that created the work.
2. Identify the smallest vertical slice that can produce observable evidence.
3. Establish a test or feedback seam before risky behavior changes.
4. Implement using the project's existing conventions and dependency choices.
5. Keep unrelated refactors separate unless they are required to make the slice correct.
6. Run the relevant checks after each meaningful slice and before declaring completion.
7. Report changed behavior, evidence, and any acceptance criterion not yet verified.

## Learned operating invariants

- Do not silently absorb newly discovered substantial work. Return it as a planning/replanning fact so ownership, dependencies, model routing, and verification remain explicit.
- When fixing a review or defect finding, change the smallest causal surface supported by evidence and preserve already accepted unrelated behavior.
- Distinguish implementation failure from environment/runtime/tool failure. A missing `PATH` entry, transport error, or unavailable runner is not proof that the code is wrong.
- Do not treat local tests as a substitute for required independent review, CI, integration, or post-merge acceptance validation.
- If the current attempt is a remediation/retry after a failed or returned code/test attempt, preserve the prior evidence so the orchestrator can route/escalate appropriately rather than pretending it is a fresh first pass.
- Prefer clean boundaries, single responsibility, maintainability, and repository conventions; do not satisfy a narrow test by creating hidden coupling or bypassing architecture.

## Completion and blocker discipline

- Finish the delegated acceptance surface before reporting `COMPLETE`. If required items remain, report the result as partial and name the unmet criteria.
- A missing repository, port, transaction manager, wiring change, fixture, or test that is already authorized by the Work Unit is implementation work, not a blocker. Make the smallest architecture-consistent change and continue.
- Use a blocker only for a real boundary the worker cannot resolve inside its authority: human decision, missing authority, unavailable environment/runtime, or an external dependency.
- When a task explicitly asks for coverage, make the evidence checkable: name the exact tests added or reused and report before/after counts when those counts are meaningful. If counts do not change, explain which existing tests satisfy the criterion.
- Under Adaptive control, honor the orchestrator's structured completion footer and never mark a partial result complete just because local checks are green.

Routine construction should normally use the economical model tier when routing is available. Repeatedly failing, returned, or explicitly remedial code work is a candidate for the code-specialist tier; the worker should not override orchestrator policy itself.

## Completion gate

Implementation is done when the requested scope works through its intended interface, relevant checks pass, changed behavior is evidenced, and no known acceptance criterion or required downstream gate is silently represented as already satisfied.
