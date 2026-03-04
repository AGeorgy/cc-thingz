---
name: custome-planning-plan-review
description: Review implementation plans for correctness, scope, and quality risks.
---

# Workflow: Planning Plan Review

## Goal

Review an implementation plan before execution and identify risk, gaps, and over-engineering.

## Process

1. Identify target plan under `docs/plans/`.
2. Delegate deep review to `agents/plan-review.md` using `spawn_agent`.
3. Present findings by severity:
   - Critical
   - Important
   - Minor
4. Give explicit verdict:
   - APPROVE
   - NEEDS REVISION
5. If revision is needed, list top priority fixes.
