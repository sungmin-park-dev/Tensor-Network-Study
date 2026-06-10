---
frontmatter-version: 1
title: Project definition and Projects cleanup
section: issue-notes/closed
issue-type: structure-cleanup
status: closed
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# Project definition and Projects cleanup

## Current Agreement

Root `README.md` stays a thin note. Detailed project definition lives under `GOVERNMENT/User-Constitution/`.

`Projects/` should contain concrete project corpus roots, not empty topic placeholders.

## Changes

- Re-established `GOVERNMENT/User-Constitution/project-definition.md` around active corpus roots.
- Added `Projects/README.md`.
- Added `Projects/map-projects.md`.
- Removed empty untracked placeholder directories:
  - `Projects/1D_Critical_Phases/`
  - `Projects/1D_Fermi_Hubbard/`
  - `Projects/1D_Gapped_Chains/`
  - `Projects/Square_Lattice/`
  - `Projects/Toric_Code/`
  - `Projects/XXZ_Multisolver/`
  - empty generated-data placeholder directories under `Projects/Cluster_Ising/data/`

## Verification

- Confirmed tracked project corpus is `Projects/1D-multi-solver-demo/` and `Projects/Cluster_Ising/`.
- Confirmed `Projects/XXZ_Multisolver/` is already marked discarded in `Projects/1D-multi-solver-demo/PLAN.md`.
- Confirmed no tracked files under `Projects/`, `Tutorials/`, or `src/` were moved.
