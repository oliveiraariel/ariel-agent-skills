---
name: testing
description: Design and execute risk-based software verification with reproducible evidence, appropriate test layers, and regression protection.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Testing

Choose the cheapest test layer that can reliably detect the failure being guarded against.

## Workflow

1. Derive test obligations from acceptance criteria, invariants, prior defects, trust boundaries, failure cost, and operational incidents.
2. Use red-green-refactor when a deterministic seam exists and the loop improves design or defect isolation; do not force it for every task.
3. Cover behavior at the appropriate mix of unit, integration, contract, end-to-end, static, and manual verification.
4. Exercise important boundaries: invalid input, empty state, concurrency/retry, permissions, error recovery, migration/compatibility, content extremes, process restart, and persistence/reconstruction when relevant.
5. Make failures reproducible and assertions diagnostic.
6. Record what was actually run and what remains unverified.

## Learned regression obligations

When the affected system is asynchronous, multiagent, event-driven, or stateful, explicitly consider tests for:

- wait timeouts as intermediate states rather than immediate task failure;
- recovery/reconciliation before redispatch and duplicate-worker prevention;
- delayed asynchronous completion and result recovery;
- `REPLAN_REQUIRED` continuing into a valid replanned frontier instead of silently terminating;
- review -> remediation -> re-review loops and stale review invalidation when HEAD changes;
- out-of-order/duplicate events, idempotent reconstruction, and stable correlation identifiers;
- producer/consumer contract compatibility for every public event type;
- refresh, browser reopen, and service restart preserving durable history;
- transient transport failures and reconnection behavior;
- environment resolution such as project-local virtualenv/tool binaries instead of assuming global `PATH`;
- privacy boundaries for observability: prompts, secrets, tokens, and sensitive payloads must not appear in operational event streams unless explicitly designed and authorized.

A bug that consumed meaningful debugging/recovery effort should normally receive the smallest reliable regression test that would have caught it before release.

Routine test construction/execution may use the economical model tier. Remediation of repeatedly failing code/test behavior is a candidate for the code-specialist tier; high-impact test strategy or acceptance analysis may justify a strong reasoning tier under orchestrator policy.

## Completion gate

Testing is sufficient when material acceptance and regression risks have evidence at an appropriate layer, prior reproduced defects are protected where practical, and remaining gaps are explicit rather than implied away.
