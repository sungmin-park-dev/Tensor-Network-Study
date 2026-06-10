---
frontmatter-version: 1
title: TNS Models and code-space structure decision
section: court-precedents
status: accepted
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
reviewed-by: user
reviewed-at: 2026-06-10
---

# TNS Models and code-space structure decision

## Decision

TNS separates reusable model theory, project-theme work, and shared toolbox code.

Current roots:

- `Models/` for reusable model-level theory, introductions, conventions, and exact references.
- `Projects/` for project themes, short project-specific theory explanation, concrete scripts, experiments, tests, notebooks, and progress.
- `code-space/` for common reusable code and personal toolbox components.

The former root `src/` is moved under `code-space/src/`.

## Rationale

Project folders should remain focused on applying ideas: paper experiments, scripts, benchmark runs, and project-local plans. Reusable model introductions and exact references should not be trapped inside one project. Shared toolbox code should have a clear root distinct from project scripts.

## Consequences

- `Projects/1D-multi-solver-demo/README.md` links project work to reusable model theory.
- `Projects/1D-multi-solver-demo/progress/` owns project-local implementation-slice progress.
- Reusable 1D spin-chain theory moves to `Models/1d-spin-chains/`.
- Code promotion targets `code-space/`, not root `src/`.
- A future model or paper should start as an issue/plan or model note before becoming a project root.
