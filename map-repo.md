---
frontmatter-version: 1
title: Map - Tensor-Network-Study repo
section: repo-root
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# Map - Tensor-Network-Study repo

- Root navigation for the Tensor-Network-Study repository.
- `GOVERNMENT/` is the operating layer. Project knowledge stays in project/study/runtime roots.
- Do not use AAD `product-space/` or `code-space/` naming as a default for this repo.

## Contents

| Path | Role |
|---|---|
| `AGENTS.md` | Root agent entrypoint and required reading |
| `README.md` | Thin human-facing project note |
| `requirements.txt` | Root Python dependency list for study/runtime work |
| `src/` | Existing core library skeleton; keep as runtime root |
| `Tutorials/` | Study notebooks and tutorial helper code |
| `Projects/` | Official TNS project corpus: theory notes, demos, packages, tests, notebooks |
| `Projects/map-projects.md` | Agent navigation for current project roots |
| `GOVERNMENT/` | Repo-local operating layer: rules, decisions, task control, issue notes |
| `GOVERNMENT/User-Constitution/project-definition.md` | Detailed protected project definition |

## Agent Instructions

- Read `GOVERNMENT/User-Constitution/agent-brief.md` before structural work.
- Read `GOVERNMENT/Working-Pad/TASK-QUEUE.md` before choosing or continuing active tasks.
- Read `Projects/map-projects.md` before adding or reorganizing project roots.
- Preserve project-local file roles under `Projects/` unless a migration plan explicitly says otherwise.
