---
name: project-handoff
description: Compact current project state into a redacted, pointer-based handoff so another agent or session can continue without re-discovery.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Project Handoff

Create continuity, not a second copy of the project documentation.

## Include

- objective and current state;
- completed work with commit/artifact/evidence pointers;
- authoritative decisions and where they live;
- active Work Units, blockers, dependency/frontier state when available;
- tests/reviews actually run and their outcomes;
- unresolved risks or assumptions;
- exact next action and suggested skills/capabilities for the next agent.

Reference specs, ADRs, plans, issues, diffs, and large documents by path or URL instead of duplicating them. Redact credentials, secrets, tokens, personal data, and unnecessary sensitive context.

## Completion gate

The handoff is complete when a fresh agent can resume at the next action without asking for history already present in authoritative artifacts and without receiving sensitive data it does not need.
