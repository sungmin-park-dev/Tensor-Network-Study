---
frontmatter-version: 1
title: TNS GOVERNMENT migration decision
section: court-precedents
status: accepted
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
reviewed-by: user
reviewed-at: 2026-06-10
---

# TNS GOVERNMENT migration decision

## Decision

Tensor-Network-Study adopts a repo-local `GOVERNMENT/` operating layer while preserving existing project corpus roots.

Accepted boundaries:

- `Projects/` is official TNS project corpus and stays separate from `GOVERNMENT/`.
- `Tutorials/` remains the study notebook root unless a later plan moves it.
- At initial bootstrap, `src/` remained the runtime root. This code-layout boundary is superseded by
  `tns-models-code-space-structure-2026-06.md`, which moves shared code under `code-space/src/`.
- Root `README.md` stays a thin note; detailed project definition lives under `GOVERNMENT/User-Constitution/project-definition.md`.
- AAD `product-space/` and `code-space/` semantics are not copied into TNS by default.
- `agent-wiki/` is not created. Agent knowledge is split across `AGENTS.md`, `agent-brief.md`, `Agents-Bylaws/`, maps, and Working-Pad.

## Rationale

TNS is a research/study repo, not a software-product repo. Its long-lived project knowledge lives in
project, study, model, and shared-code roots rather than inside `GOVERNMENT/`. GOVERNMENT should manage
operating rules, task flow, decisions, and agent procedure without flattening project-local lifecycle notes
into repo-wide task control.

## Consequences

- Project-local notes such as `Projects/1D-multi-solver-demo/progress/open/` are not automatically moved into `GOVERNMENT/Working-Pad/`.
- Future additional `*-space` roots such as `research-space/` or `study-space/` require a separate decision.
- Physical movement of project files requires path-reference checks and runtime verification.
