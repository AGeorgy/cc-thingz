# AGENTS

Repository conventions for skill and sub-agent authoring.

## Scope

- Skills are exposed individually under `skills/<skill-name>/SKILL.md`.
- Sub-agent templates stay adjacent to the owning skill under `agents/`.
- Supporting references stay adjacent to the owning skill under `references/`.

## Language Policy

- Keep all skill and agent text runtime-neutral.
- Use generic terms: `assistant`, `sub-agent`, `planner`, `reviewer`, `workspace`.
- Avoid vendor-specific names in skill logic and agent prompts.

## Execution Policy

- Use `request_user_input` only when ambiguity affects execution.
- Use `spawn_agent`, `send_input`, and `wait` for delegated analysis.
- Use `update_plan` for multi-step execution tracking.
- Prefer non-destructive commands unless explicit approval is provided.

## Quality Standards

- Reviews are findings-first with concrete file references.
- Plans include task-level testing requirements.
- Prefer simple, maintainable solutions over speculative abstractions.
- Scripts fail clearly with actionable errors.

## Maintenance Checklist

1. Add new capability as a dedicated skill folder under `skills/`.
2. Add local scripts/references only when required.
3. Update `README.md` skill list and migration map.
4. Run script checks before completing changes.
