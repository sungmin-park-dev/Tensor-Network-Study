---
frontmatter-version: 1
title: TNS GOVERNMENT migration policy
section: agents-bylaws/policies
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# TNS GOVERNMENT migration policy

## Rules

- Treat `Projects/` as official project corpus and keep it separate from GOVERNMENT.
- Keep root `README.md` thin. Put detailed project definition in `GOVERNMENT/User-Constitution/project-definition.md`.
- Do not create `agent-wiki/`; split agent-facing material by role.
- Do not create AAD-style `product-space/` or `code-space/` by default.
- Keep existing runtime roots such as `src/` unless a later approved plan moves them.
- Keep project-local progress under the relevant project unless it coordinates repo-wide work.
- Add maps where they reduce navigation cost; do not create a map for every folder by default.
- Use `GOVERNMENT/Working-Pad/TASK-QUEUE.md` as the index for repo-wide open work.

## Stop Conditions

Stop and ask the user before:

- Moving or renaming `Projects/`, `Tutorials/`, or `src/`.
- Promoting project-local progress into repo-wide Working-Pad.
- Creating new `*-space` roots.
- Changing protected canon under `User-Constitution/` or `Court-Precedents/`.
- Rewriting root contracts such as `README.md` or `AGENTS.md` beyond the approved task.
