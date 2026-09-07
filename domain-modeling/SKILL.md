---
name: domain-modeling
description: Build and sharpen a software domain model by testing vocabulary, invariants, relationships, lifecycle rules, and scenarios.
license: MIT
metadata:
  author: oliveiraariel
  version: "0.1.0"
---

# Domain Modeling

Model the problem language before encoding accidental database or framework structure.

## Workflow

1. Extract candidate entities, value objects, events, actors, states, and business terms from requirements and existing behavior.
2. Challenge synonyms and overloaded terms until each important word has one operational meaning.
3. Write invariants and lifecycle rules in domain language.
4. Stress-test the model with normal, boundary, invalid, deletion, concurrency, and recovery scenarios.
5. Record unresolved decisions separately from established domain truth.
6. Update existing domain/context artifacts and ADRs rather than forking the vocabulary into a new document set.

## Completion gate

The model is ready when implementation-facing decisions can use the domain vocabulary without hidden ambiguity and the important invariants survive scenario testing.
