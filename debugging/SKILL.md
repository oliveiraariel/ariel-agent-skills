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

## Incident-derived communication-chain rules

- When a producer appears to finish but the consumer sees missing, truncated, malformed, or summarized output, trace producer -> transport -> persistence -> consumer before retrying the work.
- Distinguish runtime completion from authoritative result verification. A completed runtime with an invalid durable result is first a transport/persistence/integrity problem, not proof of poor model output.
- Treat observer/wait-process failure separately from worker failure. Preserve execution identity and reconcile the same run before redispatch.
- When behavior contradicts checked-out source, prove the effective code identity: repository root, cwd, interpreter, virtual environment, import path, and loaded module file are distinct facts.
- Do not silently coerce machine-contract violations such as integrity numbers encoded as strings. Fix the producer/consumer contract.
- If the orchestrator exposes an incident identifier, preserve it in evidence and remediation. Report new defect evidence upward; do not close or permanently promote the incident from this Skill.

## Completion gate

Debugging is complete when the root cause is evidence-backed, the original reproduction no longer fails for the right reason, recovery/redispatch decisions are justified when relevant, the failure is correctly classified, and a regression check protects the causal behavior.
