---
name: project-handoff
description: Compact current project state into a redacted, pointer-based handoff so another agent or session can continue without re-discovery or duplicate execution.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.4.0"
---

# Project Handoff

Create continuity, not a second copy of the project documentation.

## Current-authority rule

A handoff that preserves history must still expose exactly one unmistakable **current authoritative state** near the top. That block/pointer should include, when relevant:

- active branch and exact HEAD/commit;
- whether the working tree contains WIP that must be preserved;
- current stage/lifecycle position;
- latest verified test/check baseline;
- active or recoverable execution identifiers;
- exact next safe action.

Older sections may remain for provenance, but if they contain now-obsolete claims (for example an older HEAD, unavailable tooling that has since been restored, or a stage that has since started), mark them explicitly as historical/non-current. Never leave two sections that both plausibly claim to be the current authority.

## Include

- objective and current state;
- completed work with commit/artifact/evidence pointers;
- authoritative decisions and where they live;
- active Work Units, blockers, dependency/frontier state when available;
- active or recently interrupted asynchronous executions, including safe correlation identifiers needed for recovery such as orchestration/task/execution/run/session references when available;
- pending obligations such as review, re-review, CI, merge, smoke, acceptance validation, or replanning;
- tests/reviews actually run and their outcomes, including the exact code state reviewed when relevant;
- unresolved risks or assumptions;
- exact next action and suggested skills/capabilities for the next agent.

Reference specs, ADRs, plans, issues, diffs, and large documents by path or URL instead of duplicating them. Redact credentials, secrets, tokens, personal data, raw prompts, and unnecessary sensitive context.

## Learned continuity rules

- Do not label a handoff “completed” merely because the current session is ending. Distinguish project/work completion from session termination.
- If recoverable asynchronous work may still exist, say so explicitly and provide the identifiers and authoritative state needed to reconcile it before redispatch.
- Record whether a review verdict is current or stale relative to HEAD. A successor must not reuse approval from an older code state.
- Separate model-quality failures from runtime/transport/tool/environment failures so the next agent does not choose the wrong remediation or model escalation.
- Prefer a resumable checkpoint over vague text such as “continue later”: state exactly what is done, what remains, what must not be repeated, and the next safe action.

## Incident continuity

When Adaptive exposes unresolved incidents, include their safe references in the handoff together with status, pressure/priority when relevant, latest validated evidence, and the next governed action. Do not copy the incident's entire raw timeline into the handoff.

An unresolved incident survives session termination. A successor should reconcile the same incident and any associated execution/result references before creating replacement work.

For large upstream results, preserve authoritative result references rather than duplicating payloads. Keep runtime/execution/result identity together so a future agent can verify and recover the exact artifact.

## Completion gate

The handoff is complete when a fresh agent can resume at the next safe action without asking for history already present in authoritative artifacts, without duplicating recoverable work, without mistaking pending obligations for completion, and without receiving sensitive data it does not need.
