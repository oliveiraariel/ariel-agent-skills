---
name: grill-with-docs
description: Conduct documentation-driven software decision interviews and persist traceable decisions, vocabulary and architecture records in canonical project artifacts.
license: MIT
metadata:
  author: oliveiraariel
  version: "1.0.0"
---

# Grill With Docs — Elicitation With Durable Records

Use when the user wants to clarify a software project, feature or system design **and** preserve decisions so a different skill, agent or session can prepare an implementable specification without replaying the conversation.

Compose `project-discovery`, `documentation-governance`, `grilling` and `domain-modeling` as needed. Consult `software-architecture` when material architectural alternatives arise. Do not assume any particular tool invocation interface: select available skills/capabilities or read their local `SKILL.md` instructions if the runtime does not support automatic composition.

## Startup and authority

1. Confirm project, actual repository/workspace, branch/ref, existing canonical documentation, decision approval authority and permitted write scope using `project-discovery`. Do not write to a generic workspace or an unrelated repository.
2. Load the project's existing documentation rules. If none exist, use:
   - `../documentation-governance/references/artifact-catalog.md`
   - `../documentation-governance/references/elicitation-coverage.md`
   - `../documentation-governance/references/artifact-contracts.md`
3. Select the **applicable** documents and target decision IDs. Distinguish a product PRD from an SRS, a domain rule from an architectural design choice, and a design decision from an implementation fact.
4. Locate the project's **existing canonical** decision register, glossary and ADR location. If no locations are defined, propose a single `docs/decisions/decision-log.md` for durable decisions, `docs/domain/glossary.md` for vocabulary and `docs/adr/` for architectural trade-offs, **subject to project conventions and write authorization**. Do not create competing sources of truth.

## Interview and update loop

1. Use `grilling` to build the dependency tree, investigate discoverable facts and ask only a bounded unblocked decision frontier.
2. Every question must identify its destination(s): vision/PRD, SRS/RF/RNF, business rule/invariant, use case, domain/data model, architectural decision, API/security/UX contract or test obligation. For architecture, load `../software-architecture/references/pattern-decision-guide.md` when patterns are in question; compare plausible alternatives **against real requirements** before asking for authority to choose.
3. On each resolved answer, create/update a durable decision entry with `DEC-ID`, Q-ID, decision, alternatives, rationale, source/evidence, approval status/authority, affected DOC and requirement IDs, baseline, owner and downstream consequences.
4. Update the existing glossary with **definitions only**, if vocabulary was settled. Create an ADR only for an architecturally significant trade-off (context, options, selected option and consequences). Register ordinary approved behavior in the canonical business-rule/SRS source or decision ledger; do not hide it in a glossary or make every answer an ADR.
5. Write **only within the authorized destination**. A user's interview response does not by itself grant repository or external publication access. Do not overwrite existing approved text, silently migrate a structure, auto-commit, auto-merge, deploy or mutate production.
6. After writing, read the affected artifacts back or otherwise verify the exact persisted path/content. If a write tool is unavailable or verification fails, report the result as **NOT_PERSISTED**, preserve the structured decision handoff in the response, and do not pretend that another agent will find the files.
7. If a new answer contradicts an approved rule, retain the old rule as current until authorized change control approves its supersession; record the candidate correction as `PROPOSED`/`AUTHORITY_CONFLICT`.

## Quality and handoff gate

Check that the applicable artifact catalog has no silently omitted essential information; the resolved decisions are correctly approved or proposed; critical requirements cover normal, invalid, alternate, concurrency, security, recovery and acceptance cases when material; architecture alternatives document their selection criteria; there are no duplicate active authorities; and all paths/versions are explicit.

Produce a small **document-ready handoff** to `software-specification`, `domain-modeling` and `software-architecture` as appropriate:

`baseline | artifact manifest | DEC/Q links | approved requirements/rules | glossary/ADR pointers | open decisions and blocker owners | persisted file paths | verification of writes | next safe step`.

An implementer should not need to reconstruct the interview from chat to understand the approved behavior. Do not mark a requirement `VERIFIED` unless executable evidence actually supports it.
