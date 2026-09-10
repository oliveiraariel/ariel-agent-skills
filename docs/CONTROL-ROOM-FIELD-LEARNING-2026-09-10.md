# Control Room field learning — 2026-09-10

This document records where operational lessons from the Adaptive Control Room field exercise were incorporated. It is an audit map, not the only source of behavior: role-specific rules live directly in the affected `SKILL.md` files and deterministic guarantees belong in the Adaptive core/runtime.

## Distribution map

| Field lesson | Skill(s) that absorbed it | Runtime/core implication |
|---|---|---|
| Do not stop at an intermediate gate while required work remains | `engineering-lifecycle`, `integration-release`, `project-handoff`, bridge | Track terminal obligations/checkpoints in the orchestrator |
| Reconcile an existing asynchronous execution before redispatch | `engineering-lifecycle`, `debugging`, `technical-research`, `project-handoff`, bridge | Recovery/reconciliation before duplicate dispatch |
| Wait/transport timeout is not semantic LLM failure | `engineering-lifecycle`, `debugging`, `testing` | Bounded polling and failure taxonomy |
| `REPLAN_REQUIRED` must return to planning/frontier | `engineering-lifecycle`, `work-decomposition`, `testing` | Replan loop must continue scheduling |
| Review verdict is bound to exact HEAD/code state | `code-review`, `integration-release`, `testing`, `project-handoff` | Persist/reconcile review identity against current HEAD |
| `REQUEST CHANGES` requires remediation, tests, and independent re-review | `engineering-lifecycle`, `work-decomposition`, `implementation`, `code-review`, `integration-release` | Encode review/remediation lifecycle |
| Session/search text is evidence, not authoritative terminal state | `technical-research`, `debugging`, `code-review`, `integration-release` | Runtime run state remains authoritative |
| Wrong repository/cwd or missing global PATH is environment, not code/model failure | `project-discovery`, `debugging`, `testing` | Propagate project context and resolve local environments |
| Review findings should become explicit corrective work when useful | `work-decomposition`, `implementation`, `code-review` | Preserve ownership, routing, attempts, and traceability |
| Producer/consumer event drift needs explicit contract/version testing | `software-architecture`, `testing`, `debugging` | Version event contract / contract tests |
| Operational history must survive refresh/reopen/restart | `software-architecture`, `testing`, `web-frontend-design` | Canonical durable store or reconstructable append-only log |
| Observability must not leak prompts/secrets/tokens | `security-review`, `software-architecture`, `testing` | Allowlisted event projection |
| UI must represent real runtime/domain entities, not relabel projections | `software-architecture`, `web-frontend-design` | Expose authoritative identity when product requires it |
| Unknown/empty/legacy/partial states must stay distinct | `web-frontend-design`, `testing` | Preserve event/state semantics |
| Cost/usage uncertainty must not be silently estimated/reused | `web-frontend-design`, `security-review` | Preserve actual/estimated/unknown provenance |
| Selected worker skills and incomplete Adaptive state must survive the bridge | `adaptive-orchestrator-bridge` | Bridge remains thin and does not mask core semantics |

## Model-tier intent learned from the exercise

The skill registry now records an `execution_profile` as descriptive routing metadata while the Adaptive runtime remains authoritative for actual model selection.

- High-responsibility planning, architecture, security, integration decisions, and code review: strong reasoning tier.
- Routine implementation and routine test construction: economical tier first.
- Repeatedly failing/returned or explicit code/test remediation: code-specialist tier.
- Diagnosis/research/discovery: tier depends on materiality; high-impact reasoning should use the strong tier.

The profile is intentionally not a provider lock. Skills remain runtime-neutral.

## Learning rule

A field lesson is considered incorporated only when routed to the correct layer:

1. **Core/runtime** for deterministic orchestration guarantees.
2. **Skill** for role-specific judgment and execution behavior.
3. **Registry** for discoverable capability/responsibility metadata.
4. **Tests** for regressions that should never recur silently.
5. **Documentation** only for provenance, rationale, and cross-skill mapping.

Do not copy every lesson into every worker context. Specialization is part of the learning mechanism.

## Skills versioned in this consolidation

- `engineering-lifecycle` 0.3.0
- `project-discovery` 0.2.0
- `technical-research` 0.2.0
- `work-decomposition` 0.3.0
- `software-architecture` 0.2.0
- `implementation` 0.2.0
- `testing` 0.2.0
- `debugging` 0.2.0
- `code-review` 0.2.0
- `security-review` 0.2.0
- `integration-release` 0.2.0
- `project-handoff` 0.2.0
- `web-frontend-design` 0.3.0
- `adaptive-orchestrator-bridge` 0.3.0

`domain-modeling` and `software-specification` were intentionally left unchanged because the observed Control Room incidents did not add role-specific knowledge that justified increasing their always-loaded context.
