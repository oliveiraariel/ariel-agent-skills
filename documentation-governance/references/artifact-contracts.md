# Artifact contract, templates and documentation quality gates

## Canonical manifest record

```yaml
artifact_id: DOC-04
title: Software Requirements Specification
canonical_location: docs/requirements/srs.md
classification: E                 # E / C / R
placement: standalone            # standalone / section / generated / not_applicable
applicability: "all projects"
owner: "product/requirements authority"
status: DRAFT                    # DRAFT / PROPOSED / APPROVED / IMPLEMENTED / VERIFIED / SUPERSEDED / N/A
version: "0.1"
baseline_id: "BL-001"
supersedes: null
inputs: [DOC-01, DOC-02]
downstream_consumers: [DOC-06, DOC-11, DOC-16]
approval_evidence: null
verification_evidence: []
open_decisions: []
```

Put IDs in source documents as stable headers or machine-readable properties. Do not confuse a requirement's business approval with implementation/test verification; track status per dimension where necessary.

## Minimal schemas

**Requirement (RF/RNF):** ID, stakeholder value/source, statement using measurable language, rationale, preconditions, normal behavior, invalid/boundary/error behavior, dependencies, priority, approved state, acceptance criteria, verification reference.

**Business rule (RN):** ID, canonical language, scope, related RF/UC, invariants, exceptions, pre/postcondition, owner, examples and counterexamples.

**Use case (UC):** ID, actor, trigger, preconditions, main success path, alternatives, error paths, postconditions, relevant rules and acceptance tests.

**Architecture (DOC-11):** purpose/context, constraints, quality goals, components and responsibilities, trust/data boundaries, persistence, interfaces, failure/recovery flows, trade-offs/ADRs, operational assumptions, test seams.

**API/event contract (DOC-13):** version, endpoint/event name, caller permissions, request/response schema, validation, idempotency/retry, error taxonomy, backwards compatibility, sample cases and contract tests.

**Security (DOC-14):** assets/data classification, actors/trust boundaries, threat scenarios, authentication/authorization, secrets/storage/transit, audit/privacy, backup/recovery, vulnerabilities/dependencies, mitigations and tests, residual risk.

**Test case/evidence (DOC-16/17):** CT ID, mapped requirement/rule, environment, commit/build, steps or automated test identifier, expected/actual result, execution time, pass/fail/skipped, issue references, limitations and evidence location.

**Change record (DOC-20):** version/date, baseline, approved request, changed requirements/design/code, migration/compatibility impact, tests, residual risk and superseded artifacts.

## Gates

1. **Coverage:** every E and triggered C artifact has content and a canonical location; exceptions are recorded. Untriggered C are N/A, not missing.
2. **Clarity:** no ambiguous or unmeasurable critical requirement; unresolved decisions have an explicit owner/status.
3. **Integrity:** no contradictory active normative rules or duplicated authoritative text; historical pages visibly superseded.
4. **Traceability:** high-impact requirement -> rule/scenario -> design/code -> test evidence, with stable links.
5. **Security and reliability:** critical trust boundaries, invalid inputs, recovery, concurrency, irreversible actions and observability are addressed proportionally.
6. **Verification:** test claims contain exact executed evidence; unknown, pending and skipped are not passes.
7. **Handoff:** a fresh agent can locate the current approved baseline, exact implementation state, constraints, open questions and next safe task.

## Reconciliation output

Produce a table with `item ID | canonical decision and baseline | docs state | observed implementation and commit | verification evidence | discrepancy category | severity | owner/action`. Classify `DOC_STALE`, `SPEC_GAP`, `IMPLEMENTATION_GAP`, `TEST_GAP`, `AUTHORITY_CONFLICT`, or `HISTORICAL_ONLY`. Do not overwrite implementation gaps with 'doc updated'. Changes to approved product rules require actual approval.

## References for tailoring

- ISO/IEC/IEEE 29148:2018 (requirements engineering): https://www.iso.org/standard/72089.html
- ISO/IEC 25010:2023 (product quality characteristics): https://www.iso.org/standard/78176.html
- NIST SP 800-218 (secure development practices): https://csrc.nist.gov/pubs/sp/800/218/final
- arc42 architecture documentation structure: https://arc42.org/overview/

These resources inform tailoring; referencing them does **not** assert certification or full standards compliance.
