# Ariel Agent Skills

A compact, runtime-neutral software-engineering skill ecosystem maintained by Ariel Oliveira.

The repository favors a small set of high-leverage skills over collecting every upstream idea. Skills are selected for broad reuse, clear boundaries, composability, and verifiable outcomes. Provider-specific or low-value workflows are not promoted into the core ecosystem merely because they exist upstream.

## Core engineering lifecycle

```text
objective
  ↓
project-discovery
  ↓
technical-research / domain-modeling (when needed)
  ↓
software-specification
  ↓
work-decomposition
  ↓
software-architecture
  ↓
implementation ↔ testing ↔ debugging
  ↓
code-review + security-review (+ web-frontend-design when relevant)
  ↓
integration-release
  ↓
project-handoff when crossing an execution/session boundary
```

`engineering-lifecycle` is the coordinating skill. It selects only the stages required by the task; it is not an instruction to run every skill every time.

## Skills

| Skill | Primary role | Status |
|---|---|---|
| [engineering-lifecycle](./engineering-lifecycle/) | Select and coordinate the engineering flow, including terminal obligations and recovery-aware continuity | `0.3.0` |
| [project-discovery](./project-discovery/) | Understand the real project, repository root, runtime, and environment before planning | `0.2.0` |
| [technical-research](./technical-research/) | Evidence-backed technical investigation with authority-aware runtime research | `0.2.0` |
| [domain-modeling](./domain-modeling/) | Vocabulary, invariants, scenarios, and domain decisions | `0.1.0` |
| [software-specification](./software-specification/) | Turn intent into an implementable contract | `0.1.0` |
| [work-decomposition](./work-decomposition/) | Build a dependency graph, executable frontier, remediation work, and bounded replanning | `0.3.0` |
| [software-architecture](./software-architecture/) | Boundaries, durable state, versioned contracts, correlation, and ADR-grade decisions | `0.2.0` |
| [implementation](./implementation/) | Build scoped vertical slices and bounded remediations | `0.2.0` |
| [testing](./testing/) | Risk-based verification, recovery/contract checks, and regression protection | `0.2.0` |
| [debugging](./debugging/) | Recovery-aware diagnosis, failure classification, and regression-safe fixes | `0.2.0` |
| [code-review](./code-review/) | Independent spec/standards review bound to the exact code state | `0.2.0` |
| [security-review](./security-review/) | Threat- and evidence-driven review including observability/privacy boundaries | `0.2.0` |
| [integration-release](./integration-release/) | Current-HEAD review, CI, merge, post-integration validation, release, and rollback discipline | `0.2.0` |
| [project-handoff](./project-handoff/) | Recovery-safe continuity across agents/sessions | `0.2.0` |
| [web-frontend-design](./web-frontend-design/) | Framework-neutral web UI/UX, accessibility, and semantically truthful operational dashboards | `0.3.0` |
| [adaptive-orchestrator-bridge](./adaptive-orchestrator-bridge/) | Thin OpenClaw → Adaptive invocation bridge that preserves skills and incomplete/recovery state | `0.3.0` |

### Web frontend scope

`web-frontend-design` is the general web frontend design skill. It is not a WordPress-only skill and does not select or impose a framework. It can be used with React, Vue, Angular, Svelte, server-rendered frameworks, template engines, or plain HTML/CSS/JavaScript. WordPress remains supported through a focused adapter loaded only when the target project actually uses WordPress.

## Machine-readable registry

- `registry/skills.json` is the portable skill catalog.
- `registry/capabilities.json` is the capability vocabulary used for orchestration and selection.
- Registry versions are validated against each skill's frontmatter.
- Skills that absorbed field learning may publish `execution_profile` and `learned_invariants` metadata. These fields document the responsibility/model-tier intent and the operational rules embedded directly in the corresponding `SKILL.md`; they do not replace the Adaptive runtime's authoritative model-routing policy.

## Field-learning discipline

A lesson is not considered incorporated merely because it appears in a postmortem. Operational learning should be distributed to the smallest correct layer:

- deterministic execution/recovery guarantees → orchestrator/runtime core;
- role-specific judgment and working rules → the relevant skill;
- routing/discovery metadata → the machine-readable registry;
- regression-prone behavior → executable tests;
- provenance and cross-skill rationale → concise field-learning documentation.

Do not copy every lesson into every skill. Keep each worker's context specialized to the knowledge that benefits its role.

## Validation

Run:

```bash
python3 scripts/validate_ecosystem.py
python3 web-frontend-design/scripts/validate_skill.py
```

GitHub Actions runs both classes of validation on `main`, feature branches, and pull requests.

## Design rules

- Prefer broad engineering capability over author- or provider-specific behavior.
- Keep runtime-specific mechanics in adapters, not in the skill's core contract.
- Use progressive disclosure and context pointers rather than loading every reference by default.
- Define checkable completion criteria and evidence for important claims.
- Preserve existing architecture unless the task explicitly requires changing it.
- Treat security, integrity, and explicit human authority as constraints on autonomy.
- Avoid duplicate skills when one coherent skill can absorb the useful mechanism.

The upstream evaluation and keep/discard decisions are documented in [`docs/MATT-SKILLS-EVALUATION.md`](./docs/MATT-SKILLS-EVALUATION.md).
