# cc-thingz

A collection of runtime-neutral skills and sub-agent templates.

## Usage

Invoke skills directly by name (slash or dollar style, depending on your runtime UI):

- `/custome-brainstorm` or `$custome-brainstorm`
- `/custome-planning-make` or `$custome-planning-make`
- `/custome-review-pr` or `$custome-review-pr`
- `/custome-thinking-root-cause` or `$custome-thinking-root-cause`

## Public Skills

| Skill | Purpose |
|---|---|
| `custome-brainstorm` | Explore solution approaches before implementation |
| `custome-planning-make` | Create structured implementation plans |
| `custome-planning-plan-review` | Review plans for correctness and scope |
| `custome-review-pr` | Review pull requests or issues |
| `custome-review-git-review` | Run interactive local diff annotation loops |
| `custome-review-writing-style` | Apply concise engineering writing style |
| `custome-thinking-dialectic` | Evaluate claims with parallel pro/con analysis |
| `custome-thinking-root-cause` | Run structured root-cause analysis |
| `custome-workflow-clarify` | Resolve confusion via evidence-based clarification |
| `custome-workflow-learn` | Capture durable project learnings |
| `custome-workflow-wrong` | Reset and re-evaluate failed direction |
| `custome-workflow-md-copy` | Copy markdown content to clipboard |
| `custome-workflow-txt-copy` | Copy plain text content to clipboard |

## Internal Assets

- `skills/custome-planning-plan-review/agents/plan-review.md`
- `skills/custome-thinking-dialectic/agents/dialectic-thesis.md`
- `skills/custome-thinking-dialectic/agents/dialectic-antithesis.md`
- `skills/custome-thinking-root-cause/references/*.md`

## Scripts

- `skills/custome-planning-make/scripts/plan-annotate.py`
- `skills/custome-review-git-review/scripts/git-review.py`

### Script checks

```bash
python3 skills/custome-planning-make/scripts/plan-annotate.py --test
python3 skills/custome-review-git-review/scripts/git-review.py --test
```

## Migration Map

| Legacy path | Current path |
|---|---|
| `plugins/brainstorm/skills/do/SKILL.md` | `skills/custome-brainstorm/SKILL.md` |
| `plugins/planning/commands/make.md` | `skills/custome-planning-make/SKILL.md` |
| `plugins/planning/agents/plan-review.md` | `skills/custome-planning-plan-review/SKILL.md` + `skills/custome-planning-plan-review/agents/plan-review.md` |
| `plugins/review/skills/pr/SKILL.md` | `skills/custome-review-pr/SKILL.md` |
| `plugins/review/skills/git-review/SKILL.md` | `skills/custome-review-git-review/SKILL.md` |
| `plugins/review/skills/writing-style/SKILL.md` | `skills/custome-review-writing-style/SKILL.md` |
| `plugins/thinking-tools/skills/dialectic/SKILL.md` | `skills/custome-thinking-dialectic/SKILL.md` |
| `plugins/thinking-tools/skills/root-cause-investigator/SKILL.md` | `skills/custome-thinking-root-cause/SKILL.md` |
| `plugins/workflow/skills/clarify/SKILL.md` | `skills/custome-workflow-clarify/SKILL.md` |
| `plugins/workflow/skills/learn/SKILL.md` | `skills/custome-workflow-learn/SKILL.md` |
| `plugins/workflow/skills/wrong/SKILL.md` | `skills/custome-workflow-wrong/SKILL.md` |
| `plugins/workflow/skills/md-copy/SKILL.md` | `skills/custome-workflow-md-copy/SKILL.md` |
| `plugins/workflow/skills/txt-copy/SKILL.md` | `skills/custome-workflow-txt-copy/SKILL.md` |

## License

MIT
