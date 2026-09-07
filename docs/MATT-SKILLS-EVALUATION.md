# Matt Pocock Skills Evaluation and Keep/Discard Decisions

Baseline evaluated: `oliveiraariel/mattpocock-skills-fork` on 2026-09-07.

## Decision rule

Do not port skills by category or popularity. Keep a mechanism only when it improves broad software-engineering capability, can be made runtime-neutral, and does not create a redundant skill boundary.

## Deprecated

Discard as a source category. The upstream `skills/deprecated` bucket is intentionally empty; its README states that retired skills are deleted and the removing changeset names the replacement. There is therefore no deprecated skill implementation to preserve.

## Engineering skills

These provided most of the reusable value.

- `grill-with-docs` → absorbed into `project-discovery`, `domain-modeling`, and `software-specification`: persistent questioning is useful; Matt-specific setup is not.
- `triage` → absorbed into `engineering-lifecycle`: role/state movement is useful where a tracker exists, but not universal enough for a standalone core skill.
- `to-spec` → `software-specification`.
- `to-tickets` + `wayfinder` → `work-decomposition`: tracer bullets, explicit blocking edges, decision work, and frontier thinking are retained without assuming a specific issue tracker.
- `implement` + `tdd` → `implementation` + `testing`: vertical slices and pre-agreed test seams are retained.
- `prototype` → absorbed into `technical-research` as a bounded experiment for uncertainty reduction.
- `diagnosing-bugs` → `debugging`: red feedback loop, minimize, hypothesize, instrument, fix, regression-test retained.
- `research` → `technical-research`: primary-source evidence retained; background-agent requirement removed.
- `domain-modeling` → `domain-modeling`.
- `codebase-design` + `improve-codebase-architecture` → `software-architecture`: deep modules, seams, and improvement analysis retained without HTML-report requirements.
- `code-review` → `code-review`: independent Spec and Standards axes retained and generalized.
- `resolving-merge-conflicts` → `integration-release`: resolve by intent and source evidence retained; blanket `never abort` behavior is not adopted.
- `wizard` → absorbed into `integration-release`/orchestrator human-action policy: preparing human-only steps is valuable, but a standalone bash-wizard generator is too narrow.
- `ask-matt` → discarded. It is author-specific routing; `engineering-lifecycle` replaces the useful routing function.
- `setup-matt-pocock-skills` → discarded. It configures Matt's own ecosystem and issue-tracker conventions rather than a general engineering capability.

## Productivity and rare-use skills

- `handoff` → retained as `project-handoff`: compact pointer-based continuity and redaction are high leverage even if used intermittently.
- `writing-for-agents` → retained as **repository design rules and validator philosophy**, not a user-facing core skill. Its context pointers, progressive disclosure, completion criteria, and single-source-of-truth ideas improve every skill.
- `grill-me` / `grilling` → useful questioning mechanics absorbed into discovery/specification; separate skills would duplicate the core flow.
- `teach`, `to-questionnaire`, `wait-what` → discarded from the engineering core. They are useful personal/productivity behaviors but not necessary for software-delivery orchestration.

## Misc

- `git-guardrails-claude-code` → do not port as a skill. The useful principle (authority checks before destructive side effects) is already implemented more generally in the Adaptive AI Orchestrator execution-policy boundary.
- `setup-pre-commit` → do not port. It is a JavaScript/Husky-specific setup recipe; generic pre-commit/CI verification belongs inside implementation/testing decisions when the project stack supports it.
- `migrate-to-shoehorn` → discarded as product-specific migration behavior.
- `scaffold-exercises` → discarded as teaching-content tooling, outside the engineering core.

## In-progress

In-progress status was treated as a warning, not an automatic rejection.

- `implement-spec` → mechanism retained primarily in the Adaptive AI Orchestrator: task graph, frontier, parallel execution, isolation/ownership, fan-in, and final review substantially improved the orchestrator design. It is not copied as a Claude-specific skill.
- `retro` → its strongest ideas (navigation pointers, automated checks, tool economy, no-op pruning) are retained as ecosystem maintenance principles rather than a separate runtime skill.
- `claude-handoff` → discarded as runtime-specific duplication of the more general handoff concept.
- `loop-me` → discarded from this software-engineering core; it specifies personal-life workflows rather than software delivery.
- `setup-ts-deep-modules` → discarded as TypeScript-specific setup.
- `writing-beats`, `writing-fragments`, `writing-shape` → discarded as writing workflow experiments outside this repository's purpose.

## Result

The resulting ecosystem intentionally has fewer skills than the upstream source. Reuse occurred at the **mechanism level**, not by cloning directories. This reduces overlap, runtime coupling, invocation ambiguity, and maintenance cost while retaining the strongest engineering ideas.
