---
name: custome-planning-make
description: Create structured implementation plans with concrete tasks and tests.
---

# Workflow: Planning Make

## Goal

Create a structured implementation plan file in `docs/plans/`.

## Process

1. Explore codebase context first.
2. Ask only high-impact clarifying questions.
3. Propose implementation approaches when multiple valid paths exist.
4. Produce a detailed plan with:
   - Overview and scope
   - Files/components affected
   - Step-by-step implementation tasks
   - Test strategy per task
   - Progress checklist
5. Save plan as `docs/plans/YYYYMMDD-<topic>.md`.
6. Offer optional annotation loop with:
   - `python3 skills/custome-planning-make/scripts/plan-annotate.py <plan-file>`

## Planning Rules

- Every coding task must include test updates.
- Keep tasks small, concrete, and verifiable.
- Track blockers and scope changes directly in plan file.
