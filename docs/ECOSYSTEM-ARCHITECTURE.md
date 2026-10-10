# Engineering Skill Ecosystem Architecture

## Goal

Provide a small, reusable engineering skill set that can operate manually in a single agent session or be selected and scheduled by an external orchestrator.

## Separation of responsibilities

The skills define **how a capability is performed**. The Adaptive AI Orchestrator defines **which resource performs which Work Unit, when it may run, how dependencies advance, and how policy/evaluation gates are enforced**.

```text
User objective
   ↓
engineering-lifecycle
   ↓ capability selection
registry/skills.json
   ↓
Adaptive AI Orchestrator (optional but preferred for multi-agent work)
   ├─ Work Units + dependency graph
   ├─ frontier scheduling + claims
   ├─ authority / human-approval policy
   ├─ agent + skill + model + runtime selection
   └─ independent evaluation
   ↓
selected engineering skills
```

## Composition rule

Use the **minimum sufficient skill set**. A task does not gain quality merely by invoking more skills.

Examples:

- a well-specified one-file bug may require `debugging` + `testing` + `code-review`;
- an ambiguous new subsystem may require discovery → domain/spec → work graph → architecture → implementation/testing → review;
- web UI/UX work can add `web-frontend-design` without replacing implementation, backend, testing, or security review;
- WordPress is handled inside `web-frontend-design` through its platform adapter only when WordPress is actually present;
- a cross-session boundary can add `project-handoff` without duplicating the spec or ADRs.

## Elicitation and documented-decision boundaries

`grilling` owns the evidence-backed interview and dependent decision frontier, `grill-me` only routes an explicit user request, and `grill-with-docs` owns the **authorized and verified persistence** of decisions made during software interviews. These capabilities reuse documentation-governance's applicability rules and `software-architecture`'s [pattern decision guide](../software-architecture/references/pattern-decision-guide.md). They do not own model routing, agent dispatch, branch merge, architecture sign-off or production deployment.

For software: discovered facts → user/engineering decisions → durable decision IDs and approved status → requirements and invariants → compared architecture options → executable specification → tests. General interviews do not require software documentation. When no canonical write destination is available, the correct output is `NOT_PERSISTED` plus a durable-ready handoff, never a false claim of updated files.

## Frontend specialization boundary

`web-frontend-design` is a **framework-neutral web frontend design skill**, not a WordPress-only skill. Its core covers UI/UX, responsive behavior, accessibility, visual systems, interaction states, redesign, polish, and audits across web stacks. Platform-specific guidance is progressively disclosed through adapters. WordPress is currently the first deep adapter because its theme, block, plugin, admin, and Global Styles architecture requires dedicated implementation guidance.

The skill should therefore be selected for relevant web frontend capabilities regardless of whether the project uses React, Vue, Angular, Svelte, server-rendered templates, plain HTML/CSS/JavaScript, WordPress, or another web stack. Framework/runtime engineering concerns that are outside visual/interaction design remain the responsibility of `software-architecture`, `implementation`, `testing`, `debugging`, `code-review`, and other engineering skills.

## Documentation governance boundary

`documentation-governance` owns the **artifact system**, applicability, source precedence, interview coverage, and audit/traceability; `software-specification` owns precise behavior and acceptance, `domain-modeling` owns domain vocabulary/invariants, `software-architecture` owns design decisions/contracts, and `testing` owns executed evidence. PRD/vision expresses product direction and is not a mandatory implementable contract. The logical artifact catalog is distinct from files and must be tailored to risk. An interview answer is a proposed or approved decision only when written to a durable canonical destination; it is not automatically implementation truth.

## Runtime neutrality

No core skill assumes Claude Code, Codex, OpenClaw, a specific programming language, issue tracker, or deployment platform. Runtime adapters may map generic actions such as search, edit, test, delegate, or review onto the available toolset.

## Context economy

The ecosystem adopts progressive disclosure: load only the skill and references needed for the current branch of work. Handoffs should point to authoritative artifacts instead of copying them. Completion criteria should be checkable and evidence-backed.

## Human authority

Skills never grant themselves permission. Destructive or externally consequential actions must respect the host runtime/orchestrator policy. When a step requires credentials, irreversible migration, production mutation, or another human-only action, prepare the work and surface the checkpoint explicitly rather than simulating approval.
