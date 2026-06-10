---
frontmatter-version: 1
title: Template - issue note
section: agents-bylaws/templates
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# Template - issue note

Use issue notes for active repo-wide problems, migration plans, reviews, or unresolved discussions.

```markdown
---
frontmatter-version: 1
title: [Issue title]
section: issue-notes/open
issue-type: [migration-plan|review|bug|discussion]
status: draft
last-edited-by: codex
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# [Issue title]

## Current Agreement

## Scope And Non-Goals

## Evidence

## Plan

## Approval Needed

## Verification

## Rollback Or Close Conditions
```

Every active issue note should have a row in `GOVERNMENT/Working-Pad/TASK-QUEUE.md` and an entry in `GOVERNMENT/Working-Pad/issue-notes/map-issue-notes.md`.
