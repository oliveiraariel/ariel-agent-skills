# Interview skill migration and acceptance

## Origin and scope

On 2026-10-10, the skill entrypoints `grilling`, `grill-me` and `grill-with-docs` were **adapted** from the MIT-licensed `oliveiraariel/mattpocock-skills-fork` (`skills/productivity/grilling`, `skills/productivity/grill-me`, `skills/engineering/grill-with-docs`) into the portable `ariel-agent-skills` ecosystem. Their general interviewing intent and decision-tree/frontier concept are retained. The implementation instructions are substantially rewritten for project-specific documentation governance, architecture comparison, human authority, stateful handoffs and runtime-neutral invocation. See [upstream license attribution](THIRD-PARTY-SKILLS-NOTICE.md).

The **authoritative** versions for this ecosystem are now located at the repository root skill directories:
- `grilling/SKILL.md` — question dependency tree, facts vs human choices, risk-aware selection and handoff.
- `grill-me/SKILL.md` — thin user-facing alias.
- `grill-with-docs/SKILL.md` — authorized, verified persistence in canonical artifacts.

Do not load both fork and main-repository copies into the same agent runtime without an explicit skill-precedence policy. This repository does not delete or install anything in the external fork or the user's OpenClaw runtime.

## Decision flow and artifacts

1. `project-discovery` establishes the baseline, authority and current project evidence.
2. `documentation-governance` identifies applicable documents and questioning coverage.
3. `grilling` asks bounded, independently answerable questions by decision dependency.
4. `grill-with-docs` persists decisions/glossary/ADRs in canonical locations, verifies paths and marks open gaps.
5. `domain-modeling`, `software-specification`, `software-architecture` consume approved decisions. The architecture skill's pattern guide permits comparison without imposing an architectural style.
6. `testing` supplies actual acceptance evidence; an interview never claims implementation verification.

## Runtime acceptance scenarios (not yet end-to-end executed)

| ID | Given | Expected behavior |
|---|---|---|
| INT-01 | Small low-risk idea with no software repository | `grill-me` routes to `grilling`, does not demand 20 files/PRD, collects only material user choices |
| INT-02 | Existing project with an approved baseline contradicting implemented code | `grill-with-docs` flags conflict, does not silently change approved requirements to match code |
| INT-03 | User asks whether microservices or modular monolith are better | Interview requests scale/team/deployment/data consistency evidence first, compares trade-offs against RNFs and links DOC-11/12 |
| INT-04 | User answers several questions and session is interrupted | Decision register contains stable Q/DEC IDs, authority, destinations, approved/open states, and next frontier; next agent need not guess |
| INT-05 | No permission or tool to write documentation | Emits explicit `NOT_PERSISTED` and a structured handoff; never claims files were saved |
| INT-06 | The system uses data on a regulated or high-risk domain | Documentation catalog raises applicable security/privacy/verification obligations regardless of project size |
| INT-07 | A technical solution question depends on unsettled domain rules | Defers the downstream question, resolves domain rule before comparing patterns |
| INT-08 | Generic non-software brainstorming interview | `grilling` remains useful without SRS, architectural standards or mandatory document persistence |

**Validation status:** these are test scenarios for future real runtime trials. Repository validators/CI check structural integration, not full interactive interviewing behavior.
