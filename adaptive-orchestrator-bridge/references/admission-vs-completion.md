# Bridge admission is not project completion

## Incident

During SGFP Stage 11 on 2026-09-16, OpenClaw received a successful Bridge
admission for a new governed multiagent orchestration. The response was then
phrased as if the round had effectively finished, even though several planned
workers had not yet completed and some had not started.

The error was conceptual, not transport-level:

```text
Bridge admission accepted
!=
project execution completed
```

A Bridge admission event proves only that the request crossed the invocation
boundary and was accepted for orchestration. It does not prove any of the
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

At minimum distinguish:

```text
ADMITTED
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

- Bridge `admission_id`;
- child process started successfully;
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

## Reusable invariant

```text
admission is not completion
```

The Bridge owns invocation. Adaptive owns project execution and terminal
semantics.
