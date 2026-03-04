---
name: custome-workflow-txt-copy
description: Copy plain text content to clipboard.
---

# Workflow: Workflow TXT Copy

## Goal

Copy plain text content to clipboard.

## Process

1. Determine source text.
2. Write to temporary file in `/tmp`.
3. Copy with platform tool (`pbcopy`, `xclip`, or `xsel`).
4. Remove temporary file.
5. Report success and character count.
