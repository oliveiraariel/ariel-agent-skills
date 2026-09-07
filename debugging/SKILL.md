---
name: debugging
description: Diagnose difficult defects and performance regressions with a reproducible red loop, competing hypotheses, instrumentation, and regression-safe fixes.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Debugging

Do not start with the fix. Start with a feedback loop that reliably goes red on the defect.

## Loop

1. Reproduce and define the failure precisely.
2. Minimize the reproducer without losing the failure.
3. Generate competing hypotheses and rank them by explanatory power and test cost.
4. Instrument or inspect the system to falsify hypotheses.
5. Change the smallest causal surface supported by evidence.
6. Verify the loop turns green.
7. Add regression protection at the lowest reliable layer and run adjacent checks.

## Completion gate

Debugging is complete when the root cause is evidence-backed, the original reproduction no longer fails for the right reason, and a regression check protects the causal behavior.
