---
name: engineering-lifecycle
description: Select and coordinate the minimum evidence-gated engineering flow needed to deliver a software objective safely.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Engineering Lifecycle

Use this as the coordinating engineering entry point when the correct path is not already obvious.

## Workflow

1. Classify the objective: decision, research, design, implementation, defect, review, integration, or continuity work.
2. Inspect existing project truth before inventing process. Use `project-discovery` when context is incomplete.
3. Resolve material uncertainty with `technical-research`; use `domain-modeling` when vocabulary or invariants are part of the uncertainty.
4. Require an implementable contract before substantial construction. Use `software-specification` when the acceptance boundary is not already explicit.
5. For work larger than one safe execution unit, use `work-decomposition` to create an acyclic dependency graph and ready frontier.
6. Use `software-architecture` for boundary, interface, data-flow, or structural decisions that materially affect multiple Work Units.
7. Execute with `implementation`, `testing`, and `debugging` as needed; do not force TDD where another verification loop is stronger.
8. Review independently. Use `code-review`; add `security-review` when trust boundaries, sensitive data, authorization, external input, dependencies, or deployment risk make it relevant. Add `web-frontend-design` for web UI/UX, responsive, accessibility, visual-design, or frontend-audit scope. When the target uses WordPress, that skill loads its WordPress adapter rather than becoming a separate lifecycle branch.
9. Use `integration-release` only after the required evidence gates pass.
10. Use `project-handoff` when work crosses an agent/session boundary.

## Lateral engineering flow

Do not turn the lifecycle into a fixed sequential pipeline when real dependencies permit parallel work.

Examples:

- an approved API/interface contract may unlock backend implementation, frontend client/UI work, contract tests, and documentation at the same time;
- independent backend modules may proceed in parallel;
- independent frontend surfaces may proceed in parallel;
- testing, review, research, or security analysis may share a frontier with implementation when they do not require unfinished outputs.

Add a blocking edge only for a real prerequisite. A broad phase label such as “backend” or “frontend” is not by itself a dependency.

When one active worker completes, newly unlocked useful work need not wait for unrelated active workers from the same earlier dispatch. A compatible orchestrator should refill free execution capacity from the recomputed ready frontier while respecting its global concurrency/resource budget.

When parallel results must be reconciled, create an explicit fan-in integration, synthesis, review, or verification Work Unit rather than relying on informal agent-to-agent conversation.

## Orchestrator integration

When Adaptive AI Orchestrator or another compatible orchestrator is available, treat these skills as capabilities selected **per Work Unit**. Let the orchestrator manage:

- project Work Graph and dependency state;
- ready-frontier recomputation;
- logical worker creation and bounded concurrency;
- continuous slot replenishment;
- claims and duplicate-dispatch prevention;
- authority/side-effect policy;
- runtime/session selection;
- context transfer between accepted dependencies;
- fan-out/fan-in coordination;
- result evaluation and bounded replanning.

The lifecycle skill must not duplicate those runtime responsibilities.

Prefer the smallest skill set and smallest useful worker frontier that can produce sufficient evidence. More agents are not automatically better; scale worker count only when independent useful work is ready.

## Learned continuity invariants

Field experience with asynchronous multiagent execution adds these lifecycle rules:

- An intermediate milestone is not terminal completion. Review pending, re-review required, CI pending, merge pending, smoke/acceptance validation pending, an active worker, or required fan-in keeps the objective open.
- `REQUEST CHANGES` starts a remediation -> verification -> independent re-review loop. Do not stop after applying the requested changes or after tests turn green.
- A required review is valid only for the exact code state it inspected. If the reviewed HEAD changes materially, the previous verdict is stale and a fresh review is required.
- If an asynchronous operation appears interrupted, reconcile the existing execution before creating a replacement. Preserve task/run/session identity and avoid duplicate workers or reviewers.
- A wait/transport timeout is not evidence that the delegated work failed. Distinguish runtime/transport uncertainty from semantic failure and let the orchestrator recover or classify it.
- `REPLAN_REQUIRED` is a control-flow signal, not a successful stopping point. Necessary discovered work must return to planning and the ready frontier must be recomputed.
- Testing, review, integration, and post-merge validation are evidence gates. Passing one does not silently waive another.
- Stop only when the requested outcome is complete or a genuine blocker is explicitly classified with enough state for safe resumption.

For high-responsibility lifecycle planning, governance, architecture, or review decisions, prefer the orchestrator's strongest reasoning tier when model routing is available. Routine execution should remain delegated to the least expensive tier that can satisfy the acceptance contract.

## Completion gate

The lifecycle is complete only when the requested outcome is integrated or intentionally stopped with a documented blocker, all required terminal obligations are satisfied or explicitly blocked, required evidence is attached, no recoverable asynchronous work remains unaccounted for, and the next state is unambiguous.
