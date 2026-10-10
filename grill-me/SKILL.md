---
name: grill-me
description: User-facing entry point for guided decision interviews that routes to grilling and optional software documentation standards.
license: MIT
metadata:
  author: oliveiraariel
  version: "1.0.0"
---

# Grill Me

This is a **thin entry point** for users who say "grill me", "/grill-me", or request a rigorous interrogation of an idea or design.

- Select the existing `grilling` capability in the active runtime and follow its complete workflow. If the runtime cannot load another skill automatically, read `../grilling/SKILL.md` directly and apply it. Do **not** assume a proprietary "Skill" tool exists.
- Preserve generic, non-software interview behavior; do not impose software deliverables on unrelated decisions.
- When planning software, the `grilling` skill reads documentation governance and architectural decision references according to scope, risk and dependencies. Do not add a second questionnaire or fork the question policy here.
- If the user explicitly asks for persistent documents, use `grill-with-docs` instead of silently claiming `grill-me` created files.
- Respect existing canonical decisions, user approval, and write authority. Never execute a plan just because the interview ended.

**Done:** the user is in the correct interview workflow and understands whether the result is an in-chat decision handoff or persisted project documentation.
