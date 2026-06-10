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

Tensor-Network-Study is a research and study repository for learning tensor-network methods through concrete theory notes, small solver experiments, and validation against exact, analytical, or literature-backed references.

## Purpose

The repository exists to connect four activities:

1. Study tensor-network and many-body model foundations.
2. Write concise theory notes that can support implementation.
3. Build small project-local solver or reproduction experiments.
4. Record validation evidence before promoting abstractions into shared code.

## Source-Of-Truth Model

The repo separates operating knowledge from project corpus.

- `GOVERNMENT/` holds project definition, operating decisions, agent procedures, and repo-wide task control.
- `Projects/`, `Tutorials/`, and `src/` hold the actual research/study/runtime corpus.
- Root `README.md` is intentionally thin and points to the relevant source of truth.

## Corpus Roots

| Root | Role |
|---|---|
| `Projects/` | Official project corpus: concrete plans, theory notes, runnable research demos, benchmarks, tests, and project-local progress |
| `Tutorials/` | Study notebooks and tutorial material |
| `src/` | Existing root runtime package skeleton |
| `GOVERNMENT/` | Operating layer: project definition, decisions, agent procedure, task queue, issue notes |

## Current Project Surfaces

| Surface | Role |
|---|---|
| `Projects/1D-multi-solver-demo/` | Active 1D solver-seam and theory-first demo corpus |
| `Projects/1D-multi-solver-demo/theory/` | Model definitions, conventions, exact-solution notes, writing rules, and project-local progress |
| `Projects/Cluster_Ising/` | Runnable Cluster-Ising paper reproduction and benchmark project |
| `Tutorials/Notebooks/` | Learning notebooks and notebook helper code |

## Projects Folder Policy

`Projects/` is not a topic backlog. It should contain only roots with an approved plan, runnable code, theory corpus, benchmark evidence, tests, or another concrete artifact.

Current active project roots:

- `Projects/1D-multi-solver-demo/`
- `Projects/Cluster_Ising/`

Future topic candidates such as additional model families should be captured as issue notes, roadmap notes, or project-local plans before creating a top-level project directory.

## Operating Boundaries

- Root `README.md` stays a thin human-facing note.
- Detailed project definition lives here under `GOVERNMENT/User-Constitution/`.
- `Projects/` is not scratch and is not a GOVERNMENT layer.
- Project-local progress stays in the relevant project unless the user promotes it to repo-wide operations.
- `research-space/`, `study-space/`, `product-space/`, `code-space/`, and `agent-wiki/` are not current TNS roots.
- Future root moves require a separate decision and path-reference verification.
- Empty project placeholder directories should not be kept as structural claims.

## Non-Goals

- Do not turn this repo into an AAD-style product repo.
- Do not use root README as the full project charter.
- Do not flatten theory notes, benchmark plans, or project-local progress into Working-Pad.
- Do not promote shared abstractions into `src/` before project-local evidence justifies it.
