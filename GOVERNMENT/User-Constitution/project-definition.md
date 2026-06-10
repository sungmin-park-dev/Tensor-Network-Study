---
frontmatter-version: 1
title: Tensor-Network-Study Project Definition
section: user-constitution
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# Tensor-Network-Study Project Definition

Tensor-Network-Study is a research and study repository for learning tensor-network methods through concrete theory notes, small solver experiments, paper-application projects, and validation against exact, analytical, or literature-backed references.

## Purpose

The repository exists to connect six activities:

1. Study tensor-network and many-body model foundations.
2. Write concise theory notes that can support implementation.
3. Apply new papers in concrete local experiments instead of leaving them as reading notes only.
4. Build small project-local solver or reproduction experiments.
5. Record validation evidence before promoting abstractions into shared code.
6. Gradually build a personal tensor-network and solver toolbox from repeated, validated patterns.

## Source-Of-Truth Model

The repo separates operating knowledge from project corpus.

- `GOVERNMENT/` holds project definition, operating decisions, agent procedures, and repo-wide task control.
- `Models/`, `Projects/`, `Tutorials/`, and `code-space/` hold the actual model theory, project, study, and shared-code corpus.
- Root `README.md` is intentionally thin and points to the relevant source of truth.

## Corpus Roots

| Root | Role |
|---|---|
| `Models/` | Reusable model-level theory: introductions, Hamiltonian definitions, conventions, and exact references |
| `Projects/` | Project-theme corpus: project-specific theory summaries, concrete scripts, runnable demos, benchmarks, tests, and project-local progress |
| `Tutorials/` | Study notebooks and tutorial material |
| `code-space/` | Shared code and future home for validated personal toolbox components |
| `GOVERNMENT/` | Operating layer: project definition, decisions, agent procedure, task queue, issue notes |

## Current Project Surfaces

| Surface | Role |
|---|---|
| `Projects/1D-multi-solver-demo/` | Active 1D solver-seam and theory-first demo corpus |
| `Models/1d-spin-chains/` | Reusable 1D spin-chain model definitions, conventions, and exact-solution notes |
| `Projects/1D-multi-solver-demo/theory/` | Project-local theory bridge, writing rules, and implementation-slice progress |
| `Projects/Cluster_Ising/` | Runnable Cluster-Ising paper reproduction and benchmark project |
| `Tutorials/Notebooks/` | Learning notebooks and notebook helper code |
| `code-space/src/` | Shared Python package skeleton |

## Projects Folder Policy

`Projects/` is not a topic backlog. It should contain only roots with an approved plan, project-theme explanation, runnable code, paper-application evidence, benchmark evidence, tests, or another concrete artifact.

Current active project roots:

- `Projects/1D-multi-solver-demo/`
- `Projects/Cluster_Ising/`

Future topic candidates such as additional model families or newly read papers should be captured as issue notes, roadmap notes, or project-local plans before creating a top-level project directory.

## Models Folder Policy

`Models/` owns reusable model-theory explanations and introductions. It should not contain project-local scripts, run outputs, or implementation progress.

Current model roots:

- `Models/1d-spin-chains/`

When a project needs a model explanation that could be reused elsewhere, the reusable part belongs under `Models/`; the project folder keeps the short project-specific theory bridge and concrete scripts.

## Operating Boundaries

- Root `README.md` stays a thin human-facing note.
- Detailed project definition lives here under `GOVERNMENT/User-Constitution/`.
- `Projects/` is not scratch and is not a GOVERNMENT layer.
- `Models/` is not a project execution folder.
- Project-local progress stays in the relevant project unless the user promotes it to repo-wide operations.
- `research-space/`, `study-space/`, `product-space/`, and `agent-wiki/` are not current TNS roots.
- Future root moves require a separate decision and path-reference verification.
- Empty project placeholder directories should not be kept as structural claims.
- Toolbox components should graduate to `code-space/` only after project-local experiments have produced reusable evidence.

## Non-Goals

- Do not turn this repo into an AAD-style product repo.
- Do not use root README as the full project charter.
- Do not flatten theory notes, benchmark plans, or project-local progress into Working-Pad.
- Do not promote shared abstractions or toolbox components into `code-space/` before project-local evidence justifies them.
