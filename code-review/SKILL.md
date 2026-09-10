---
name: code-review
description: Independently review a software change against both the originating specification and the repository's engineering standards.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.2.0"
---

# Code Review

Review from a fixed diff/base point. Keep **Spec** and **Standards** as independent axes so one does not bias the other.

## Review identity

Bind every review to the exact code state inspected: repository, base/head or commit SHA, and relevant specification version. A verdict does not automatically transfer to a later HEAD.

If the reviewed code changes materially after the verdict, mark the prior review stale/superseded and perform a fresh independent review of the new code state before using the verdict as a merge/release gate.

## Spec axis

Verify each acceptance obligation against the implementation and tests. Missing required behavior is a finding even when the code is elegant.

## Standards axis

Check correctness, maintainability, architecture boundaries, error handling, naming, duplication, test quality, performance risks, clean-code/SOLID concerns where material, and repository-specific standards. Prefer concrete evidence over stylistic preference.

## Verdict and remediation lifecycle

Classify findings by severity and location. Distinguish blocker, required revision, conditional acceptance, and accepted outcomes.

Learned rules:

- Do not interpret an unrun, timed-out, still-running, or unreconciled required review as acceptance.
- `REQUEST CHANGES`/required revision blocks the corresponding integration gate until the findings are remediated, relevant tests pass, and the corrected HEAD receives a new independent review.
- Do not reuse an `APPROVE` text fragment recovered from search/history when the authoritative review/run is still active or refers to an older HEAD.
- Produce findings in a structured form suitable for corrective Work Units: severity, location, evidence, required change, and verification expectation.
- A reviewer should not implement its own required fixes unless the workflow explicitly assigns a separate implementation role; preserve independence between author/remediator and final reviewer when required by the project.

Code review is high-responsibility analytical work. When model routing supports tiers, use the strongest reasoning/review tier rather than downgrading required independent review to an economical implementation tier.

## Completion gate

Review is complete when both required axes have explicit evidence, the verdict is bound to the exact reviewed code state, every blocking finding points to a reproducible or inspectable reason, and the workflow can determine unambiguously whether remediation/re-review is still required.
