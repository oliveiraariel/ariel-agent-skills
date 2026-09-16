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
