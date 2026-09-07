---
name: security-review
description: Review software security through explicit trust boundaries, threat scenarios, authorization rules, data handling, dependencies, and evidence.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Security Review

Scope the threat model before enumerating controls.

## Review areas

Inspect what is relevant: authentication, authorization, tenancy/ownership boundaries, input validation and injection, output encoding, secrets, sensitive data, storage and transport, session/token handling, CSRF/SSRF/path traversal/file upload, dependency/supply-chain exposure, logging/privacy, rate/abuse controls, privilege transitions, deployment configuration, and recovery paths.

Trace critical operations from untrusted input to privileged effect. Verify server-side enforcement; UI restrictions are not authorization.

Use project/framework/platform security guidance and version-specific primary sources when claims depend on current behavior.

## Output

For each finding: severity, threat scenario, affected boundary/location, evidence, exploit preconditions, remediation, and verification status. Separate confirmed vulnerability from hypothesis or hardening suggestion.

## Completion gate

Security review is complete when material trust boundaries have been examined, critical findings have evidence, and residual/unverified risk is explicit.
