---
name: aaa-workflow-md-copy
description: Format content as markdown and copy to clipboard.
---

# Workflow: Workflow MD Copy

## Goal

Format generated content as markdown and copy it to clipboard.

## Process

1. Build final markdown content.
2. Write to temporary file in `/tmp`.
3. Copy with platform tool (`pbcopy`, `xclip`, or `xsel`).
4. Remove temporary file.
5. Report success and character count.
