---
name: implementation
description: Implement scoped software work in small vertical slices while preserving architecture, project conventions, and explicit acceptance boundaries.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Implementation

Implement the requested work, not an opportunistic rewrite.

## Workflow

1. Read the Work Unit/spec, relevant architecture, and local project instructions.
2. Identify the smallest vertical slice that can produce observable evidence.
3. Establish a test or feedback seam before risky behavior changes.
4. Implement using the project's existing conventions and dependency choices.
5. Keep unrelated refactors separate unless they are required to make the slice correct.
6. Run the relevant checks after each meaningful slice and before declaring completion.
7. Report changed behavior, evidence, and any acceptance criterion not yet verified.

## Completion gate

Implementation is done when the requested scope works through its intended interface, relevant checks pass, and no known acceptance criterion is silently deferred.
