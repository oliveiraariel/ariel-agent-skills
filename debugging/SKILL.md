---
name: debugging
description: Diagnose difficult defects and performance regressions with a reproducible red loop, competing hypotheses, instrumentation, recovery awareness, and regression-safe fixes.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.4.0"
---

# Debugging

Do not start with the fix. Start with a feedback loop that reliably goes red on the defect.

## Loop

1. Reproduce and define the failure precisely.
2. Classify the failure domain before blaming the implementation or model: application/code, model output quality, test, runtime/orchestrator, transport, tool, environment, authentication/authorization, governance, dependency, or unknown infrastructure.
3. If asynchronous work may already exist, reconcile the current task/run/session/execution state before reproducing or redispatching. Do not create a duplicate just to make the symptom easier to observe.
4. Minimize the reproducer without losing the failure.
5. Generate competing hypotheses and rank them by explanatory power and test cost.
6. Instrument or inspect the system to falsify hypotheses.
7. Change the smallest causal surface supported by evidence.
8. Verify the loop turns green for the right reason.
9. Add regression protection at the lowest reliable layer and run adjacent checks.

## Learned recovery rules

- A wait timeout means “no terminal result yet” unless the underlying runtime contract explicitly says otherwise. Inspect/reconcile before treating it as task failure.
- A persisted/dashboard `RUNNING` label is supporting evidence, not proof of an active worker. Prefer current run/session identity, active-run evidence, terminal runtime state, and correlated telemetry when sources disagree.
- If repeated reconciliation/retry attempts exhaust the governed attempt budget without a usable completion, stop automatic redispatch and surface a circuit-breaker state. Do not manufacture an equivalent third/fourth worker merely to make the symptom disappear.
- Transport failures such as WebSocket/HTTP/Gateway disconnects, project-local tool lookup failures, or authentication errors must not be counted as LLM-quality failures.
- Search/history text is supporting evidence. Terminal runtime state and canonical project state remain authoritative when they disagree.
- When a run is recoverable, preserve its identifiers and retrieve the existing result. Redispatch only after irrecoverability is evidenced.
- When the defect reveals a missing contract between components, fix the contract/validation seam rather than teaching one side to silently ignore legitimate events.
- Record the failure class, causal evidence, affected identifiers, remediation, and regression check so later model-routing or reliability analysis can separate model quality from infrastructure noise.

Root-cause analysis may require a strong reasoning tier when the failure is complex or high-impact. Concrete code remediation after diagnosis is a candidate for the code-specialist tier under orchestrator policy.

## Validated investigation lessons

- When conversational/session memory conflicts with correlated operational evidence, prefer execution identity, active-execution state, valid lease, fresh heartbeat, checkpoint/Result Store evidence appropriate to the question. A PID, launcher, or stale `RUNNING` label alone is not proof of useful worker execution.
- For component failures, use a controlled A/B isolation when safe: reproduce with the suspected component active, hold the environment stable, disable only that component, and compare behavior. If the A/B result isolates the component, inspect the platform-native logs immediately before changing code.
- A failed hypothesis is useful evidence. Preserve that it was tested and refuted so later investigation does not repeat the same path without new evidence.
- If ordinary debugging/retry has exhausted materially distinct paths, return the failure history to Adaptive's `investigation` / Recovery Strategist capability rather than inventing another equivalent retry locally.

## Completion gate

Debugging is complete when the root cause is evidence-backed, the original reproduction no longer fails for the right reason, recovery/redispatch decisions are justified when relevant, the failure is correctly classified, and a regression check protects the causal behavior.
