---
name: aaa-review-pr
description: Perform pull request or issue review with quick or deep analysis.
---

# Workflow: Review PR

## Goal

Perform structured pull request or issue review with optional deep analysis.

## Process

1. Determine target type (pull request vs issue).
2. Pull metadata, discussion context, and merge/check status.
3. Ask review depth when appropriate:
   - Full review (deep analysis)
   - Quick review (diff-only)
4. Full review path:
   - Create isolated worktree
   - Delegate analysis to sub-agent
   - Collect findings, validation status, and open questions
5. Quick review path:
   - Read diff and summarize scope
   - Flag obvious issues
6. Draft comment only when user asks to proceed.
7. Before posting, avoid duplicating feedback already posted by the same reviewer.
8. Clean up temporary worktree artifacts at the end.

## Requirements

- Include file:line references for technical findings.
- Highlight unrelated scope creep separately from core changes.
