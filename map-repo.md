---
frontmatter-version: 1
template-version: 1
title: Map — Tensor-Network-Study repo
section: repo-root
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-30
must-read: GOVERNMENT/Agents-Bylaws/templates/map-template.md
---

# Map — Tensor-Network-Study repo

- Root navigation for the Tensor-Network-Study repository.
- `GOVERNMENT/` is the operating layer. Project knowledge stays in project/study/runtime roots.
- Do not use AAD `product-space/` semantics as a default for this repo; TNS `code-space/` is the local shared-toolbox root.

## 목차

| 항목 | 역할 |
|---|---|
| [[AGENTS.md\|AGENTS.md]] | Root agent entrypoint and required reading |
| [[README.md\|README.md]] | Thin human-facing project note |
| [[requirements.txt\|requirements.txt]] | Root Python dependency list for study/runtime work |
| `Tutorials/` | Study notebooks and tutorial helper code |
| `Models/` | Reusable model theory, introductions, conventions, and exact references |
| `Projects/` | Project-theme corpus: short theory bridge, demos, scripts, tests, notebooks |
| `code-space/` | Shared code and personal toolbox components |
| `GOVERNMENT/` | Repo-local operating layer: rules, decisions, task control, issue notes |

### Remarks

Nested navigation belongs in the relevant child README or map, such as `Projects/map-projects.md`, `Models/map-models.md`, or `GOVERNMENT/README.md`.

## 에이전트 지침

- Read `GOVERNMENT/User-Constitution/agent-brief.md` before structural work.
- Read `GOVERNMENT/Working-Pad/TASK-QUEUE.md` before choosing or continuing active tasks.
- Preserve project-local file roles under `Projects/` unless a migration plan explicitly says otherwise.

## 참고 문서

- [[GOVERNMENT/Agents-Bylaws/templates/map-template\|map-template]] — map 작성 기준
