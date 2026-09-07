---
name: testing
description: Design and execute risk-based software verification with reproducible evidence, appropriate test layers, and regression protection.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Testing

Choose the cheapest test layer that can reliably detect the failure being guarded against.

## Workflow

1. Derive test obligations from acceptance criteria, invariants, prior defects, trust boundaries, and failure cost.
2. Use red-green-refactor when a deterministic seam exists and the loop improves design or defect isolation; do not force it for every task.
3. Cover behavior at the appropriate mix of unit, integration, contract, end-to-end, static, and manual verification.
4. Exercise important boundaries: invalid input, empty state, concurrency/retry, permissions, error recovery, migration/compatibility, and content extremes when relevant.
5. Make failures reproducible and assertions diagnostic.
6. Record what was actually run and what remains unverified.

## Completion gate

Testing is sufficient when material acceptance and regression risks have evidence at an appropriate layer and remaining gaps are explicit rather than implied away.
