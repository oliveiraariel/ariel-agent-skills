---
name: project-handoff
description: Compact current project state into a redacted, pointer-based handoff so another agent or session can continue without re-discovery or duplicate execution.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Project Handoff

Create continuity, not a second copy of the project documentation.

## Canonical path and naming rule

Unless the project explicitly defines another canonical handoff path in its own governance, the current authoritative handoff MUST be exactly:

```text
HANDOFF.md
```

Treat `HANDOFF.md` as a stable pointer to the current project/session continuity state. Update it in place. Do not create a new dated file merely because a session ended or a handoff was refreshed.

Do not invent current-authority names such as:

```text
HANDOFF-ETAPA-11-CONTEXTO-2026-09-16.md
HANDOFF-CURRENT-2026-09-17.md
HANDOFF-FINAL.md
```

A dated handoff may exist only as an intentional historical snapshot. When a snapshot is actually required and the project does not define a stricter convention, use:

```text
docs/governanca/handoffs/HANDOFF-YYYY-MM-DD-HHMM-<SCOPE>.md
```

Rules for historical snapshot names:

- use a sortable `YYYY-MM-DD-HHMM` timestamp;
- use the project's local timezone when explicitly known, otherwise UTC;
- `<SCOPE>` is optional and, when present, must be a short stable uppercase/kebab-style scope such as `ETAPA-11` or `API-HOTFIX`;
- the snapshot must state near the top that it is historical/non-current;
- the snapshot must point back to the canonical current handoff;
- a historical snapshot never competes with the canonical handoff for current authority.

If a legacy file with a dated or descriptive handoff name is currently being used as the live handoff, migrate its current authoritative content into the canonical path, preserve history only when useful, and remove or clearly archive the legacy current-looking file. Never leave two files that both plausibly claim to be the current handoff.

When resuming work, read the project-defined canonical handoff first. If the project has no explicit override, read `HANDOFF.md`. Do not choose the current handoff by sorting dated filenames.

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
- Keep exactly one current-authority handoff path; dated files are historical snapshots only.
- Resume from the canonical handoff path, never by guessing which dated filename is newest.

## Completion gate

The handoff is complete when a fresh agent can resume at the next safe action without asking for history already present in authoritative artifacts, without duplicating recoverable work, without mistaking pending obligations for completion, without receiving sensitive data it does not need, and without ambiguity about which handoff file is current.