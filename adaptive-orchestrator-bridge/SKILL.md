---
name: adaptive-orchestrator-bridge
description: Invoke the external Adaptive AI Orchestrator engine through its CLI so OpenClaw chat can delegate governed single-unit or scalable multiagent project work without duplicating orchestration logic.
license: MIT
user-invocable: true
metadata:
  author: oliveiraariel
  version: "1.1.0"
  openclaw:
    primaryEnv: OPENCLAW_GATEWAY_TOKEN
---

# Adaptive Orchestrator Bridge

This skill is a **thin invocation bridge**. It is not the orchestrator and must not reproduce Adaptive planning, policy, claims, frontier, evaluation, concurrency, fan-in, recovery, or replanning logic inside the prompt.

## When to use

Use this bridge when the user explicitly asks to run, use, delegate to, or execute work through the **Adaptive AI Orchestrator**.

Do not use it merely because the Adaptive repository is readable.

Choose the Adaptive entrypoint explicitly according to the work:

- **bounded one-Work-Unit task** → add `--single-unit`;
- **non-trivial project work that can benefit from decomposition, dependencies, multiple specialists, parallel execution, fan-in, recovery, or replanning** → add `--multi-agent` so the helper invokes `adaptive-orchestrator orchestrate`.

The bridge intentionally has **no implicit default execution mode**. If neither flag is supplied it refuses the invocation instead of silently degrading a project request into a fresh one-Work-Unit `run`.

Do not manually simulate a multiagent plan in this skill. In multi-agent mode the Adaptive engine owns the Work Graph, ready frontier, worker count, skill selection, model routing, concurrency, continuous slot replenishment, evaluation, fan-in, recovery, and bounded replanning.

For one user request that is clearly project work, invoke the bridge **exactly once** with `--multi-agent`. Do not split phases such as discovery, implementation, tests, packaging, or handoff into separate top-level bridge invocations; those phases belong inside one Adaptive Work Graph. A handoff-only request is a legitimate `--single-unit` task when it truly asks only for one bounded artifact and no project mutation beyond that artifact.

## Invocation

Invoke the helper at `{baseDir}/scripts/invoke.py` on the host. Pass only the actual delegated work as `--objective`; do not include outer instructions such as “use Adaptive” in the nested objective. Use `--agent main` unless the user or project context identifies another OpenClaw agent/workspace that owns the target project.

### Bounded single-unit example

```bash
python3 "{baseDir}/scripts/invoke.py" \
  --single-unit \
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

## Observability boundary

Once OpenClaw delegates an authorized project scope to Adaptive, it must not continue executing that same delegated scope through direct shell commands, file writes, package/build steps, tests, or other project mutations outside the admitted Adaptive execution. While the delegation is active, the caller may observe, reconcile, surface status, and report the authoritative Adaptive result, but execution of the delegated scope remains inside Adaptive.

If additional project work becomes necessary after the Adaptive result, delegate that work through the appropriate Adaptive path instead of silently continuing it out of band. A deliberately separate action may stay outside Adaptive only when it is genuinely outside the delegated scope and its observability boundary is made explicit. This prevents the Control Room from showing an Adaptive orchestration as terminal while the caller is still performing the same project task invisibly elsewhere.

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

## Worker protocol boundary

The bridge transports work into Adaptive; it does **not** define worker execution semantics.

Adaptive owns the mandatory **Adaptive Worker Protocol**. That protocol is injected before task-specific content and has precedence over roles, skills, task context, and ordinary worker instructions. Skills may add domain know-how, but they must never redefine result transport, completion, recovery, or integrity semantics.

The bridge must preserve this boundary:

- do not prepend a competing worker protocol;
- do not rewrite or strip Adaptive's worker protocol envelope;
- do not teach individual skills to own Result Store transport;
- do not treat chat/history as authoritative output;
- do not translate runtime completion into semantic completion when Adaptive has not reached `RESULT_VERIFIED`;
- do not generate or repair Result Store integrity metadata in the bridge.

Result integrity metadata and the completion manifest are owned by deterministic Adaptive code. Workers own result content; Adaptive owns final publication verification.

Bridge diagnostics should surface the active worker protocol name/version when Adaptive exposes them so runtime identity can be proven before dispatch.

## OpenClaw async process discipline

Adaptive project execution can outlive the foreground wait window of OpenClaw's shell tool. Treat the OpenClaw background-exec session and the Adaptive project checkpoint as two different layers.

Required behavior:

- start the Adaptive bridge invocation only once;
- if OpenClaw backgrounds the command, retain the returned OpenClaw process/session handle and use the supported `process` lifecycle or completion notification;
- when collecting an already-finished background command whose output may be large, prefer `process log`/paginated aggregated output or the compact trailing `BRIDGE_FINAL`; do not assume one late `process poll` contains the complete child transcript;
- **never** emulate waiting with `tail --pid`, `sleep` loops, repeated shell PID probes, or a second equivalent bridge invocation;
- an operating-system PID is process evidence only and is never Adaptive project state;
- the Bridge-allocated `orchestration_id` is the canonical project identity; the SHA-256 checkpoint filename is only a storage key and must never be presented as the orchestration id;
- `BRIDGE_ADMISSION event=durable-admission-materialized` is the Bridge proof that the exact project checkpoint exists;
- `BRIDGE_FINAL` is a compact final transport marker. When it carries `authoritative_project_state=true`, its project fields were re-read through Adaptive `project-status` after the child command ended;
- if any observer/precheck/tool result conflicts with `BRIDGE_FINAL` or a fresh `project-status` query, the authoritative project checkpoint wins;
- after durable project admission, a previous bounded `run` precheck is historical diagnostic evidence only. It cannot classify the later project orchestration as blocked, running, or completed.

When a completion notification is missing, stale, truncated, or ambiguous, invoke:

```text
project-status --orchestration-id <exact-id> --project-root <project-root>
```

before producing any user-visible terminal conclusion. If that status is non-terminal, use the same orchestration's targeted supervisor/resume path. Do not use the global supervisor merely to discover the state of one known orchestration.

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

- **Bridge invocation is not durable Adaptive admission.** The Bridge correlation/admission id and child-process startup are control-plane evidence only. For normal multiagent project execution, durable admission is proven by a new Adaptive project checkpoint; `--plan-only` is the intentional exception.
- **Admission is not project completion.** A successful Bridge admission event, `admission_id`, child-process start, or orchestration identifier proves only that the request crossed the Bridge admission boundary. It does **not** prove that planned workers started, finished, passed review, reached fan-in, or produced a terminal project result.
- **Delegation is an execution boundary.** Once project work is admitted to Adaptive, do not perform the same delegated project work out of band in the parent OpenClaw session; observe/reconcile it or delegate a subsequent Work Unit instead.
- After a multiagent admission succeeds, do not send a user-visible completion/finalization message merely because Bridge invocation returned successfully. Continue observing/reconciling the admitted orchestration until Adaptive returns a project-level terminal result, or explicitly report that the orchestration is still running/incomplete.
- Before saying a multiagent round is complete, verify authoritative project state from Adaptive checkpoint/result data rather than inferring completion from Bridge success, dashboard cosmetics, elapsed time, or the absence of an active foreground command.
- Before saying a durably admitted multiagent round is blocked or failed, perform the same authoritative project-state verification. A stale precheck, dead observer PID, missing OpenClaw background handle, or earlier infrastructure warning cannot override a terminal `COMPLETED` project checkpoint.
- If the caller asks whether workers finished, distinguish at least: admission accepted, workers dispatched/active, Work Units completed/accepted, reviews pending/returned, fan-in pending, and project terminal state.
- Do not translate `RUNNING`, `PARTIAL`, `BLOCKED`, pending review, or recoverable asynchronous state into a friendly but false “completed” response.
- A persisted/dashboard `RUNNING` label is not proof of an active worker. When Adaptive exposes current execution/session/run evidence, prefer that evidence over stale historical UI state and surface any mismatch explicitly.
- If Adaptive returns a recoverable/incomplete state, preserve its orchestration/execution identifiers and state exactly what remains. Do not launch a replacement orchestration from the bridge simply because the caller session is about to end.
- Recovery/reconciliation belongs to Adaptive core/runtime policy. The bridge may surface the state and invoke an explicitly supported recovery path, but must not invent its own competing scheduler or duplicate workers/reviewers.
- When Adaptive reports a circuit-breaker/attempt-budget stop, do not silently redispatch the same work. Surface the stop reason and any human-decision requirement.
- Do not paraphrase worker-reported partial work as completion. If unmet criteria remain, preserve them in the user-visible result.
- Missing implementation/wiring that is already authorized by the delegated Work Unit is not a bridge-level blocker; let Adaptive/worker continue or return the structured incomplete state.
- Distinguish model-quality failures from transport/runtime/tool/environment failures in user-visible summaries when Adaptive provides that classification.
- Do not treat an intermediate gate such as “plan produced”, “tests green”, or “PR merged” as project completion when Adaptive still reports required unfinished work.

## Recovery Loop terminology

For OpenClaw-facing conversation, **Recovery Loop** means the complete **Adaptive Persistent Recovery & Learning Lifecycle** documented by Adaptive core. It is a subsystem/capability coordinated by the Orchestrator, not a separate scheduler and not a Skill that owns dispatch.

A normal task does not require the user to say “use the Recovery Loop”. In ordinary project execution the Orchestrator may activate Recovery Loop behavior proactively when retrabalho, strategy exhaustion, recovery, retest, or learning conditions are detected.

Project-mode Adaptive execution starts a detached per-orchestration supervisor guardian by default. If the launching OpenClaw/tool session disappears after durable admission, that is not a reason to ask the user for a direct fallback or to abandon the objective: the guardian reconciles controller liveness and resumes the same Adaptive orchestration when needed. Completion of one recovery attempt is not closure of the Recovery Loop; closure follows the original objective or a governed terminal stop.

Questions such as “o Recovery Loop foi acionado?”, “em que etapa está o Recovery Loop?”, “o que ele aprendeu?” or “pause/retome o Recovery Loop” refer to the state of that Adaptive lifecycle. The bridge must surface the authoritative Adaptive state and must not emulate a conversational retry loop locally.

## Persistent recovery boundary

When Adaptive enables persistent investigation/recovery, the bridge remains a transport boundary.

- Do not treat an earlier OpenClaw/chat statement that a worker is active as authoritative. Reconcile the current Adaptive checkpoint/Result Store and correlated runtime liveness evidence.
- A launcher PID or controller process is not sufficient proof of an active worker.
- Do not start a replacement recovery from the bridge merely because a Work Unit is `RETURNED`, `RECOVERY_REQUIRED`, or `BLOCKED` by strategy exhaustion. Adaptive core decides whether to invoke the Recovery Strategist, replan, and dispatch.
- After durable project admission, do not ask the user to authorize an out-of-band fallback merely because the caller/controller ended or an intermediate observation is stale. Reconcile the same orchestration first; Adaptive's per-orchestration guardian is the normal persistence path.
- The bridge may invoke Adaptive's supported `project-status`, `resume-project` and `supervise-projects` commands when explicit reconciliation is needed. These commands operate on existing durable state and must never be translated into a fresh replacement orchestration.
- Prefer targeted `project-status` and targeted supervision for a known orchestration id. Do not stop or manipulate unrelated project checkpoints to recover one project.
- When the developer requests pause, preserve the orchestration id and use Adaptive's supported pause/resume path rather than abandoning the execution narrative.
- Learning promotion after a successful retest belongs to Adaptive incident/learning lifecycle; the bridge may report it but must not rewrite Skills or knowledge independently.

## Security rules

- Never print, echo, persist, or place Gateway credentials in a prompt or command argument.
- Token authentication uses `OPENCLAW_GATEWAY_TOKEN`; password authentication uses `OPENCLAW_GATEWAY_PASSWORD`. An unauthenticated local Gateway needs neither.
- Credentials must arrive through OpenClaw's per-skill environment injection or the trusted host environment.
- Do not request provider/model overrides unless the user explicitly requires them and Gateway policy authorizes them.
- Do not edit the Adaptive core to work around a denied execution policy.
- If the helper reports missing prerequisites, report the missing prerequisite rather than silently bypassing the bridge.
