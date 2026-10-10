# Documentation-driven elicitation and interview coverage

Use this matrix with `grilling`, `grill-me`, or any requirements interview. Read existing evidence first; ask **human choices** only when evidence cannot settle them. The interview's aim is to make target artifacts implementable, not to force a fixed questionnaire. Each decision must be attached to an artifact/requirement ID and recorded persistently.

| Decision domain | Ask only if unknown and material | Expected artifact(s) |
|---|---|---|
| Problem and outcomes | Which problem, whose outcome, success measure, constraints? | DOC-01, DOC-02 |
| Stakeholders and authority | Who uses, approves, operates, and can change priorities? | DOC-01, DOC-03 |
| Scope and versions | What is in/out, MVP versus future, acceptance boundary? | DOC-02, DOC-04, DOC-20 |
| Actors and permissions | Identity, roles, tenant/data boundaries, privileged actions? | DOC-04, DOC-06, DOC-14 |
| Core workflow | Trigger, normal path, alternatives, invalid/boundary paths, cancellation? | DOC-04, DOC-05, DOC-06 |
| Domain invariants | Vocabulary, states, lifecycle, calculations, consistency, concurrency? | DOC-05, DOC-08, DOC-09 |
| Data lifecycle | Source, ownership, validation, storage, retention, deletion, migration, recovery? | DOC-09, DOC-10, DOC-14 |
| Interfaces/integrations | Consumers, contract/version compatibility, failures, idempotence? | DOC-11, DOC-13 |
| Quality attributes | Measurable availability, latency, volume, accessibility, maintainability? | DOC-04, DOC-11, DOC-15, DOC-16 |
| Security and privacy | Threats, consent/authorization, encryption, secrets, audit and abuse paths? | DOC-04, DOC-14, DOC-16 |
| UX and accessibility | Devices, states, error messages, navigation, inclusive interaction? | DOC-06, DOC-15 |
| Architecture and deployment | Runtime, environment, failure domains, dependencies, rollbacks? | DOC-11, DOC-12, DOC-18, DOC-19 |
| Verification and release | Acceptance evidence, test tiers, negative cases, release criteria? | DOC-07, DOC-16, DOC-17, DOC-20 |
| Continuity and change | Owners, approval, documentation authority, known legacy versions? | DOC-03, DOC-07, DOC-20 |

## Procedure

1. Inventory what is already known and cite its source, version and confidence. A codebase fact is not necessarily an approved product decision.
2. Derive question candidates from gaps/contradictions in applicable artifact contracts; attach target IDs and decision prerequisites.
3. Order questions as a dependency tree. Ask only a bounded **currently unblocked** round; do not ask a downstream API/schema choice before its product rule is settled. Offer a reasoned recommendation, and mark whether it is a proposed default or approved fact.
4. For each answer create/update a durable decision entry:
   - `DEC-ID`, topic, question, alternatives, human answer/authority, rationale, decision date, status, affected DOC IDs, affected RF/RN/UC/ADR/test IDs, source link.
   - If unresolved: `OPEN`/owner/next question/blocking scope; don't substitute assumptions for approval.
5. After each round update the applicable canonical documents or an append-only decision ledger, then report updated paths. Keep draft and approved states distinct.
6. At closure verify: no material decision branch silently assumed, coverage by required artifacts, unresolved blockers visible, downstream consumer and acceptance boundary identified, and agent handoff self-contained.

## Grilling implementation safeguards

- `grilling` is a general interviewing skill; these questions are activated **only for software/documentation planning**, never for unrelated personal questioning.
- `grill-me` remains a thin user-facing alias; it should not independently define a second interrogation policy.
- If a requested interview skill is outside the active runtime/repository, load its actual source or use this elicitation matrix directly. Never claim a wrapper has produced persistent documentation without verifying writes.
- Do not make an exhaustive question dump; asking the entire decision frontier still requires practical batching and user agency.
