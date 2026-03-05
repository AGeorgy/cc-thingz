# cc-thingz

A collection of runtime-neutral skills and sub-agent templates.

## Usage

Invoke skills directly by name (slash or dollar style, depending on your runtime UI):

- `/aaa-brainstorm` or `$aaa-brainstorm`
- `/aaa-planning-make` or `$aaa-planning-make`
- `/aaa-review-pr` or `$aaa-review-pr`
- `/aaa-thinking-root-cause` or `$aaa-thinking-root-cause`

## Public Skills

| Skill | Purpose |
|---|---|
| `aaa-brainstorm` | Explore solution approaches before implementation |
| `aaa-planning-make` | Create structured implementation plans |
| `aaa-planning-plan-review` | Review plans for correctness and scope |
| `aaa-review-pr` | Review pull requests or issues |
| `aaa-review-git-review` | Run interactive local diff annotation loops |
| `aaa-review-writing-style` | Apply concise engineering writing style |
| `aaa-thinking-dialectic` | Evaluate claims with parallel pro/con analysis |
| `aaa-thinking-root-cause` | Run structured root-cause analysis |
| `aaa-workflow-clarify` | Resolve confusion via evidence-based clarification |
| `aaa-workflow-learn` | Capture durable project learnings |
| `aaa-workflow-wrong` | Reset and re-evaluate failed direction |
| `aaa-workflow-md-copy` | Copy markdown content to clipboard |
| `aaa-workflow-txt-copy` | Copy plain text content to clipboard |

## Internal Assets

- `skills/aaa-planning-plan-review/agents/plan-review.md`
- `skills/aaa-thinking-dialectic/agents/dialectic-thesis.md`
- `skills/aaa-thinking-dialectic/agents/dialectic-antithesis.md`
- `skills/aaa-thinking-root-cause/references/*.md`

## Scripts

- `skills/aaa-planning-make/scripts/plan-annotate.py`
- `skills/aaa-review-git-review/scripts/git-review.py`

### Script checks

```bash
python3 skills/aaa-planning-make/scripts/plan-annotate.py --test
python3 skills/aaa-review-git-review/scripts/git-review.py --test
```

## Migration Map

| Legacy path | Current path |
|---|---|
| `plugins/brainstorm/skills/do/SKILL.md` | `skills/aaa-brainstorm/SKILL.md` |
| `plugins/planning/commands/make.md` | `skills/aaa-planning-make/SKILL.md` |
| `plugins/planning/agents/plan-review.md` | `skills/aaa-planning-plan-review/SKILL.md` + `skills/aaa-planning-plan-review/agents/plan-review.md` |
| `plugins/review/skills/pr/SKILL.md` | `skills/aaa-review-pr/SKILL.md` |
| `plugins/review/skills/git-review/SKILL.md` | `skills/aaa-review-git-review/SKILL.md` |
| `plugins/review/skills/writing-style/SKILL.md` | `skills/aaa-review-writing-style/SKILL.md` |
| `plugins/thinking-tools/skills/dialectic/SKILL.md` | `skills/aaa-thinking-dialectic/SKILL.md` |
| `plugins/thinking-tools/skills/root-cause-investigator/SKILL.md` | `skills/aaa-thinking-root-cause/SKILL.md` |
| `plugins/workflow/skills/clarify/SKILL.md` | `skills/aaa-workflow-clarify/SKILL.md` |
| `plugins/workflow/skills/learn/SKILL.md` | `skills/aaa-workflow-learn/SKILL.md` |
| `plugins/workflow/skills/wrong/SKILL.md` | `skills/aaa-workflow-wrong/SKILL.md` |
| `plugins/workflow/skills/md-copy/SKILL.md` | `skills/aaa-workflow-md-copy/SKILL.md` |
| `plugins/workflow/skills/txt-copy/SKILL.md` | `skills/aaa-workflow-txt-copy/SKILL.md` |

## License

MIT
