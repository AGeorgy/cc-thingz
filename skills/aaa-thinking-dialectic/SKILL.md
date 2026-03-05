---
name: aaa-thinking-dialectic
description: Analyze a claim with parallel thesis/antithesis evidence.
---

# Workflow: Thinking Dialectic

## Goal

Stress-test a claim with parallel pro and con analysis, then synthesize verified conclusion.

## Process

1. Spawn two sub-agents in parallel:
   - Thesis (`agents/dialectic-thesis.md`)
   - Antithesis (`agents/dialectic-antithesis.md`)
2. Wait for both results.
3. Synthesize shared facts, conflicts, and unresolved uncertainty.
4. Verify cited evidence directly in repository files before final conclusion.

## Requirements

- Evidence must include concrete paths and lines where applicable.
- Final conclusion must reflect verified evidence, not just agent assertions.
