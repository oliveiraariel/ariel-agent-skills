# WIP Preservation — Incident Learning Dissemination

**Status:** protected work in progress  
**Owner directive date:** 2026-09-14  
**Related Adaptive issue:** oliveiraariel/adaptive-ai-orchestrator#38  
**Draft PR:** #14

## Owner directive

The incident-learning dissemination changes in this repository are intentionally
unfinished and synchronized with the Adaptive Incident / Investigation lifecycle work.

Until the repository owner explicitly asks the orchestrator to resume, redesign,
finalize, or remove this capability, agents and automated maintenance must not delete,
revert, rename, or semantically rewrite these incident-related changes as cleanup.

Reading, validation and reporting are allowed. If unrelated work conflicts with these
changes, surface the conflict instead of silently removing them.

## Why these changes exist

These Skill updates make reusable Skills aware of Adaptive incident boundaries while
keeping lifecycle ownership in Adaptive core. They are also preparation for a future
Investigation Skill/capability tracked by Adaptive Issue #38.

The Investigation Skill itself has **not** been created yet.

## Protected WIP file

~~~text
ariel-agent-skills/
└── WIP-INCIDENT-LEARNING-PRESERVATION.md
~~~

## Existing Skill files with protected incident-related changes

~~~text
adaptive-orchestrator-bridge/SKILL.md
debugging/SKILL.md
engineering-lifecycle/SKILL.md
project-discovery/SKILL.md
project-handoff/SKILL.md
registry/skills.json
security-review/SKILL.md
software-architecture/SKILL.md
technical-research/SKILL.md
testing/SKILL.md
~~~

These files are not globally frozen. Only the incident/result-lifecycle changes
introduced by Draft PR #14 are protected by this directive.

## Resume condition

Resume or consolidate this work only when the repository owner explicitly directs the
orchestrator to continue/finalize Adaptive Issue #38 and the related Investigation
Skill/capability.

Start by reading Adaptive Issue #38, Adaptive Draft PR #39, this file, and Draft PR #14.
