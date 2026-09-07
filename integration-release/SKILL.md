---
name: integration-release
description: Integrate validated changes safely through intent-aware conflict resolution, CI gates, migrations, release checks, human authority, and rollback planning.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Integration and Release

Integration is an engineering step, not merely a Git command.

## Workflow

1. Confirm required implementation, testing, code review, security review, and platform-specific gates are complete for the scope.
2. Reconcile branch drift and merge/rebase conflicts by tracing the intent and primary source of each side. Preserve valid behavior from both; abort/restart is allowed when it is safer than guessing.
3. Re-run affected tests and CI after integration.
4. Identify migrations, configuration changes, feature flags, compatibility windows, and ordering requirements.
5. Define rollback/recovery before irreversible or high-impact changes.
6. Treat production mutation, credential use, destructive operations, and other externally consequential actions as authority checkpoints governed by the host runtime/orchestrator.
7. Record release evidence and known residual risk.

## Completion gate

Release is complete only when the integrated artifact passes required gates, operational ordering is clear, and the rollback/recovery path matches the risk of the change.
