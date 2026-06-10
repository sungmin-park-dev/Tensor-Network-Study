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
- Keep reusable model theory in `Models/`.
- Keep shared toolbox code in `code-space/`.
- Do not create `agent-wiki/`; split agent-facing material by role.
- Do not create AAD-style `product-space/` by default. TNS `code-space/` is a local shared-toolbox root, not an AAD product-code clone.
- Keep project-local progress under the relevant project unless it coordinates repo-wide work.
- Add maps where they reduce navigation cost; do not create a map for every folder by default.
- Use `GOVERNMENT/Working-Pad/TASK-QUEUE.md` as the index for repo-wide open work.

## Stop Conditions

Stop and ask the user before:

- Moving or renaming `Models/`, `Projects/`, `Tutorials/`, or `code-space/`.
- Promoting project-local progress into repo-wide Working-Pad.
- Creating new `*-space` roots.
- Changing protected canon under `User-Constitution/` or `Court-Precedents/`.
- Rewriting root contracts such as `README.md` or `AGENTS.md` beyond the approved task.
