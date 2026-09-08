---
name: adaptive-orchestrator-bridge
description: Invoke the external Adaptive AI Orchestrator engine through its CLI so OpenClaw chat can delegate governed work without duplicating orchestration logic.
license: MIT
user-invocable: true
metadata:
  author: oliveiraariel
  version: "0.1.0"
  openclaw:
    primaryEnv: OPENCLAW_GATEWAY_TOKEN
    requires:
      env:
        - OPENCLAW_GATEWAY_TOKEN
---

# Adaptive Orchestrator Bridge

This skill is a **thin invocation bridge**. It is not the orchestrator and must not reproduce Adaptive planning, policy, claims, frontier, evaluation, or replanning logic inside the prompt.

## When to use

Use this bridge when the user explicitly asks to run, use, delegate to, or execute work through the **Adaptive AI Orchestrator**.

Do not use it merely because the Adaptive repository is readable.

## Invocation

Invoke the helper at `{baseDir}/scripts/invoke.py` on the host. Pass the user's objective as `--objective` and use `--agent main` unless the user or project context identifies another OpenClaw agent.

Example:

```bash
python3 "{baseDir}/scripts/invoke.py" \
  --objective "Analyze this project and return the next safe engineering step." \
  --agent main
```

Pass `--accept` only for explicit acceptance text that the result can actually demonstrate. If no semantic acceptance criterion is available, omit it; the Adaptive CLI will validate runtime completion only and the response must say that semantic correctness was not independently proven.

If the task requires a side effect, declare it with `--side-effect`. Add the matching `--allow-side-effect` only when the user's request clearly authorizes that effect. Never infer authorization for unrelated writes, destructive operations, credential changes, publication, deployment, or external communication.

## Result handling

The helper returns the Adaptive CLI's JSON result. Report:

- `runtime_status`;
- `work_unit_state`;
- `verdict`;
- `output`;
- the execution identifier when useful.

A successful OpenClaw agent call is not sufficient by itself; distinguish runtime completion from Adaptive evaluation acceptance.

## Security rules

- Never print, echo, persist, or place `OPENCLAW_GATEWAY_TOKEN` in a prompt or command argument.
- The token must arrive through OpenClaw's per-skill environment injection or the trusted host environment.
- Do not request provider/model overrides unless the user explicitly requires them and Gateway policy authorizes them.
- Do not edit the Adaptive core to work around a denied execution policy.
- If the helper reports missing prerequisites, report the missing prerequisite rather than silently bypassing the bridge.
