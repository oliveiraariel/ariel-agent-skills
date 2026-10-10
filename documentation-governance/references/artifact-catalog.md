# Canonical software documentation catalog (v1)

This is a **logical catalog**, not a compulsory folder list or a claim of regulatory compliance. Six areas contain twenty artifact types. Every project instantiates the same catalog and records for each type: `E` essential information, `C` conditionally needed, or `R` recommended; independent/embedded/generated placement; owner; canonical URL/path; applicability reason; status; evidence.

## Classification and packaging

- `E` = content required in some reviewable form. Could be a section, README, test suite, generated contract, or standalone artifact.
- `C` = required **if the stated trigger applies**; otherwise mark `N/A` with rationale.
- `R` = useful default, may be omitted when equivalent information exists or is unnecessary. An explicit regulation/contract or significant project risk can elevate a C/R artifact to E.
- Document *independence* is orthogonal: split when it has a distinct owner, update cadence, audience, review/approval gate, or durable machine-readable contract. Otherwise link or embed it. Never duplicate authoritative rules.

### 01 — Product and planning

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-01 | Vision / product intent | E | Vision section or standalone | Problem, users, value, objectives, boundaries, success measure |
| DOC-02 | PRD | R | Standalone for product-led work; section otherwise | Users, outcomes, scope, features, priorities, non-goals; do not replicate SRS in full |
| DOC-03 | Project / delivery plan | E | Plan, README or tracker | Milestones, responsibilities, constraints, risks, dependencies, delivery/acceptance approach |

### 02 — Requirements and business rules

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-04 | SRS / ERS / requirements contract | E | Canonical specification | Functional requirements, measurable quality requirements, constraints, interfaces, acceptance, exclusions |
| DOC-05 | Business rule and invariant catalog | E | SRS section, separate if complex | Named rules with IDs, applicability, pre/postconditions, exceptions, ownership |
| DOC-06 | Use cases / user scenarios | C | SRS section or per-flow files | Actors, triggers, normal/alternative/failure flows; applies to substantial user/business workflows |
| DOC-07 | Traceability matrix | R | Index or generated table | Outcome -> requirement -> rule/scenario -> design -> code -> test; elevate for large/critical/regulated work |
| DOC-08 | Glossary | R | Shared vocabulary | Definitions of ambiguous domain/technical terms; elevate when multiple actors or overloaded terms exist |

### 03 — Domain and data analysis

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-09 | Domain model | C | Domain section or standalone | Concepts, lifecycle states, invariants, relationships; applies to nontrivial business-domain behavior |
| DOC-10 | Data model / schema dictionary | C | Models or versioned schema | Entities, ownership, constraints, migrations, relationships; applies when persistent structured data exists |

### 04 — Technical solution and controls

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-11 | Architecture | E | Short architectural overview or standalone | Context, components, trust/dependency boundaries, data flow, critical trade-offs, deployment topology |
| DOC-12 | Architecture decision records (ADRs) | R | Individual dated/numbered decisions | Significant trade-offs, decision status, consequences; conditional elevation for material choices |
| DOC-13 | API / integration contract | C | OpenAPI, event schema or standalone | Operations, versions, validation, auth, errors, compatibility; applies when API/events/integrations exist |
| DOC-14 | Security / privacy specification | E | Security section or standalone | Threats, trust boundaries, permissions, data classification, secrets, audit, recovery and verification obligations |
| DOC-15 | Interface design / UX contract | C | UI specs and prototypes | Routes, states, accessibility, error behavior; applies if users interact with an interface |

### 05 — Verification and quality

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-16 | Test strategy, cases and acceptance checks | E | Plan, test code and scenario index | Test levels, key boundaries, acceptance IDs, data, environments, expected outcomes |
| DOC-17 | Test results and evidence | E | CI artifacts, reports or test history | Actual commands, timestamp, commit/build ID, pass/fail/skip, gaps; never treat a plan as execution |

### 06 — Delivery, operation and evolution

| ID | Artifact | Class | Default container | Minimum information / trigger |
|---|---|---|---|---|
| DOC-18 | Deployment / installation guide | C | README / runbook | Prerequisites, configuration, install, rollback; applies when installation/deployment is required |
| DOC-19 | Operations / support runbook | C | Runbook or README | Monitoring, incident response, backup/restore, ownership, maintenance; applies to operated/live systems |
| DOC-20 | Change and version history | E | CHANGELOG, release notes or version log | Version/baseline IDs, meaningful changes, approvals, migration notes where relevant |

## Recommended extension modules, not 21st+ mandatory artifacts

For a project requiring them, attach specialized artifacts to the owning area: stakeholder map, risk register, data dictionary, migrations, data retention/privacy assessment, threat model, observability/SLO plan, performance budgets, accessibility audit, CI/CD plan, incident/disaster recovery, regulatory evidence, procurement/vendor contracts. Record every extension in the manifest with its applicability trigger and canonical owner.

## Proportionality and independence

- **Small / lower-risk**: one structured project spec (vision+SRS+rules+key scenarios), a brief architecture/security section, tests with stored results, setup instructions where needed, and version history. Optional PRD. Structured data/API/UI specs only if relevant.
- **Medium**: distinct Vision/PRD when useful, SRS, domain/rules, models, architecture/security/API/UX as applicable; an evidence-linked test strategy, traceability and delivery runbooks. Independent artifacts when different maintainers or revision cycles exist.
- **Large or critical**: independent approved baselines; formal SRS and rule catalogs, detailed scenario and traceability coverage, independent security/privacy and operations evidence, ADRs, automated schema/API contracts, risk-focused test plans, controlled changes and review/audit trails.
- **Risk supersedes size**: an apparently small regulated or security-critical product may require more rigor than a large low-risk internal tool.

## Authority and precedence

For every scope, identify one approved baseline and its change authority. Within its owned domain, normative requirements/decisions outrank implementation; code and tests are evidence of observed behavior, not automatic amendments. CI reports are facts only for the exact commit/build tested. Historical documents are retained with `SUPERSEDED` + link to replacement. If conflicting sources claim precedence, flag `AUTHORITY_CONFLICT` and request a decision; do not resolve by latest timestamp alone.
