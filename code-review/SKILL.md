---
name: code-review
description: Independently review a software change against both the originating specification and the repository's engineering standards.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Code Review

Review from a fixed diff/base point. Keep **Spec** and **Standards** as independent axes so one does not bias the other.

## Spec axis

Verify each acceptance obligation against the implementation and tests. Missing required behavior is a finding even when the code is elegant.

## Standards axis

Check correctness, maintainability, architecture boundaries, error handling, naming, duplication, test quality, performance risks, and repository-specific standards. Prefer concrete evidence over stylistic preference.

## Verdict

Classify findings by severity and location. Distinguish blocker, required revision, conditional acceptance, and accepted outcomes. Do not interpret an unrun required review as acceptance.

## Completion gate

Review is complete when both required axes have explicit evidence and verdicts and every blocking finding points to a reproducible or inspectable reason.
