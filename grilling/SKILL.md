---
name: grilling
description: Clarify ambiguous plans and software requirements through bounded, evidence-led decision interviews with documented trade-offs and downstream handoff.
license: MIT
metadata:
  author: oliveiraariel
  version: "1.0.0"
---

# Grilling — Decision Interview

Use when the user asks to "grill" an idea, stress-test a plan, clarify an ambiguous software objective, or resolve material decisions before implementation. Interview for **decisions**, not for discoverable facts. Stay useful for non-software topics: the software documentation and architecture rules below activate only when the objective concerns software.

## 1. Discover and classify

1. Read the stated objective and available evidence. For software, use `project-discovery` to locate the canonical project baseline, specs, code, tests, existing decisions and approval authority before asking.
2. For software, read `documentation-governance/references/artifact-catalog.md` and `documentation-governance/references/elicitation-coverage.md` as relevant. Determine which document types apply to this project or change; do not assume every project needs a standalone PRD, every type of model or twenty physical documents.
3. Classify gaps as **facts to investigate**, **business/product decisions requiring human authority**, **design alternatives to analyze**, or **open external dependencies**. Gather facts from available evidence; never ask the user to recall something reliably discoverable.
4. Build a **decision dependency tree**. Each candidate question has a stable Q-ID, topic, prerequisite question/decision IDs, target DOC/RF/RN/UC/ADR references (if software), risk/criticality, and the expected effect of the answer.

## 2. Ask only the useful frontier

- The frontier comprises **unanswered decisions whose prerequisites are already settled**. Do not ask a downstream database schema or framework choice before the governing domain behavior, operating constraints and quality requirements are understood.
- Ask a manageable round of independent frontier decisions, typically 2–5 questions and fewer if each is substantial; one question when one answer is sufficient. Rank by ambiguity, architectural impact, business risk and blocker severity. Do not dump the entire project questionnaire in one message.
- For each question, give: `Q-ID`, the decision to make, why it matters, realistic options and their consequences, your evidence-based recommendation (if possible), and the specific documents/requirements affected. State clearly when there is not enough evidence for a recommendation.
- Await user answers before claiming a decision is approved. Recalculate the frontier after the answers, incorporating corrections, conflicts and new constraints. Do not repeat resolved questions.

Example:

```text
Q-ARCH-003 — Qual estratégia de implantação atende ao objetivo?
Contexto: requisito RNF-012 exige implantação local, sem equipe operacional.
Alternativas: monólito modular (menos complexidade operacional) ou serviços separados (mais coordenação).
Recomendação proposta: monólito modular, sujeita à confirmação das restrições.
Destinos: DOC-04, DOC-11, DOC-12. Estado: PROPOSED.
```

## 3. Software engineering decision guides

For software-related interviews, route questions by the target *artifact* and the responsible engineering skill:

- Product purpose, users, scope, success and priority → `documentation-governance` DOC-01..03; `software-specification` for implementable behavior.
- Functional requirements, exceptions, business invariants, quality attributes and acceptance → DOC-04..08; `software-specification` + `domain-modeling`.
- Data ownership, state transitions, deletion, concurrency, migration, privacy and recovery → DOC-09..10, DOC-14; `domain-modeling` + `software-architecture`.
- Architecture, APIs, distributed boundaries, patterns, deployment constraints and trade-offs → DOC-11..13, DOC-18..19; `software-architecture/references/pattern-decision-guide.md`.
- UI, accessibility, security threat surfaces, tests, release and operability → DOC-14..20; select `web-frontend-design`, `security-review`, `testing` and `integration-release` when material.

For architectural choices, **do not begin by asking which named pattern the user prefers**. First discover scale, team, deployment, existing stack, availability, data consistency, change frequency, integrations, security, operational capacity and cost constraints. Use the architecture guide to compare viable patterns; give the user meaningful trade-offs and distinguish decisions that an authorized engineer may take under an approved requirement from those needing human sign-off. Never impose microservices, DDD, hexagonal layers, CQRS or an event bus by default.

## 4. Capture decisions for durable use

During each round preserve a compact decision register (or link to the project's existing canonical ledger) with:

`DEC-ID | question | answer/alternatives | rationale/evidence | approval authority | approval status | baseline/version | affected artifacts and requirement IDs | dependencies | follow-up owner`.

- A recommended default or model inference is **PROPOSED**, not `APPROVED`. An unresolved choice is `OPEN` with its blocker/owner. An explicit authorized choice may be recorded `APPROVED`.
- Do not treat observed code as automatic approval of a requirement. Never overwrite an approved baseline because an implementation disagrees.
- In plain `grilling`, communicate the decision register as a structured handoff. **Do not claim documents were persisted.** For persistent document editing select `grill-with-docs`, obey write authority and verify the resulting files.
- When existing docs are present, reference canonical facts by identifier and location rather than making duplicate current rules.

## 5. Close safely

Conclude when material, applicable decision branches are answered, explicitly delegated, or marked as open blockers; the user has confirmed the shared understanding for decisions under their authority; and the downstream documentation producer knows the selected baseline, approved choices, open questions and target artifacts. Do not prolong an interview merely to fill irrelevant template sections.

**Output:** a decision summary, Q/DEC traceability, affected document IDs, unresolved blockers, proposed handoff to `software-specification` or `grill-with-docs` and clear statement of whether any persistent artifact was actually written.
