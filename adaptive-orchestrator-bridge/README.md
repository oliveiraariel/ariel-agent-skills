# Adaptive Orchestrator Bridge

Thin OpenClaw-facing bridge for invoking the external `adaptive-ai-orchestrator` engine.

## What it is

This skill does not implement orchestration logic. It delegates to the Adaptive CLI and returns its structured result.

## Resolution order

`adaptive-orchestrator-bridge/scripts/invoke.py` resolves the engine in this order:

1. `ADAPTIVE_ORCHESTRATOR_ROOT/.venv/bin/python -m adaptive_orchestrator`;
2. a sibling `adaptive-ai-orchestrator` repository with `.venv/bin/python`;
3. an installed `adaptive-orchestrator` executable on `PATH`.

This allows portable installations while supporting the common development layout where `ariel-agent-skills` and `adaptive-ai-orchestrator` are sibling repositories.

## Gateway credentials

The bridge remains eligible across token, password, and unauthenticated Gateway modes. For token authentication, `OPENCLAW_GATEWAY_TOKEN` is the primary environment variable and can be injected through OpenClaw's per-skill `apiKey` / SecretRef mechanism. Password authentication uses `OPENCLAW_GATEWAY_PASSWORD`.

Do not put Gateway credentials in `SKILL.md`, prompts, shell arguments, or repository files.

## Example host invocation

```bash
python3 adaptive-orchestrator-bridge/scripts/invoke.py \
  --objective "Respond exactly with BRIDGE_OK." \
  --agent main \
  --accept BRIDGE_OK
```

The command forwards to the Adaptive CLI and returns the same exit status and JSON output.
