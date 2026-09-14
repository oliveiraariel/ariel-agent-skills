---
name: testing
description: Design and execute risk-based software verification with reproducible evidence, appropriate test layers, and regression protection.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.4.0"
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

## Evidence and failure classification

- Treat a red suite as evidence of a problem, not automatic proof of a production defect. Classify each failure as production code, test/fixture/double, environment/tooling, runtime/transport, or unresolved before changing the implementation.
- When the objective is to add coverage, make the delta auditable. Prefer exact test method names plus before/after test/assertion counts when meaningful. If no count changes because an existing test already covers the obligation, identify that test and the assertion/expectation that proves it.
- A passing subset does not waive missing requested scenarios. Map material acceptance criteria to tests/evidence and keep uncovered items explicit.
- Repair the test environment before drawing conclusions from a runner that cannot start. Prefer project-local tools/dependencies over assuming global `PATH` state.
- When a production defect is confirmed, add the smallest regression test that reproduces the causal behavior rather than merely increasing aggregate test count.

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

## Incident-derived transport verification

For machine-result transport and agent handoff regressions, prefer staged proof:

1. SMALL proves the basic end-to-end contract.
2. MEDIUM targets known representation/transport boundaries.
3. LARGE proves independence from presentation-size limits.
4. Reference fan-in proves a downstream worker can consume the verified authoritative artifact without copying the full payload into conversation context.

Stop escalation when an earlier stage fails and diagnose that boundary first.

Also verify that runtime COMPLETED does not satisfy an authoritative-result gate by itself, that malformed integrity metadata fails closed, that observer loss does not trigger duplicate execution, and that reference fan-in begins only after upstream verification.

When a test exposes a meaningful reusable defect, preserve the incident/evidence reference supplied by the orchestrator. Tests provide validation evidence; they do not themselves promote permanent knowledge.

## Completion gate

Testing is sufficient when material acceptance and regression risks have evidence at an appropriate layer, prior reproduced defects are protected where practical, and remaining gaps are explicit rather than implied away.
