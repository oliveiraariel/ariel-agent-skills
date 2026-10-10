# Architectural Pattern Decision Guide

This guide supports `software-architecture`, `grilling` and `grill-with-docs` when genuine architecture decisions affect implementation. It is **not** a list of required patterns or a mandate to create layers. Start with product and quality requirements, existing architecture and constraints.

## Decision-first workflow

1. **Discover constraints**: users, scale/concurrency, consistency and latency, domain complexity, delivery team, deployment environments, integration topology, operations/on-call, security and privacy, observability, maintainability, fault isolation, migration/legacy and budget. Distinguish measured requirements from estimates and unresolved assumptions.
2. **Identify irreversible boundaries**: state ownership, trust boundaries, transactions, external contracts, failure modes, regulatory requirements and organizational team ownership.
3. **Propose the smallest viable design**: reuse existing architecture when suitable; avoid distributed complexity without a measurable need.
4. **Compare at least two realistic alternatives** for material design decisions on the same criteria. Include operational cost, coupling, complexity, change/reversibility and verification/test seams.
5. **Record a decision or ADR** (when material): context, constraints, options, selection, consequences, rejected alternatives, risks, linked RF/RNF/RN/UC and verification obligations. Do not label an option approved before the authorized decision maker approves it.

## Common alternatives and selection cues

| Pattern / style | Consider when | Trade-offs / warning signs |
|---|---|---|
| Simple layered application | Small cohesive system with clear UI/business/data responsibilities | Can create anemic pass-through layers; avoid layers without meaningful boundaries |
| Modular monolith | One deployable with multiple domain modules, strong transactional consistency or small operations team | Requires strict module boundaries; shared database shortcuts can erode modularity |
| Hexagonal / ports and adapters | Domain logic must be tested independent of persistence, web framework or vendors | More interfaces/adapters to maintain; apply selectively to real change seams |
| Clean architecture / dependency inversion | Long-lived core with several delivery interfaces and volatile infrastructure | Do not equate correctness with a mandated ring diagram or excessive indirection |
| Domain-Driven Design / bounded contexts | Complex business language with distinct subdomains and ownership | More modeling effort; a basic CRUD app rarely needs the full DDD toolkit |
| Microservices | Independent team/deployment/scaling/fault boundaries are demonstrated | Network latency, distributed transactions, operational cost and version drift |
| Event-driven integrations / asynchronous messaging | Loose coupling, async work, replay, integrations with natural events | Ordering, duplicate delivery, idempotency, schema evolution and eventual consistency |
| CQRS | Read and write models demonstrably need different scaling/consistency shapes | Duplication, projection lag and synchronization complexity; not default |
| Event sourcing | Audit/replay is an explicit core requirement with budget for projections and migration | High design and operational complexity; event history does not replace backups |
| Serverless / managed event functions | Event-triggered bursts and small independent workloads with provider constraints | Cold starts, platform lock-in, observability and transaction boundaries |
| MVC / component UI / frontend modules | Interface interaction and framework boundaries merit a defined structure | UI pattern does not decide domain persistence and backend architecture |
| API-first contracts | Several consumers, independent team work or versioned external integrations | Versioning and compatibility become obligations, not just endpoint definitions |

Patterns can be composed: `modular monolith + selected ports/adapters + REST` is often coherent; `microservices + event-driven` requires explicit distributed failure controls. Do not select from buzzwords or force a specific technology.

## Architectural questions tied to documents

| Decision theme | Ask about evidence and constraints, not pattern names | Document destination |
|---|---|---|
| Deployment unit | How many owners, independent release needs, scale and operations staff? | DOC-04 RNFs, DOC-11, DOC-12 |
| Module boundaries | Which business invariants and transaction boundaries change together? | DOC-05, DOC-09, DOC-11 |
| State and data | Who owns truth, consistency, migration, deletion, retention and recovery? | DOC-05, DOC-10, DOC-11, DOC-14 |
| APIs / events | Which clients, version compatibility, ordering, retries and idempotency? | DOC-04, DOC-11, DOC-13 |
| Performance / resilience | What measurable targets and failure costs exist? | DOC-04, DOC-11, DOC-16 |
| Security / tenancy | Which actors can read/change which data across trust boundaries? | DOC-04, DOC-14, DOC-16 |
| UX / frontend | Which clients, accessibility, offline behavior, navigation and error states? | DOC-06, DOC-15 |
| Delivery / observability | Who deploys, monitors, responds, rolls back and audits changes? | DOC-03, DOC-18, DOC-19, DOC-20 |

## Suggested decision record

```text
ADR-NNN: [decision title]
Status: PROPOSED | ACCEPTED | SUPERSEDED
Baseline / scope:
Driving RF/RNF/RN/UC:
Quality and operational constraints:
Alternatives: A / B [and concrete evidence]
Chosen approach and authority:
Consequences and accepted risks:
Related documents and tests:
Review/reconsideration trigger:
```

### Non-negotiable cautions

- The architecture skill recommends engineering decisions; it does **not** grant itself business/product approval or commit authority.
- A diagram without explicit APIs/data ownership/error/recovery semantics is not a sufficient implementation contract.
- Separate unverified guesses from accepted constraints. Use `technical-research` for niche or version-dependent platform claims.
- Validate risk-specific behavior (transaction integrity, permissions, retries, concurrency, backup/recovery, migration, distributed observability) with suitable tests.
- Prefer stable seams and measurable outcomes over maximal pattern adoption.
