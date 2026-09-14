---
name: security-review
description: Review software security through explicit trust boundaries, threat scenarios, authorization rules, data handling, dependencies, observability, and evidence.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.3.0"
---

# Security Review

Scope the threat model before enumerating controls.

## Review areas

Inspect what is relevant: authentication, authorization, tenancy/ownership boundaries, input validation and injection, output encoding, secrets, sensitive data, storage and transport, session/token handling, CSRF/SSRF/path traversal/file upload, dependency/supply-chain exposure, logging/privacy, observability/event payloads, rate/abuse controls, privilege transitions, deployment configuration, and recovery paths.

Trace critical operations from untrusted input to privileged effect. Verify server-side enforcement; UI restrictions are not authorization.

Use project/framework/platform security guidance and version-specific primary sources when claims depend on current behavior.

## Learned observability rules

- Treat logs, traces, event streams, audit records, snapshots, and Control-Room-style projections as security boundaries, not harmless debugging output.
- Prefer explicit allowlists of operational metadata. Raw prompts, credentials, API keys, tokens, session secrets, private user data, and unnecessary payload contents must not cross an observability boundary merely because they simplify debugging.
- Correlation identifiers should be sufficient for diagnosis without exposing secret material. Review retention, access, and persistence of append-only logs as part of the threat model.
- When adding usage/cost/model metadata, verify that billing identifiers or provider responses do not accidentally introduce secrets or sensitive content.
- Recovery mechanisms must not broaden privileges or bypass execution policy merely to retrieve a lost result.

Security review is high-responsibility analytical work; prefer the strongest reasoning tier available under orchestrator policy.

## Incident and integrity boundaries

- Content hashes, contract hashes and commit hashes are integrity/provenance identifiers, not credentials or authorization mechanisms.
- Incident memory must be sanitized. Preserve bounded symptoms, classifications, identifiers and evidence references rather than raw prompts, tokens, credentials, source payloads or unnecessary user data.
- Permanent learning promotion must not turn a diagnostic artifact into a new secret-retention path.
- A proactive incident system does not gain extra authority from severity. Research, remediation, external communication, merge and deployment remain subject to their existing policy boundaries.
- Recovery or reference-based result access must preserve authorization and project ownership boundaries.

## Output

For each finding: severity, threat scenario, affected boundary/location, evidence, exploit preconditions, remediation, and verification status. Separate confirmed vulnerability from hypothesis or hardening suggestion.

## Completion gate

Security review is complete when material trust and observability boundaries have been examined, critical findings have evidence, sensitive-data exposure paths are explicitly considered where relevant, and residual/unverified risk is explicit.
