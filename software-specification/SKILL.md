---
name: software-specification
description: Turn product intent, project evidence, and domain decisions into an implementable software specification with checkable acceptance criteria.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Software Specification

A specification is an **implementation and independent review contract**, not a narrative recap of an interview. For documentation catalog, proportional deliverables and canonical authority, follow `documentation-governance`; do not recreate its taxonomy here.

## Entry

1. Use `project-discovery` to locate the approved scope, baseline, existing PRD/vision, known requirements, business rules, domain model and relevant code/tests.
2. If decisions are missing, ask only material unblocked questions, preferably with `grilling` and the documentation-governance elicitation matrix when accessible. Facts should be investigated; human decisions need explicit authority. Preserve every answer in a durable decision record or an approved artifact, never conversation alone.
3. Distinguish **product intent** (Vision/PRD), **normative requirements** (SRS/ERS), **rules/invariants** (catalog or SRS section), and **solution design** (architecture, API, schema). A PRD is not mandatory and does not replace testable requirements.
4. Specify only the approved scope. Unapproved recommendations remain `PROPOSED`; absent facts remain `OPEN`, not implied agreements.

## Implementation contract

Include, as applicable:

- objective, users, boundaries, business outcomes, version and explicit non-goals;
- current behavior, exact reference evidence and intended changed behavior;
- individually identifiable functional requirements and measurable nonfunctional quality requirements (including constraints on security, privacy, accessibility, performance, reliability and compatibility appropriate to risk);
- canonical business rules/invariants and related IDs, preconditions, state/data transitions, user scenarios and alternate/error/boundary behavior;
- integrations, external interfaces and API expectations at the requirement level, linking detailed design/contract files rather than duplicating them;
- measurable acceptance criteria with negative cases, failure/recovery expectations and dependencies;
- approved decisions, unresolved decision owners, risks and explicit blockers;
- stable links to domain/architecture/data design and planned test/evidence IDs.

Prefer one authoritative requirement statement per ID. If the project has an existing valid spec format, extend it rather than imposing a parallel one. Do not demand a separate document for every logical artifact.

## Quality gate

A competent implementer can build the approved behavior, an independent reviewer can verify it without guessing, and each high-impact requirement has a planned test/evidence path. No critical ambiguity, hidden baseline conflict, unverifiable adjective ("fast", "secure", "intuitive") or undocumented exception remains. Incomplete decisions stay visibly open; nothing is marked implemented or verified until code-state-specific evidence exists.
