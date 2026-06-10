---
frontmatter-version: 1
title: TNS project corpus structure decision
section: court-precedents
status: accepted
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
reviewed-by: user
reviewed-at: 2026-06-10
---

# TNS project corpus structure decision

## Decision

`Projects/` is limited to concrete project corpus roots.

Current project roots:

- `Projects/1D-multi-solver-demo/`
- `Projects/Cluster_Ising/`

Empty topic placeholders such as old planned model folders are not part of the project corpus. Future project roots should be created only when they have an approved plan and initial content.

## Rationale

The project definition should distinguish active evidence-bearing work from possible future topics. Keeping empty placeholders under `Projects/` makes the repo look broader and more active than it is, and it blurs the boundary between project corpus and roadmap.

## Consequences

- The root `README.md` stays thin.
- Detailed project definition lives in `GOVERNMENT/User-Constitution/project-definition.md`.
- `Projects/README.md` and `Projects/map-projects.md` describe current active project roots.
- Roadmap or future-topic planning belongs in `GOVERNMENT/Working-Pad/` or a project-local `PLAN.md`, not in empty folders.
