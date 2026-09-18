---
name: integration-release
description: Integrate validated changes safely through intent-aware conflict resolution, CI gates, current-HEAD review, release-artifact verification, post-integration checks, human authority, and rollback planning.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Integration and Release

Integration is an engineering step, not merely a Git command.

## Workflow

1. Confirm required implementation, testing, code review, security review, and platform-specific gates are complete for the exact code state being integrated.
2. Verify that any required review verdict is authoritative and bound to the current HEAD. If the code changed after review, treat the prior verdict as stale and require re-review.
3. Reconcile branch drift and merge/rebase conflicts by tracing the intent and primary source of each side. Preserve valid behavior from both; abort/restart is allowed when it is safer than guessing.
4. Re-run affected tests and CI after integration when the project contract requires them.
5. When producing an installable/deployable release artifact, apply the release-artifact packaging standard below to the exact intended source state.
6. Execute required post-merge/post-integration smoke or acceptance validation; do not treat merge itself as completion when those checks are part of the requested outcome.
7. Identify migrations, configuration changes, feature flags, compatibility windows, and ordering requirements.
8. Define rollback/recovery before irreversible or high-impact changes.
9. Treat production mutation, credential use, destructive operations, installation/activation, publication, and other externally consequential actions as authority checkpoints governed by the host runtime/orchestrator.
10. Record release evidence and known residual risk.

## Release artifact packaging standard

Use this standard whenever the work creates or regenerates an installable/deployable artifact such as a ZIP, plugin/theme package, runtime bundle, or equivalent archive. Project-specific release/build rules remain authoritative.

### Exact source → artifact identity

- Confirm the authoritative repository/worktree, branch/ref, HEAD when available, and working-tree state before packaging.
- Package the intended current state. Intentional dirty WIP is allowed only when explicitly recognized and reported.
- Never silently package a stale commit or reuse an artifact generated before the validated change.
- For a fix/hotfix/retest, generate a fresh artifact after the relevant gates pass.

### Validation before packaging

- Execute the smallest sufficient existing project-defined gates relevant to the artifact: build, tests, lint/syntax, contract/composition, smoke, or equivalent when applicable.
- Do not invent a framework-specific gate merely to fill a checklist.
- Never report a gate as `PASS` if it was not executed against the packaged source state.
- If a required local gate fails, the artifact is not ready for release/retest unless it is explicitly diagnostic and marked accordingly.

### Runtime-only composition

Include only runtime-required material and production dependencies/assets. Exclude unless explicitly required by the target runtime:

- source-control metadata;
- environment files, secrets, tokens, credentials, keys;
- tests/fixtures;
- caches and temporary files;
- local state;
- development-only tooling/documentation.

Validate the platform-specific package root, entrypoint/manifests, runtime dependencies/autoload/assets, and absence of accidental extra directory nesting.

### Integrity evidence

Before declaring the artifact ready:

- run the archive/package integrity check appropriate to the format;
- verify expected runtime files are present;
- verify forbidden sensitive/development material is absent;
- compute SHA-256;
- record artifact size;
- report filename/path, package root, main entrypoint/manifest when applicable, source identity, working-tree state, and validations actually executed.

The filename is not proof of identity. Source identity plus checksum is the artifact fingerprint.

### Authority boundary

Packaging does not itself authorize merge, publication, deploy, remote upload, installation, activation, or destructive environment changes. These are separate authority gates.

A package may be locally ready while real environmental validation remains pending. Keep those states explicit instead of turning package creation into a false end-to-end `PASS`.

## Learned gate invariants

- `REQUEST CHANGES`, a still-running review, an unreconciled review, failed/unknown CI, or a stale review blocks integration when that gate is required.
- Tests passing do not waive required independent review; review approval does not waive required tests/CI; merge does not waive required post-merge validation.
- If an asynchronous gate is still active, reconcile and await it within policy rather than creating duplicate reviewers/checks or silently proceeding.
- A recovered text fragment saying `APPROVE` is insufficient when the authoritative run/review state is not terminal or does not match current HEAD.
- Preserve the exact evidence chain from reviewed commit -> approved verdict -> CI/test state -> merge -> post-integration verification.
- Bind every release artifact to the exact intended source state.
- A retest package created after a change must be a fresh artifact, not an ambiguous reuse of an older archive.
- Runtime release packages should contain runtime requirements, not development residue or secrets.
- Archive integrity and SHA-256 are required release-artifact evidence when the format supports them.
- Packaging authority never implies deploy/install/publish authority.

## Artifact readiness versus orchestration debt

Release/retest gating must distinguish defects in the artifact from defects in orchestration observability.

If the exact artifact source has passed its required product gates, authoritative results are intact, and there is no evidence of corruption, unsafe concurrency, stale source identity, or unmet functional/security criteria, a historical Adaptive lease/checkpoint/observability gap may be recorded as a separate infrastructure incident instead of forcing recursive recovery of an otherwise valid artifact.

This separation never waives a gate that can materially affect the artifact. Report both states explicitly, for example `READY_FOR_ENVIRONMENTAL_RETEST` plus an unresolved Adaptive observability incident.

Integration/release decisions are high-responsibility work; prefer a strong reasoning tier when model routing is available.

## Completion gate

Release is complete only when the integrated artifact passes every required gate for the exact released code state, required post-integration validation is terminal, operational ordering is clear, no required asynchronous gate remains merely pending, and the rollback/recovery path matches the risk of the change.
