---
name: integration-release
description: Integrate validated changes safely through intent-aware conflict resolution, CI gates, current-HEAD review, post-integration checks, human authority, and rollback planning.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Integration and Release

Integration is an engineering step, not merely a Git command.

## Workflow

1. Confirm required implementation, testing, code review, security review, and platform-specific gates are complete for the exact code state being integrated.
2. Verify that any required review verdict is authoritative and bound to the current HEAD. If the code changed after review, treat the prior verdict as stale and require re-review.
3. Reconcile branch drift and merge/rebase conflicts by tracing the intent and primary source of each side. Preserve valid behavior from both; abort/restart is allowed when it is safer than guessing.
4. Re-run affected tests and CI after integration when the project contract requires them.
5. Execute required post-merge/post-integration smoke or acceptance validation; do not treat merge itself as completion when those checks are part of the requested outcome.
6. Identify migrations, configuration changes, feature flags, compatibility windows, and ordering requirements.
7. Define rollback/recovery before irreversible or high-impact changes.
8. Treat production mutation, credential use, destructive operations, and other externally consequential actions as authority checkpoints governed by the host runtime/orchestrator.
9. Record release evidence and known residual risk.

## Learned gate invariants

- `REQUEST CHANGES`, a still-running review, an unreconciled review, failed/unknown CI, or a stale review blocks integration when that gate is required.
- Tests passing do not waive required independent review; review approval does not waive required tests/CI; merge does not waive required post-merge validation.
- If an asynchronous gate is still active, reconcile and await it within policy rather than creating duplicate reviewers/checks or silently proceeding.
- A recovered text fragment saying `APPROVE` is insufficient when the authoritative run/review state is not terminal or does not match current HEAD.
- Preserve the exact evidence chain from reviewed commit -> approved verdict -> CI/test state -> merge -> post-integration verification.

Integration/release decisions are high-responsibility work; prefer a strong reasoning tier when model routing is available.

## Completion gate

Release is complete only when the integrated artifact passes every required gate for the exact released code state, required post-integration validation is terminal, operational ordering is clear, no required asynchronous gate remains merely pending, and the rollback/recovery path matches the risk of the change.
