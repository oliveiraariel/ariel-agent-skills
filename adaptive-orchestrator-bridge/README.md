# Adaptive Orchestrator Bridge

Thin OpenClaw-facing bridge for invoking the external `adaptive-ai-orchestrator` engine.

## What it is

This skill does not implement orchestration logic. It delegates to the Adaptive CLI and returns its structured result.

For a continuity-sensitive development task that has one Work Unit or one
executor, invoke the bridge with `--durable-single-worker` and an explicit
`--project-root`. The helper delegates to `orchestrate --max-concurrency 1`,
so checkpointing, supervision, recovery, and resume remain available. Use
`--single-unit` only for genuinely bounded work that does not require those
durable mechanisms.

## Resolution order

`adaptive-orchestrator-bridge/scripts/invoke.py` resolves the engine in this order:

1. `ADAPTIVE_ORCHESTRATOR_ROOT/.venv/bin/python -m adaptive_orchestrator`;
2. a sibling `adaptive-ai-orchestrator` repository with `.venv/bin/python`;
3. an installed `adaptive-orchestrator` executable on `PATH`.

This allows portable installations while supporting the common development layout where `ariel-agent-skills` and `adaptive-ai-orchestrator` are sibling repositories.

## Admission versus completion

A Bridge invocation/correlation id means only that the Bridge started an attempt. For normal multiagent execution, durable Adaptive admission is proven only when a new project checkpoint is materialized (`--plan-only` is exempt).\n\nOnce durable admission is proven, it still does **not** mean the project is complete.\n
OpenClaw should not report a governed round as finished until Adaptive exposes
authoritative project-level terminal state. In particular, an `admission_id`,
allocated orchestration id, successful child-process start, or absence of a
currently active worker is not sufficient completion evidence.

See `references/admission-vs-completion.md` for the durable learned invariant
and incident rationale.

## Gateway credentials

The bridge remains eligible across token, password, and unauthenticated Gateway modes. For token authentication, `OPENCLAW_GATEWAY_TOKEN` is the primary environment variable and can be injected through OpenClaw's per-skill `apiKey` / SecretRef mechanism. Password authentication uses `OPENCLAW_GATEWAY_PASSWORD`.

Do not put Gateway credentials in `SKILL.md`, prompts, shell arguments, or repository files.

## Example host invocation

```bash
python3 adaptive-orchestrator-bridge/scripts/invoke.py \
  --single-unit \
  --objective "Respond exactly with BRIDGE_OK." \
  --agent main \
  --accept BRIDGE_OK
```

The command forwards to the Adaptive CLI and returns the same exit status and JSON output.

## Terminal delivery contract

`BRIDGE_FINAL` is the only compact completion marker emitted by this process. It
is emitted after the child command ends and after the Bridge re-reads
`project-status`; it is not a chat message and it is not proof that a detached
OpenClaw conversation has received a reply.

At durable admission, an OpenClaw invocation supplies the trusted source
session through `OPENCLAW_SESSION_KEY` (and may supply an audit-only
`OPENCLAW_CONVERSATION_REF`). The Bridge persists an association under
`.adaptive/openclaw-terminal-observers/<orchestration-id>.json` and registers an
idempotent Gateway cron declaration keyed by that orchestration. The declaration
uses bounded `project-status` triggers, `once=true`, the exact source session,
and `delivery.mode=announce`; it never resumes or dispatches Adaptive work.
The Gateway therefore owns retry, history commit, and deduplication after the
originating turn ends. If source-session context is unavailable, the association
is explicitly recorded as `UNBOUND` and no delivery is claimed.

The OpenClaw-facing skill obtains the current session key through the native
`session_status` operation and injects it into the Bridge-owned
`--openclaw-session-key` option. This is internal integration context; the user
does not provide it. The Bridge strips the option before invoking Adaptive.

Recovery rule: if a completion announcement is missing, read the retained
`BRIDGE_FINAL`/process log and run targeted `project-status` for the exact
orchestration ID. Do not re-run the Bridge or redispatch Work Units. A terminal
checkpoint is sufficient to recover the result, while a non-terminal checkpoint
must go through the existing targeted supervisor path.
