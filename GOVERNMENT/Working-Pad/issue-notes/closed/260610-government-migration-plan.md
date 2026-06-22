---
frontmatter-version: 1
title: Tensor-Network-Study GOVERNMENT migration plan
section: issue-notes/closed
issue-type: migration-plan
status: closed
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-10
source-skill: /Users/david/GitHub/ai-automation-dashboard/GOVERNMENT/Agents-Bylaws/skills/government-migration/SKILL.md
---

# Tensor-Network-Study GOVERNMENT migration plan

## Current Agreement

Mode: **fresh migration + baseline gate**.

Initial request scope was plan-only. After reviewing the plan, the user approved proceeding. Initial bootstrap execution is complete.

Still true:

- No project source files are moved.
- No `research-space/`, `study-space/`, `product-space/`, or `code-space/` roots are created.
- `Projects/`, `Tutorials/`, and `src/` remain in place.
- Project-local lifecycle notes are not absorbed into repo-wide Working-Pad.

The requested output path was:

```text
GOVERNMENT/Working-Pad/issue-notes/open/260610-government-migration-plan.md
```

At session start this path did not exist because the repo had no `GOVERNMENT/` root. The plan was created there first, then moved to:

```text
GOVERNMENT/Working-Pad/issue-notes/closed/260610-government-migration-plan.md
```

after initial bootstrap completion.

Current physical state after initial bootstrap:

- `GOVERNMENT/README.md` exists.
- `GOVERNMENT/Working-Pad/TASK-QUEUE.md`, `map-working-pad.md`, and `issue-notes/map-issue-notes.md` exist.
- `GOVERNMENT/User-Constitution/agent-brief.md` and map exist.
- `GOVERNMENT/Court-Precedents/tns-government-migration-2026-06.md` and map exist.
- `GOVERNMENT/Agents-Bylaws/` has a TNS migration policy and two local templates.
- Root `AGENTS.md` and `map-repo.md` exist as thin entrypoints.
- Current `git status --short --untracked-files=all` should show the initial GOVERNMENT/root entrypoint changes plus the README update.

### T0 Corpus Boundary

T0 is a **corpus-boundary gate**, not an importance test.

`Projects/` contains important project knowledge: research demos, theory notes, solver plans, benchmarks, and project-local progress. Its role is different from `GOVERNMENT/`, which should hold operating policy, task control, handoff, and decisions.

Pre-plan snapshot on 2026-06-10:

```bash
git status --short
git status --porcelain=v1 -uall -- Projects
git ls-files Projects
```

Observed result:

- `git status --short`: clean before this plan file was created
- `git status --porcelain=v1 -uall -- Projects`: no output
- `git ls-files Projects`: tracked files under `Projects/1D-multi-solver-demo/` and `Projects/Cluster_Ising/`

Therefore the old dry-run warning "`Projects/` untracked tree" is not true for this checkout at the Git-status level. That does **not** make `Projects/` less important. T0 remains a user decision about corpus boundaries:

| Option | Meaning | Default proposal |
|---|---|---|
| Include | Treat `Projects/` as official TNS project corpus, separate from GOVERNMENT operating files | Yes; keep it in place |
| Commit first | If a future checkout shows untracked `Projects/` content, commit or otherwise baseline it before migration execution | Yes if untracked content appears |
| Separate | Treat some `Projects/` content as scratch or external material outside the migration corpus | Only if the user identifies such content |

No scaffold or move may start until the user accepts the T0 boundary for the active checkout. The proposed boundary is: keep `Projects/` as official project corpus, do not absorb it into `GOVERNMENT/`, and do not rename it before a separate user decision.

## Source Boundary

AAD source repo:

```text
/Users/david/GitHub/ai-automation-dashboard
branch: restructure/aad-identity
```

Read as source pattern:

| Priority | Source | Role in this plan |
|---:|---|---|
| 1 | `GOVERNMENT/Agents-Bylaws/skills/government-migration/SKILL.md` v0.2.4 | Governing migration procedure, User-Confirmed Mode, baseline gate, stop conditions, plan contract |
| 2 | `GOVERNMENT/Court-Precedents/government-product-code-space-structure-2026-06.md` | Current AAD decision; also records that AAD `product-space`/`code-space` is AAD-specific |
| 3 | `GOVERNMENT/Agents-Bylaws/policies/directory-structure-guide.md` | Placement criteria for GOVERNMENT layers, maps, README, and AGENTS |
| 4 | `GOVERNMENT/README.md` | GOVERNMENT root role and protected-canon write rules |
| 5 | `GOVERNMENT/User-Constitution/agent-brief.md` | Agent read-order pattern, not project definition |
| 6 | `GOVERNMENT/Working-Pad/TASK-QUEUE.md` | Active task index and open-file sync model |
| 7 | `GOVERNMENT/Agents-Bylaws/templates/map-template.md` | Map format and lifecycle-map distinction |
| 8 | `map-repo.md` | Root-boundary pattern |
| 9 | `GOVERNMENT/Working-Pad/issue-notes/open/260608-cross-project-government-migration-template.md` | TNS T0-T6 dry-run sequence |

Do not use deleted or archived `knowledge/`, `user-vault`, `project-wiki`, `human-vault`, or `agent-wiki` language as current migration policy.

## Scope And Non-Goals

In scope:

- Record the current TNS baseline.
- Classify existing roots and high-signal files by role.
- Propose TNS-specific target roots and map coverage.
- Define future movement order, gates, verification commands, and rollback rules.

Out of scope for this pass:

- Moving or renaming any existing file or directory.
- Creating empty or unused GOVERNMENT subtrees beyond the initial bootstrap.
- Creating `research-space/`, `study-space/`, `product-space/`, or `code-space/`.
- Copying AAD `product-space/` or `code-space/` naming into TNS.
- Rewriting root `README.md` beyond recording that it needs a separate cleanup.
- Absorbing project-local lifecycle notes such as `Projects/1D-multi-solver-demo/theory/progress/open/` into repo-wide `GOVERNMENT/Working-Pad/`.

## Decision Ledger

| Ledger item | Current finding |
|---|---|
| Evidence summary | Pre-plan repo had `README.md`, `.gitignore`, `requirements.txt`, `src/`, `Tutorials/`, and `Projects/`. No operational `GOVERNMENT/`, root `AGENTS.md`, `CLAUDE.md`, `SPEC.md`, `charter.md`, `map-*.md`, or repo-wide Working-Pad lifecycle was found. Current untracked state should be this plan file only. |
| Proposed working mode | Fresh migration + baseline gate. Evidence: no operation root exists; existing corpus is project/study/research material, not operating governance. |
| Modifiers | Research/study repo, large notebooks, project-local progress lifecycle, root README drift resolved during bootstrap, no Working-Pad checker, no frontmatter policy/checker, existing `src/` runtime root. |
| Agent-safe work | Inventory, classification, plan writing, old-term reference search, future verification command design. |
| Needs user decision | Future `*-space` creation or root renames, root README rewrite, any bulk move, and any protected-canon change beyond the 2026-06-10 migration decision. |
| Stop conditions already relevant | Future `research-space/` or `study-space/` names are not approved. Further root README expansion should stay thin and route details to GOVERNMENT. |

## Source Inventory

### Root Snapshot

Tracked file count:

```text
65 tracked files
```

Top-level tracked distribution:

| Root | Tracked count | Current role |
|---|---:|---|
| `.gitignore` | 1 | Ignore rules for Python, notebooks, generated figures, and project-local outputs |
| `README.md` | 1 | Human entrypoint; currently drifted/stale in structure descriptions |
| `requirements.txt` | 1 | Root learning/runtime dependency list |
| `src/` | 4 | Existing core library skeleton; keep as runtime root |
| `Tutorials/` | 6 | Learning notebook corpus |
| `Projects/` | 52 | Core project corpus: research demos, theory notes, tests, scripts, notebooks |

Absent before bootstrap:

- operational `GOVERNMENT/`
- root `AGENTS.md`
- `CLAUDE.md`
- `SPEC.md`
- `charter.md`
- root or folder-level `map-*.md`
- repo-wide `TASK-QUEUE.md`

### Project Corpus

| Path | Current role | Migration note |
|---|---|---|
| `Projects/1D-multi-solver-demo/_meta/PLAN.md` | Approved 1D multi-solver demo plan and implementation sequence | Treat as project corpus. Do not move into GOVERNMENT. |
| `Projects/1D-multi-solver-demo/theory/` | Theory specification and exact-solution notes | Treat as study/research project content. Add map coverage later only if useful. |
| `Projects/1D-multi-solver-demo/theory/progress/open/first-slice.md` | Project-local implementation-slice note | Keep project-local by default. Do not auto-register in repo-wide Working-Pad. |
| `Projects/Cluster_Ising/` | Runnable paper reproduction project with package, tests, scripts, notebooks | Treat as research/runtime project corpus. Any path move requires import/test verification. |
| `Tutorials/Notebooks/` | Learning notebooks and notebook-local helper code | Candidate study corpus. Do not rename until notebook references are checked. |
| `src/` | Root package skeleton | Keep as existing runtime root; do not force `code-space/`. |

### Root README Drift

Resolved in the initial bootstrap follow-up: root `README.md` is now a thin human-facing note. The detailed project definition lives in `GOVERNMENT/User-Constitution/project-definition.md`.

## Proposed TNS Roots

The default conservative plan is to preserve meaningful existing roots first, then introduce `*-space` roots only where they remove ambiguity.

| Candidate root | Proposed status | Why |
|---|---|---|
| `GOVERNMENT/` | Future operating root after user approval | Needed for repo-local task queue, issue notes, agent rules, migration plans, and protected decisions. |
| `Projects/` | Keep by default | Already a meaningful project corpus root. It contains important TNS knowledge and runnable research projects. |
| `research-space/` | Candidate, not default move | Could eventually hold stable research project definitions or consolidate `Projects/` if the user wants suffix-normalized roots. Requires approval. |
| `Tutorials/` | Keep by default | Existing study material root. Notebook paths and user mental model may depend on it. |
| `study-space/` | Candidate, not default move | Could eventually hold tutorial/lecture/study material if the user wants a stronger GOVERNMENT + space layout. Requires approval. |
| `src/` | Keep | Existing runtime root. Moving to `code-space/` would add import/config risk without current value. |
| `var/` | Optional ignored runtime root | Only useful if generated logs/cache/exports need a repo-local home. Do not create empty. |

Explicit non-choice: do not create AAD-style `product-space/` or `code-space/` in TNS by default.

## Classification Table

| Current path | Current role | Candidate target | Action | Needs user approval? | Notes |
|---|---|---|---|---|---|
| `README.md` | Human root entrypoint | Keep root | Later update | Yes | Root contract; separate from structural migration. |
| `.gitignore` | Ignore/generated-output policy | Keep root | Keep/update only if generated roots change | Maybe | Existing project-local output ignores should be preserved. |
| `requirements.txt` | Root Python dependencies | Keep root | Keep | No | A root dependency file is acceptable for this repo. |
| `src/` | Core runtime package skeleton | Keep `src/` | Keep | No for keeping; yes for moving | Avoid `code-space/` unless imports/config are redesigned. |
| `Tutorials/Notebooks/` | Study/learning notebooks | Keep `Tutorials/` or later `study-space/` | Keep for now | Yes for rename | Notebook references and outputs need checks before any move. |
| `Tutorials/Notebooks/src/ncon.py` | Notebook helper code | Keep under tutorial corpus | Keep | Maybe | If promoted to library later, handle as separate code migration. |
| `Projects/` | Important project corpus | Keep `Projects/` or later `research-space/` | Keep for now | Yes for rename | T0 corpus boundary: do not conflate with GOVERNMENT. |
| `Projects/1D-multi-solver-demo/_meta/PLAN.md` | Approved project plan | Keep project-local | Keep | No | It is not a repo-wide issue note. |
| `Projects/1D-multi-solver-demo/theory/*.md` | Theory docs and model notes | Keep project-local | Keep | No | Can receive project-local map coverage later. |
| `Projects/1D-multi-solver-demo/theory/progress/open/first-slice.md` | Project-local progress lifecycle | Keep project-local | Keep | Yes to absorb | Default is not to move into Working-Pad. |
| `Projects/1D-multi-solver-demo/theory/writing-guidelines.md` | Project-local writing policy | Keep project-local; possible future `Agents-Bylaws/policies/tns-writing-style.md` | Keep for now | Yes for promotion | It references LSWT policy; do not generalize automatically. |
| `Projects/Cluster_Ising/` | Runnable research project | Keep project-local | Keep | Yes for move | Contains package, tests, notebooks, scripts. Moving requires smoke tests. |
| `Projects/Cluster_Ising/pyproject.toml` | Package/build metadata | Keep with package | Keep | Yes for move | Path-sensitive package context. |
| `Projects/Cluster_Ising/tests/` | Project tests | Keep with project | Keep | Yes for move | Use for future migration verification. |
| `GOVERNMENT/Working-Pad/issue-notes/closed/260610-government-migration-plan.md` | Migration plan | Closed Working-Pad issue note | Moved to closed after bootstrap | Already approved | Records initial GOVERNMENT bootstrap and remaining boundaries. |

## Implemented Minimal Bootstrap

Implemented after user approval:

```text
GOVERNMENT/
  README.md
  User-Constitution/
    agent-brief.md
    project-definition.md
    map-user-constitution.md
  Court-Precedents/
    tns-government-migration-2026-06.md
    map-decisions.md
  Agents-Bylaws/
    map-agents-bylaws.md
    policies/
      tns-government-migration-policy.md
    templates/
      map-template.md
      issue-notes-template.md
  Working-Pad/
    TASK-QUEUE.md
    map-working-pad.md
    issue-notes/
      map-issue-notes.md
      open/
        260610-government-migration-plan.md
```

Still not created:

- `research-space/`
- `study-space/`
- `product-space/`
- `code-space/`
- `agent-wiki/`

Bootstrap rule: `GOVERNMENT/Working-Pad/` exists to manage active work. It is not a replacement for `Projects/` or `Tutorials/`.

## Movement Sequence

No movement is approved in this plan. The following is the future sequence after user approval.

| Phase | Action | Gate |
|---|---|---|
| T0 | Ask the user to accept the `Projects/` corpus boundary for the active checkout | Done: include as official project corpus, keep in place, separate from GOVERNMENT. If `?? Projects/...` appears later, stop for commit/include/separate decision. |
| T1 | Confirm root naming: keep `Projects/`/`Tutorials/` or adopt `research-space`/`study-space` | Current default: keep `Projects/`, `Tutorials/`, and `src/`. No AAD `product-space`/`code-space` copy. |
| T2 | Create minimal GOVERNMENT bootstrap | Done: root entrypoints, protected decision/brief, Working-Pad queue/maps, and minimal Agents-Bylaws policy/templates. |
| T3 | Rewrite root `README.md` as a thin note and move detailed project definition into GOVERNMENT | Done: `README.md` is thin; details live in `GOVERNMENT/User-Constitution/project-definition.md`. |
| T4 | Add map coverage in order: root map, Working-Pad map, then project maps only where useful | Do not auto-create maps for every folder. |
| T5 | Add template/skill preset only when there is immediate use | No bulk copy of AAD templates. |
| T6 | Preserve project-local progress lifecycle | Do not auto-absorb `theory/progress/open/` into repo-wide Working-Pad. |
| T7 | Optional project-space move, if approved | Verify imports, notebook references, scripts, tests, and README path references. |

### Candidate Future Moves

| Candidate move | Default | Reason |
|---|---|---|
| `Projects/` -> `research-space/` | Do not move | `Projects/` is meaningful and already tracked. |
| `Tutorials/` -> `study-space/` | Do not move | Notebook path/reference risk; user approval needed. |
| `src/` -> `code-space/src/` | Do not move | Existing runtime root should remain stable. |
| `Projects/1D-multi-solver-demo/theory/progress/open/` -> `GOVERNMENT/Working-Pad/` | Do not move | It is project-local lifecycle, not repo-wide operating control. |

## Approval-Required Items

| Decision | Default until approved |
|---|---|
| T0 `Projects/` corpus boundary | Approved for this pass: official project corpus, keep in place, separate from GOVERNMENT |
| Full minimal GOVERNMENT bootstrap | Initial bootstrap created |
| `Projects/` rename or placement under `research-space/` | Keep `Projects/` |
| `Tutorials/` rename or placement under `study-space/` | Keep `Tutorials/` |
| Root `README.md` rewrite | Done: thin note only |
| Root `AGENTS.md` creation | Defer until agent-brief/source rules are approved |
| `User-Constitution/` protected canon | Do not create empty; stage only real approved principles |
| `Court-Precedents/` protected decisions | Do not create empty; use only for accepted closed decisions |
| `Agents-Bylaws/` policy/template/skill import | Do not bulk copy; add only target-local rules with immediate use |
| Promotion of `writing-guidelines.md` to repo-wide policy | Keep project-local |
| Any physical path move of code/notebooks/projects | Defer until path verification plan is accepted |

## Path Reference Checks

Before any future move, run targeted searches for current active references:

```bash
rg -n "Projects/|Tutorials/|src/|Docs/|Benchmarks/" README.md Projects Tutorials src requirements.txt .gitignore
rg -n "GOVERNMENT|Working-Pad|product-space|code-space|knowledge/|user-vault|project-wiki|human-vault|agent-wiki|product-workspace" -g '!node_modules/**' -g '!dist/**' -g '!build/**' -g '!coverage/**' -g '!var/**'
rg -n "Projects/1D-multi-solver-demo|Projects/Cluster_Ising|Tutorials/Notebooks" -g '!node_modules/**' -g '!dist/**' -g '!build/**' -g '!coverage/**' -g '!var/**'
```

Known current reference:

- `Projects/1D-multi-solver-demo/theory/writing-guidelines.md` links to LSWT `GOVERNMENT/Agents-Bylaws/policies/lswt-writing-style.md`. This is a cross-repo style reference, not evidence that TNS already has GOVERNMENT.

README drift resolution:

- Removed stale `Docs/` and `Benchmarks/` root claims.
- Removed duplicate repository-structure sections.
- Added pointers to `map-repo.md`, `GOVERNMENT/User-Constitution/project-definition.md`, and `GOVERNMENT/Working-Pad/TASK-QUEUE.md`.

## Verification Commands

### Bootstrap Verification

Run after initial bootstrap:

```bash
git status --short
git diff --check
test -f GOVERNMENT/Working-Pad/issue-notes/closed/260610-government-migration-plan.md
test -f GOVERNMENT/Working-Pad/TASK-QUEUE.md
test -f GOVERNMENT/Working-Pad/issue-notes/map-issue-notes.md
```

### Pre-Move Verification

Run before any future structural move:

```bash
git status --short
git status --porcelain=v1 -uall -- Projects
git ls-files Projects
rg --files -g '*.md' -g '!node_modules/**' -g '!dist/**' -g '!build/**' -g '!coverage/**' -g '!var/**'
rg --files -g '!node_modules/**' -g '!dist/**' -g '!build/**' -g '!coverage/**' -g '!var/**'
```

### Post-Bootstrap Verification

After an approved minimal bootstrap:

```bash
git status --short
git diff --check
test -f GOVERNMENT/README.md
test -f GOVERNMENT/Working-Pad/TASK-QUEUE.md
test -f GOVERNMENT/Working-Pad/map-working-pad.md
test -f GOVERNMENT/Working-Pad/issue-notes/map-issue-notes.md
```

If no automated Working-Pad checker exists, manually compare:

- every file in `GOVERNMENT/Working-Pad/issue-notes/open/`
- every file in future `handoff/open/`, `vault-staging/`, and `idea-proposals/open/`
- rows in `GOVERNMENT/Working-Pad/TASK-QUEUE.md`
- entries in corresponding `map-*.md` files

### Runtime Verification If Project Paths Move

Only needed if code/project paths move:

```bash
python -m compileall src Projects/Cluster_Ising/cluster_ising
python -m pytest Projects/Cluster_Ising/tests
python Projects/Cluster_Ising/scripts/reproduce_paper.py
```

The reproduction script may be slower and dependency-sensitive; use it as an optional stronger smoke test unless the moved paths affect that project directly.

## Rollback Plan

Plan-only rollback:

1. Remove this plan file if the user rejects it.
2. Remove empty parent directories only if they contain no other accepted files.
3. Confirm with `git status --short`.

Future bootstrap rollback:

1. Revert only the migration commit or reverse `git mv` operations in the exact old-to-new map order.
2. Do not delete or rewrite project corpus under `Projects/`, `Tutorials/`, or `src/`.
3. Re-run `git status --short` and `git diff --check`.
4. Re-run path-reference searches for any moved paths.

Future code/path rollback:

1. Restore moved runtime files to their previous paths.
2. Restore package metadata, imports, scripts, notebook references, and README links.
3. Re-run `python -m compileall ...` and project tests relevant to the moved paths.

## Stop Conditions

Stop and ask the user before continuing if:

- `git status --short` shows unrelated dirty changes.
- `git status --porcelain=v1 -uall -- Projects` shows untracked `Projects/` content.
- The user has not approved `research-space/` or `study-space/` names.
- A root contract file such as `README.md` or future `AGENTS.md` would change meaning.
- A file mixes project definition, active task state, and closed decision in one body and cannot be split mechanically.
- Code imports, package scripts, notebooks, or launch commands depend on current paths.
- Protected canon content needs to be accepted, rejected, or rewritten.
- A proposed map/queue update would create sync drift.

## Safe-To-Move Summary

Safe to move without user approval in the current plan: **none**.

Safe to do after this plan without changing corpus:

- Decide root naming policy.
- Add more Agents-Bylaws policies or templates only when they have immediate TNS use.

## Open Questions

| Question | Default |
|---|---|
| Should TNS keep `Projects/` as the stable corpus root? | Yes |
| Should `research-space/` exist at all? | Only if user wants suffix-normalized research areas |
| Should TNS keep `Tutorials/` or move to `study-space/`? | Keep `Tutorials/` |
| Should `src/` stay root-level? | Yes |
| Should project-local progress notes be registered in repo-wide TASK-QUEUE? | No, unless they coordinate repo-wide operations |
| Should TNS create protected canon immediately? | No; only create when there is real approved content |
