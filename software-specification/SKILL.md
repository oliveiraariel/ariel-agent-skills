---
name: software-specification
description: Turn product intent, project evidence, and domain decisions into an implementable software specification with checkable acceptance criteria.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Software Specification

A specification is a contract for implementation and review, not a narrative summary.

## Include

- objective and user/system outcome;
- current behavior and relevant evidence;
- scope and explicit non-goals;
- functional behavior, invariants, interfaces, data/state changes, and failure behavior when relevant;
- constraints and compatibility requirements;
- security/accessibility/performance requirements when in scope;
- checkable acceptance criteria;
- unresolved decisions that block implementation.

Interrogate unclear requirements before pretending they are settled. Prefer recommended answers grounded in project evidence.

## Completion gate

The spec is complete when a competent implementer can build the requested scope and an independent reviewer can decide whether it was implemented correctly without inventing missing requirements.
