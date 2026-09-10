---
name: adaptive-orchestrator-bridge
description: Invoke the external Adaptive AI Orchestrator engine through its CLI so OpenClaw chat can delegate governed single-unit or scalable multiagent project work without duplicating orchestration logic.
license: MIT
user-invocable: true
metadata:
  author: oliveiraariel
  version: "0.3.0"
  openclaw:
    primaryEnv: OPENCLAW_GATEWAY_TOKEN
---

# Adaptive Orchestrator Bridge

This skill is a **thin invocation bridge**. It is not the orchestrator and must not reproduce Adaptive planning, policy, claims, frontier, evaluation, concurrency, fan-in, recovery, or replanning logic inside the prompt.

## When to use

Use this bridge when the user explicitly asks to run, use, delegate to, or execute work through the **Adaptive AI Orchestrator**.

Do not use it merely because the Adaptive repository is readable.

Choose the Adaptive entrypoint according to the work:

- **bounded one-Work-Unit task** → normal bridge invocation;
- **non-trivial project work that can benefit from decomposition, dependencies, multiple specialists, parallel execution, fan-in, recovery, or replanning** → add `--multi-agent` so the helper invokes `adaptive-orchestrator orchestrate`.

Do not manually simulate a multiagent plan in this skill. In multi-agent mode the Adaptive engine owns the Work Graph, ready frontier, worker count, skill selection, model routing, concurrency, continuous slot replenishment, evaluation, fan-in, recovery, and bounded replanning.

## Invocation

Invoke the helper at `{baseDir}/scripts/invoke.py` on the host. Pass only the actual delegated work as `--objective`; do not include outer instructions such as “use Adaptive” in the nested objective. Use `--agent main` unless the user or project context identifies another OpenClaw agent/workspace that owns the target project.

### Bounded single-unit example

```bash
python3 "{baseDir}/scripts/invoke.py" \
  --objective "Analyze this project and return the next safe engineering step." \
  --agent main
```

### Multiagent project example

```bash
python3 "{baseDir}/scripts/invoke.py" \
  --multi-agent \
  --objective "Implement the authorized project objective using the project governance and current repository state." \
  --agent main \
  --max-concurrency 4
```

The helper removes its private `--multi-agent` selector before invoking Adaptive and automatically appends a recursion-guard constraint. Each worker delegated by Adaptive is already under orchestrator control and must not invoke this bridge again.

## Multiagent execution semantics

`--multi-agent` means **dynamic logical worker sessions**, not a permanent pool of newly configured OpenClaw agent profiles.

Adaptive may create multiple independent runtime sessions for ready Work Units and may run 2, 3, 4, 6, or more concurrently up to the configured/policy limit when real dependencies and workspace safety permit. The same configured OpenClaw agent id may own multiple independent worker sessions; role and selected skills specialize each Work Unit.

The bridge must preserve the skill set selected by Adaptive for each Work Unit. Selected skills are capability instructions for the delegated worker; do not replace them with a generic bridge prompt or strip them from the task configuration.

The project scheduler is continuous rather than barrier-based: when one worker completes and its accepted result unlocks new work, Adaptive may use the newly free slot immediately while unrelated workers from earlier dispatches remain active. The bridge must not wait for or reproduce this scheduling logic itself.

The orchestrator may parallelize any safe combination, including:

- backend + backend;
- frontend + frontend;
- backend + frontend;
- testing/review/research alongside other independent work.

It must not parallelize merely to maximize worker count. It should prefer the smallest useful ready frontier and minimum skill context required for the objective.

When workers write to the same checkout, multiagent mode relies on declared literal non-overlapping repository-relative write scopes. Missing, unsafe, unknown or overlapping write scopes are rejected or serialized. This bridge must not claim Git worktree/container isolation unless the active runtime actually provides it.

## Side effects and authority

For a bounded single-unit task, declare required effects with `--side-effect` and add matching `--allow-side-effect` only when the user's request clearly authorizes them.

For multiagent project work, the planner declares side effects per Work Unit. If the user clearly authorized project file edits, pass only the relevant project-level allowance, normally:

```text
--allow-side-effect filesystem.write
```

Do not pass the single-unit `--side-effect` flag to project mode. Do not grant unrelated effects. Never infer authorization for destructive operations, credential changes, publication, deployment, external communication, or scope expansion.

Pass `--accept` only for explicit literal acceptance text in bounded single-unit mode. Project mode derives acceptance criteria per Work Unit and normally represents semantic verification through dedicated testing/review/integration Work Units.

## Result and recovery semantics

### Single-unit mode

Report the structured Adaptive result, especially:

- `runtime_status`;
- `work_unit_state`;
- `verdict`;
- `output`;
- execution identifier when useful.

### Multiagent project mode

Report the project-level result, especially:

- `status`;
- `plan_summary`;
- `work_unit_count`;
- completed, blocked, and unfinished Work Units;
- `max_parallelism_observed`;
- `replan_count`;
- dispatch-generation/frontier summary;
- blockers or human decisions still required.

Do not equate runtime completion with semantic correctness. A project result is strongest when testing/review/integration Work Units also passed.

Learned bridge rules:

- Do not translate `RUNNING`, `PARTIAL`, `BLOCKED`, pending review, or recoverable asynchronous state into a friendly but false “completed” response.
- If Adaptive returns a recoverable/incomplete state, preserve its orchestration/execution identifiers and state exactly what remains. Do not launch a replacement orchestration from the bridge simply because the caller session is about to end.
- Recovery/reconciliation belongs to Adaptive core/runtime policy. The bridge may surface the state and invoke an explicitly supported recovery path, but must not invent its own competing scheduler or duplicate workers/reviewers.
- Distinguish model-quality failures from transport/runtime/tool/environment failures in user-visible summaries when Adaptive provides that classification.
- Do not treat an intermediate gate such as “plan produced”, “tests green”, or “PR merged” as project completion when Adaptive still reports required unfinished work.

## Security rules

- Never print, echo, persist, or place Gateway credentials in a prompt or command argument.
- Token authentication uses `OPENCLAW_GATEWAY_TOKEN`; password authentication uses `OPENCLAW_GATEWAY_PASSWORD`. An unauthenticated local Gateway needs neither.
- Credentials must arrive through OpenClaw's per-skill environment injection or the trusted host environment.
- Do not request provider/model overrides unless the user explicitly requires them and Gateway policy authorizes them.
- Do not edit the Adaptive core to work around a denied execution policy.
- If the helper reports missing prerequisites, report the missing prerequisite rather than silently bypassing the bridge.
