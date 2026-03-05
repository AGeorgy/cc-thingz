# cc-thingz

A collection of runtime-neutral skills and sub-agent templates.

This repository keeps the practical workflows from the original plugin-based setup, now as standalone skills with `aaa-*` prefixes.

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

## Skill Details

### aaa-brainstorm

Collaborative design skill that helps turn ideas into implementation-ready direction.

| Component | Trigger | Description |
|-----------|---------|-------------|
| skill | `/aaa-brainstorm` | Collaborative dialogue from idea to options to concrete plan |

Guides a 4-phase flow:

1. **Understand** - gather project context and constraints.
2. **Explore approaches** - provide 2-3 options with trade-offs and recommendation.
3. **Present design** - break solution into clear, reviewable increments.
4. **Next steps** - hand off to planning or implementation.

### aaa-review-pr / aaa-review-git-review / aaa-review-writing-style

Review and communication toolkit for code changes.

| Component | Trigger | Description |
|-----------|---------|-------------|
| skill | `/aaa-review-pr <number>` | Pull request or issue review with structured findings |
| skill | `/aaa-review-git-review [ref]` | Interactive local diff annotation loop |
| skill | `/aaa-review-writing-style` | Direct, concise engineering writing guidance |

`aaa-review-pr` focuses on code quality, architecture, test coverage, and scope creep detection.  
`aaa-review-git-review` supports iterative in-editor diff annotations and feedback loops.  
`aaa-review-writing-style` enforces brief, specific, technical communication.

Run checks:

```bash
python3 skills/aaa-review-git-review/scripts/git-review.py --test
```

### aaa-planning-make / aaa-planning-plan-review

Structured planning workflow plus plan quality review.

| Component | Trigger | Description |
|-----------|---------|-------------|
| skill | `/aaa-planning-make <desc>` | Build implementation plan with tasks, files, and tests |
| skill | `/aaa-planning-plan-review` | Review plan quality and identify risks before coding |

`aaa-planning-make` produces concrete task plans and supports iterative plan editing.  
`aaa-planning-plan-review` checks plan correctness, scope, over-engineering risk, and test coverage.

Run checks:

```bash
python3 skills/aaa-planning-make/scripts/plan-annotate.py --test
```

### aaa-thinking-dialectic / aaa-thinking-root-cause

Analytical skills for objective reasoning and fault investigation.

| Component | Trigger | Description |
|-----------|---------|-------------|
| skill | `/aaa-thinking-dialectic <statement>` | Parallel thesis/antithesis analysis |
| skill | `/aaa-thinking-root-cause` | Structured 5-Why investigation |

`aaa-thinking-dialectic` reduces confirmation bias by forcing opposing evidence collection.  
`aaa-thinking-root-cause` drills from symptoms to underlying system-level causes.

### aaa-workflow-*

Session helpers for learning capture, clarification, recovery, and clipboard workflows.

| Component | Trigger | Description |
|-----------|---------|-------------|
| skill | `/aaa-workflow-learn` | Capture reusable project knowledge |
| skill | `/aaa-workflow-clarify` | Resolve confusion via evidence and expectation checks |
| skill | `/aaa-workflow-wrong` | Reset and re-evaluate a failing approach |
| skill | `/aaa-workflow-md-copy` | Format answer as markdown and copy to clipboard |
| skill | `/aaa-workflow-txt-copy` | Copy plain text to clipboard |

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

## Credits

Some skills and scripts were influenced by community ideas, posts, and open-source examples. If you recognize your work and want explicit attribution, open an issue and it can be added.

## License

MIT
