---
name: technical-research
description: Resolve technical uncertainty with primary sources, explicit evidence quality, and bounded experiments when documentation alone is insufficient.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Technical Research

Use for questions that materially affect architecture, implementation, compatibility, security, or tool choice.

## Workflow

1. Write the question and decision it informs.
2. Prefer primary/vendor/specification sources; use secondary discussion to discover edge cases, not as sole authority for critical claims.
3. Track version/date when behavior can change.
4. Distinguish sourced fact, observation, inference, and recommendation.
5. If evidence remains ambiguous, build the smallest disposable experiment that can falsify a competing hypothesis. Do not turn the prototype into production by accident.
6. Record findings with source pointers and remaining uncertainty.

## Completion gate

Research is complete when the decision owner can see the evidence, its freshness and limits, the recommended action, and what would invalidate that recommendation.
