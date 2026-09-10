---
name: software-architecture
description: Design software boundaries, interfaces, seams, data flow, and trade-offs that fit the existing project rather than a preferred stack.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Software Architecture

Prefer deep modules: small stable interfaces hiding meaningful implementation complexity. Architecture should reduce coordination cost, not maximize layers.

## Workflow

1. Start from the specification, domain invariants, and existing architecture.
2. Identify responsibilities, boundaries, dependency direction, state ownership, integration points, trust boundaries, and recovery ownership.
3. Define seams that are testable through public interfaces.
4. For producer/consumer integrations, define the event/API contract explicitly: identifiers, required/optional fields, lifecycle semantics, compatibility behavior, and contract/version ownership.
5. Separate transient transport from persistent source of truth. Operational state that must survive refresh/restart requires a canonical durable store or a reconstructable append-only history; in-memory state and disposable `/tmp` artifacts are not sufficient by themselves.
6. Compare realistic alternatives and record the trade-off that selects one.
7. Preserve established architecture unless evidence shows it blocks the requirement; avoid rewrite reflexes.
8. Record material decisions in the project's existing ADR/architecture mechanism.

## Learned operating invariants

- Producer and consumer event vocabularies must evolve together. Add contract tests or a shared/versioned schema so a newly emitted event cannot be silently dropped by the consumer.
- Correlation identifiers are part of the architecture, not incidental logging. Preserve orchestration, work, execution/run/session, attempt, and model correlation across process boundaries when the use case requires recovery or observability.
- Distinguish logical domain/UI entities from storage/event projection keys. Renaming a Work Unit card to “Agent” does not create an agent identity; model the real identity if the product promises it.
- Define authoritative state and reconstruction rules so refresh, browser reopen, or service restart does not lose durable history.
- Observability must remain a safe projection: enough metadata for diagnosis and learning without leaking raw prompts, secrets, credentials, or unnecessary sensitive payloads.

Architecture and cross-boundary contract decisions are high-responsibility work; prefer a strong reasoning tier when model routing is available.

## Completion gate

Architecture is ready when implementers know the owning module, public/versioned contracts, dependency direction, state/data flow, persistence/recovery authority, test seams, correlation semantics where required, and the risks accepted by the decision.
