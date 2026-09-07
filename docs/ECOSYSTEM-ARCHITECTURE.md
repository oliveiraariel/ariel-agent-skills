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
- frontend WordPress work can add `frontend-design-wordpress` without replacing backend/security review;
- a cross-session boundary can add `project-handoff` without duplicating the spec or ADRs.

## Runtime neutrality

No core skill assumes Claude Code, Codex, OpenClaw, a specific programming language, issue tracker, or deployment platform. Runtime adapters may map generic actions such as search, edit, test, delegate, or review onto the available toolset.

## Context economy

The ecosystem adopts progressive disclosure: load only the skill and references needed for the current branch of work. Handoffs should point to authoritative artifacts instead of copying them. Completion criteria should be checkable and evidence-backed.

## Human authority

Skills never grant themselves permission. Destructive or externally consequential actions must respect the host runtime/orchestrator policy. When a step requires credentials, irreversible migration, production mutation, or another human-only action, prepare the work and surface the checkpoint explicitly rather than simulating approval.
