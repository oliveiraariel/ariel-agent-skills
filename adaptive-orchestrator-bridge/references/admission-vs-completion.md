# Bridge invocation, durable admission, and project completion are distinct

## Incident

During SGFP Stage 11 on 2026-09-16, OpenClaw received a successful Bridge
admission for a new governed multiagent orchestration. The response was then
phrased as if the round had effectively finished, even though several planned
workers had not yet completed and some had not started.

The incident revealed two separate boundaries:\n\n```text\nBridge invocation / correlation id\n!=\ndurable Adaptive project admission\n!=\nproject execution completed\n```\n\nA Bridge invocation id is control-plane correlation only. For normal multiagent execution, durable Adaptive admission is proven by a new project checkpoint. `--plan-only` is the intentional exception because it does not create a resumable project.\n\nAfter durable admission, the checkpoint proves that the request crossed the project-admission boundary, but it still does not prove completion. It does not prove any of the
following:

- all planned Work Units were dispatched;
- all workers started;
- all workers finished;
- verification passed;
- security/code review passed;
- fan-in executed;
- the project checkpoint is terminal.

## Durable rule for OpenClaw

After successful multiagent admission, the controller must keep the state
classification explicit.

At minimum distinguish:\n\n```text\nBRIDGE INVOCATION STARTED\nDURABLE PROJECT ADMITTED\n
DISPATCHED / ACTIVE
WORK-UNIT COMPLETED
REVIEW PENDING / RETURNED
FAN-IN PENDING
PROJECT TERMINAL
```

Do not collapse these into one generic "done" state.

## Authoritative completion evidence

Before reporting that the governed round is complete, prefer Adaptive's
project-level checkpoint/result state over presentation-layer signals.

Strong evidence includes:

- project checkpoint with terminal state;
- project-level structured result;
- Work Unit states/verdicts;
- review/fan-in state;
- Result Store references where required.

Weak evidence that must not be treated as completion by itself includes:

- Bridge `admission_id` / invocation id by itself;\n- child process started successfully;
- orchestration id was allocated;
- foreground invocation returned;
- dashboard shows no currently running worker;
- elapsed time;
- local shell command finished.

## User-visible behavior

If admission succeeds but the project is still executing, say so explicitly.

Correct:

```text
The orchestration was admitted successfully. It is still running; workers and
downstream review/fan-in have not yet reached a terminal project result.
```

Incorrect:

```text
The round is complete.
```

when only admission has been proven.

## Recovery interaction

If the controller process ends or observation becomes stale, preserve the
orchestration id and use Adaptive's supported reconciliation/resume mechanisms.
Do not infer completion from loss of an observer, and do not launch a duplicate
orchestration merely because the caller session is ending.

## Reusable invariants\n\n```text\nbridge invocation is not durable admission\ndurable admission requires a project checkpoint\nadmission is not completion\n```

The Bridge owns invocation. Adaptive owns project execution and terminal
semantics.


## Incident: false infrastructure blocker after successful project completion

On 2026-09-18, an SGFP Stage 11 Compromissos orchestration exposed a different
failure mode. The Adaptive project itself completed correctly: discovery,
frontend, backend, gates and package Work Units were all accepted, the release
ZIP was produced, the checkpoint was terminal, and observability recorded
`orchestration_completed status=COMPLETED`.

The parent OpenClaw conversation nevertheless reported:

```text
Bloqueado por infraestrutura Adaptive
```

The false conclusion was reconstructed from four interacting mistakes:

1. a previous bounded `run` precheck was still present in conversation/history
   and was treated as if it owned the later project lifecycle;
2. the caller observed a long-running shell command with `tail --pid`, which
   tracks an operating-system process rather than Adaptive project state;
3. the SHA-256 checkpoint filename was used conversationally as if it were the
   real `orchestration_id`;
4. the bridge did not provide a compact authoritative terminal marker after the
   potentially large Adaptive project JSON, so a background-exec observer could
   reason from incomplete/stale output instead of re-reading the checkpoint.

The incident demonstrates another required boundary:

```text
precheck run state
!=
OpenClaw exec/process state
!=
Adaptive project state
```

### Correct finalization protocol

For project mode, the Bridge allocates the exact `orchestration_id` before
Adaptive starts and passes that id into the core. The expected checkpoint path
is therefore known deterministically.

The Bridge emits:

```text
BRIDGE_ADMISSION ... event=durable-admission-materialized ... orchestration_id=<id>
```

when that exact checkpoint appears, and after the Adaptive child exits it
queries Adaptive `project-status` for the same id and emits a compact final
tail marker:

```text
BRIDGE_FINAL {
  authoritative_project_state: true,
  orchestration_id: <id>,
  status: COMPLETED|RUNNING|PAUSED|PARTIAL|BLOCKED|RECOVERY_REQUIRED,
  terminal: true|false,
  ...
}
```

A user-visible final classification must agree with that status or with a fresh
`project-status` query. If an older precheck, observer PID, shell notification,
or conversational statement disagrees, the durable project checkpoint wins.

### Async observer rule

OpenClaw background execution must be followed through its supported background
process/session lifecycle. Do not replace it with shell-level waiting such as
`tail --pid`, `sleep` loops, or repeated PID probes. Those signals can tell
whether a process exists; they cannot prove whether the Adaptive project is
terminal or what its semantic result is.

### Reusable invariants

```text
checkpoint filename hash is not orchestration id
OS process exit is not project result
precheck lifecycle cannot override admitted project lifecycle
terminal user conclusion requires authoritative project re-read
compact final marker must survive large/truncated child output
```
