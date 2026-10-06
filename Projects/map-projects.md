---
frontmatter-version: 1
template-version: 1
title: Map — Projects
section: projects
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-30
must-read: GOVERNMENT/Agents-Bylaws/templates/map-template.md
---

# Map — Projects

- Agent navigation for the TNS project corpus.
- Project roots should contain concrete plans, project-specific theory summaries, paper-application work, runnable scripts, benchmarks, tests, or evidence.
- Empty topic placeholders do not belong here.

## 목차

| 항목 | 역할 | 비고 |
|---|---|---|
| [[Projects/README.md\|README.md]] | Human-facing orientation for `Projects/` | Keep thin; details belong in project-local docs |
| `1D-multi-solver-demo/` | Active 1D multi-solver seam project | Theory-first, project-local progress stays inside this root |
| `Cluster_Ising/` | Cluster-Ising paper reproduction and benchmark project | Runnable package with scripts, tests, and notebooks |

## 에이전트 지침

- Read a project root's `PLAN.md` or `README.md` before editing inside it.
- Do not create empty project directories as future-topic placeholders.
- Do not move project roots into `GOVERNMENT/`.
- Link to `../Models/` for reusable model theory instead of duplicating it in each project.
- Do not promote toolbox code into `../code-space/` until project-local validation supports reuse.

## 참고 문서

- [[GOVERNMENT/Agents-Bylaws/templates/map-template\|map-template]] — map 작성 기준
