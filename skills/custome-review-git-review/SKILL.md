---
name: custome-review-git-review
description: Run interactive annotation review loop on local diffs.
---

# Workflow: Review Git Review

## Goal

Run interactive annotation review loop on local changes.

## Process

1. Run:
   - `python3 skills/custome-review-git-review/scripts/git-review.py [base_ref]`
2. If script outputs annotation diff:
   - Interpret each annotation in context
   - Plan code updates
   - Apply updates in workspace
   - Re-run script
3. Repeat until script returns no annotation diff.
4. Report completion with summary of addressed items.

## Notes

- The script supports overlay terminals and plain editor fallback.
- Use `--clean` to remove temporary review repo when needed.
