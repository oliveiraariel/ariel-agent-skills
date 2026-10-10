---
name: documentation-governance
description: Establish and audit a proportional, traceable software documentation system, from discovery through verified delivery, without duplicating engineering skills.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.1"
---

# Documentation Governance

Own **the documentation system**, not every technical decision. Use for greenfield documentation planning, legacy documentation audits, PRD/SRS organization, evidence handoff, and reconciliations across repositories, agents, and document platforms.

Read [the artifact catalog](references/artifact-catalog.md) before choosing deliverables. Read [the elicitation coverage matrix](references/elicitation-coverage.md) when deciding what to ask or when reviewing unanswered requirements. Read [the artifact contract and quality gates](references/artifact-contracts.md) before publishing or auditing documents.

## Workflow

1. Discover existing documentation and authoritative sources with `project-discovery`. Capture repository, branch/commit, document location/version, owners, status, and environment evidence. Never impose a new tree over an established valid project scheme without an approved migration.
2. Classify the work: greenfield, feature change, maintenance, migration, security-critical, regulated, or documentation reconciliation; assess *risk and complexity*, not only project size.
3. Instantiate the **logical six-area catalog**. Each artifact is classified as essential information (E), conditional (C), or recommended (R); decide separately whether it is its own file/page, a section, generated evidence, or explicitly not applicable with rationale.
4. Build a documentation plan/manifest: artifact ID, canonical path or URL, ownership, upstream input, downstream consumer, applicability trigger, lifecycle status, version/baseline, review requirement, and links to acceptance evidence. Record exceptions.
5. Inspect existing evidence before asking anyone. For missing or ambiguous decisions, select `grilling` (or the user-facing `grill-me` alias), following the elicitation matrix: ask only the unblocked decision frontier, recommend grounded defaults, and distinguish facts, assumptions, proposals, approvals, and blockers. When the task includes durable documentation, use `grill-with-docs` to record answers in canonical locations and verify persistence. For architectural trade-offs, have the interview consult `software-architecture/references/pattern-decision-guide.md`; do not treat a technical recommendation as a business approval. Do not fabricate user decisions.
6. Route production: `software-specification` owns detailed behavioral contracts and acceptance; `domain-modeling` owns vocabulary/invariants; `software-architecture` owns boundaries/contracts/ADRs; `security-review` investigates security threats; `testing` owns verification evidence. This skill owns catalog, placement, traceability, audit, and synchronization rules.
7. Establish traceability for critical features: stakeholder outcome -> PRD/vision -> requirement -> business rule / scenario -> design/API/data -> implementation reference -> test/evidence. Use stable IDs and a canonical owner for each normative statement.
8. Audit document-to-document and document-to-code drift against an *approved baseline*. Never silently promote implemented behavior into requirements, or replace a human-approved decision with stale documentation. Report conflicting authority and human decisions separately.
9. Publish a reproducible handoff: artifact manifest, unresolved decisions, applicability exceptions, traceability gaps, verification status, and next safe action. Update the project's existing documentation rather than creating competing 'current' copies.

## Operating rules

- **E means content is essential, not that a separate file is mandatory.** **C** applies when its trigger is true. **R** may be omitted with a short rationale. Regulatory, contractual, privacy, or high-risk obligations override defaults.
- A PRD is a *product* planning artifact, not a universal prerequisite or substitute for testable requirements. SRS/ERS owns precise software requirements; the product and implementation must not silently share contradictory definitions.
- Maintain one authoritative location per decision, rule, invariant, and acceptance criterion. Other documents link to it by stable ID, rather than restating it inconsistently.
- Separate **normative target** (approved specification), **observed product state** (implementation), and **verified state** (test/review evidence). Preserve superseded baselines marked historical.
- Question coverage is determined by artifacts and risk, not by asking a fixed number of questions; don't overload a single round with dependent questions.
- A specification is not done merely because all sections are filled. Mark `DRAFT`, `PROPOSED`, `APPROVED`, `IMPLEMENTED`, `VERIFIED`, `SUPERSEDED`, or `N/A` distinctly; verification requires evidence and a specific code/artifact state.
- No new framework, document repository, or platform migration is implied. Documents may live in Markdown, Notion, a tracker, OpenAPI, schema files, or generated reports so long as authority, portability, and reviewability are clear.

## Completion gate

Documentation governance is ready when the artifact inventory is explicit, essential/triggered content is present or openly blocked, no competing current authority exists, crucial decisions are traceable and versioned, critical acceptance requirements have verification mappings, unresolved questions and implementation gaps are visible, and another agent can safely proceed from documented sources without reconstructing an interview.
