# cc-thingz

A collection of runtime-neutral skills and sub-agent templates.

## Usage

Invoke skills directly by name (slash or dollar style, depending on your runtime UI):

- `/brainstorm` or `$brainstorm`
- `/planning-make` or `$planning-make`
- `/review-pr` or `$review-pr`
- `/thinking-root-cause` or `$thinking-root-cause`

## Public Skills

| Skill | Purpose |
|---|---|
| `brainstorm` | Explore solution approaches before implementation |
| `planning-make` | Create structured implementation plans |
| `planning-plan-review` | Review plans for correctness and scope |
| `review-pr` | Review pull requests or issues |
| `review-git-review` | Run interactive local diff annotation loops |
| `review-writing-style` | Apply concise engineering writing style |
| `thinking-dialectic` | Evaluate claims with parallel pro/con analysis |
| `thinking-root-cause` | Run structured root-cause analysis |
| `workflow-clarify` | Resolve confusion via evidence-based clarification |
| `workflow-learn` | Capture durable project learnings |
| `workflow-wrong` | Reset and re-evaluate failed direction |
| `workflow-md-copy` | Copy markdown content to clipboard |
| `workflow-txt-copy` | Copy plain text content to clipboard |

## Internal Assets

- `skills/planning-plan-review/agents/plan-review.md`
- `skills/thinking-dialectic/agents/dialectic-thesis.md`
- `skills/thinking-dialectic/agents/dialectic-antithesis.md`
- `skills/thinking-root-cause/references/*.md`

## Scripts

- `skills/planning-make/scripts/plan-annotate.py`
- `skills/review-git-review/scripts/git-review.py`

### Script checks

```bash
python3 skills/planning-make/scripts/plan-annotate.py --test
python3 skills/review-git-review/scripts/git-review.py --test
```

## Migration Map

| Legacy path | Current path |
|---|---|
| `plugins/brainstorm/skills/do/SKILL.md` | `skills/brainstorm/SKILL.md` |
| `plugins/planning/commands/make.md` | `skills/planning-make/SKILL.md` |
| `plugins/planning/agents/plan-review.md` | `skills/planning-plan-review/SKILL.md` + `skills/planning-plan-review/agents/plan-review.md` |
| `plugins/review/skills/pr/SKILL.md` | `skills/review-pr/SKILL.md` |
| `plugins/review/skills/git-review/SKILL.md` | `skills/review-git-review/SKILL.md` |
| `plugins/review/skills/writing-style/SKILL.md` | `skills/review-writing-style/SKILL.md` |
| `plugins/thinking-tools/skills/dialectic/SKILL.md` | `skills/thinking-dialectic/SKILL.md` |
| `plugins/thinking-tools/skills/root-cause-investigator/SKILL.md` | `skills/thinking-root-cause/SKILL.md` |
| `plugins/workflow/skills/clarify/SKILL.md` | `skills/workflow-clarify/SKILL.md` |
| `plugins/workflow/skills/learn/SKILL.md` | `skills/workflow-learn/SKILL.md` |
| `plugins/workflow/skills/wrong/SKILL.md` | `skills/workflow-wrong/SKILL.md` |
| `plugins/workflow/skills/md-copy/SKILL.md` | `skills/workflow-md-copy/SKILL.md` |
| `plugins/workflow/skills/txt-copy/SKILL.md` | `skills/workflow-txt-copy/SKILL.md` |

## License

MIT
