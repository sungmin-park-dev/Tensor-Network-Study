---
frontmatter-version: 1
title: Models and code-space separation
section: issue-notes/closed
issue-type: structure-cleanup
status: closed
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
---

# Models and code-space separation

## Current Agreement

TNS now separates:

- `Models/` for reusable model theory and introductions.
- `Projects/` for project-theme explanations, concrete scripts, experiments, and progress.
- `code-space/` for common reusable code and personal toolbox components.

## Changes

- Moved root `src/` to `code-space/src/`.
- Created `Models/`.
- Moved reusable 1D spin-chain model notes from `Projects/1D-multi-solver-demo/theory/` to `Models/1d-spin-chains/`.
- Rewrote `Projects/1D-multi-solver-demo/theory/README.md` as a project-local bridge to `Models/1d-spin-chains/`.

## Verification Notes

- No project-local progress file was moved into GOVERNMENT.
- Project-local scripts remain under `Projects/`.
- Reusable model notes now have a root-level `Models/` entrypoint.
