---
frontmatter-version: 1
title: 1D Solver UI/App 제작 계획
section: issue-notes/open
issue-type: discussion
status: draft
last-edited-by: codex
created: 2026-06-21
updated: 2026-06-23
---

# 1D Solver UI/App 제작 계획

> **문서 역할:** 구현 핸드오프 스펙. 이 노트는 repo-wide issue note 형식에서는 `discussion`으로 두고, `TASK-QUEUE.md`에서는 P0 implementation item으로 추적한다.
> **원본 plan:** `~/.claude/plans/pure-cuddling-koala.md`.
> **읽는 순서:** `Current Agreement` -> `Scope And Non-Goals` -> `Plan`의 `SPEC A-D` -> `Verification`.

## Current Agreement

- **무엇을 만드는가:** 임의의 1D spin-1/2 chain을 `정의 -> 풀이 -> 결과 확인`까지 안내하는 Streamlit multi-page app.
- **왜 만드는가:** 현재 프로젝트에는 "어떤 solver가 system definition에서 무엇을 소비하는지"를 기록하는 probe는 있지만, family의 임의 파라미터를 실제로 푸는 앱 흐름은 없다.
- **핵심 접근:** 새 framework를 만들지 않고 기존 척추인 `SpinSystem -> change_form`에 project-local ED solver와 observable layer를 붙인다.
- **정본 Hamiltonian family:** $H = H_{\mathrm{XXZ}} + H_{\mathrm{cluster}} + H_{\mathrm{Zeeman}}$.
- **확정 결정:** D1-D5는 아래 `SPEC D`의 implementation decisions로 고정한다.
- **구현 담당:** codex.

## Scope And Non-Goals

**In scope**

- Streamlit app under `Projects/1D-multi-solver-demo/app/`.
- Family parameters: `Jxy`, `Jz`, `K`, `hz`, `hx`.
- Geometry parameters: chain length `L`, boundary condition `OBC/PBC`.
- First solver: ED.
- Observable basics: ground-state energy, energy per site, site-resolved `Sz`, correlations, half-chain entanglement entropy.
- Exact overlay when the chosen limit has a documented reference.
- Define page as a clean system-definition screen, not a theory lecture page.

**Non-goals**

- 2D systems.
- DMRG/NQS/TN implementation in this slice.
- Arbitrary operator editor.
- Dynamics/time-evolution animation.
- Promotion into `code-space/` shared toolbox.
- Long theory exposition inside Streamlit Home or Define.

## Evidence

- The project already has the conceptual pipeline `SpinSystem -> MethodForm(ED)`, but the runnable solver/result/observable path must be made explicit for the app.
- The app should preserve the probe character: each page should show what it consumes and produces.
- User feedback on 2026-06-23 rejected unclear or duplicate Define-page layout. In particular:
  - Home should stay clean and minimal; project basics belong in Define or supporting docs.
  - Define should distinguish the required pre-definition work for a spin system.
  - The main split should be **Geometry** and **Hamiltonian**.
  - Lattice controls should not be duplicated in an extra banner when an existing input card can own them.
  - Lattice explanation belongs near the lattice preview, and 1D geometry should not be over-explained.
  - Boundary condition must be user-editable.
  - A free index `i` is not meaningful unless it is introduced together with the lattice/index set.
- `GOVERNMENT/Agents-Bylaws/templates/issue-notes-template.md` requires active issue notes to use the standard sections in this document and to be registered in both `TASK-QUEUE.md` and `issue-notes/map-issue-notes.md`.

## Plan

### SPEC A - App Flow

The app is a four-step browser workflow:

```
1. Define system -> 2. Select method form -> 3. Solve -> 4. Inspect observables
   parameters        ED first              diagonalize  observables + exact overlay
```

| Step | Page | User action | Page output |
|---|---|---|---|
| 1 | Define | Set `L`, boundary condition, and couplings | Chain preview, Hamiltonian summary, active term support |
| 2 | MethodForm | Select solver form, ED first | What ED consumes from `SpinSystem` |
| 3 | Solve | Run the calculation | `E0`, `E0/L`, wall time, state summary |
| 4 | Observables | Select observable views | `Sz`, correlations, entanglement entropy, exact comparison when available |

Example path: for Heisenberg chain with `L=8`, `PBC`, `Jxy=1`, `Jz=1`, `K=0`, `hz=0`, `hx=0`, the Define page shows the chain and Hamiltonian terms, Solve runs ED, and Observables compares supported quantities against documented exact references where applicable.

### SPEC B - Define Page Contract

**Page role**

- Define creates one `SpinSystem`.
- Its output is the system definition passed to `MethodForm -> Solve -> Observables`.
- It does not run ED, explain method conversion in detail, compute observables, or host long theory notes.

**Required sections**

1. **Geometry**
   - Purpose: define the geometry of a 1D chain.
   - Inputs: `L`, boundary condition (`open`/`periodic`).
   - Fixed premise: local Hilbert space is spin-1/2 and local dimension is 2.
   - Visual: lattice preview centered in this section.
   - Explanation: keep 1D geometry short; detailed notation such as $\Lambda_L$, bond set, and cluster-center set belongs in a nearby `Lattice notation` expander.
2. **Hamiltonian**
   - Purpose: define the Hamiltonian family and coupling values.
   - Inputs: term view selector (`Full`/`XXZ`/`Cluster`/`Zeeman`), `Jxy`, `Jz`, `K`, `hz`, `hx`.
   - Visual/summary: show the full Hamiltonian and, next to it, the selected term's expression/support explanation.
   - Diagnostics: show active matrix-term count; put the matrix-term table in an expander.

**Layout rules**

- Use only the two top-level body sections **Geometry** and **Hamiltonian** for basic system definition.
- Do not introduce duplicate section names such as `Lattice controls`, `Lattice sets`, or `System inputs` unless a later spec gives them distinct ownership.
- Do not duplicate the same values in both summary cards and input cards.
- Keep system-definition inputs in the page body; leave the sidebar for Streamlit navigation unless a later design explicitly assigns it a role.
- Treat the Hamiltonian term selector as a view/highlight selector. Actual matrix-term activity is determined by coefficient values.
- If `K=0`, the cluster term remains part of the family but contributes zero active matrix terms.

### SPEC C - Visual Requirements

**Define page**

- Hamiltonian should be visually central.
- Draw the chain as sites and bonds.
- Represent interactions as links:
  - XXZ: two-site links.
  - Cluster: three-site support, visually grouped across neighboring sites.
  - Zeeman: on-site arrows or markers, not as bonds.
- Use color or line pattern to distinguish term families, but avoid a noisy legend-heavy layout.

**Solve page**

- Show ground-state spin alignment from expectation values where meaningful.
- Hide arrows when $|\langle S\rangle|$ is below threshold; do not imply a fake direction in a disordered or symmetry-preserving state.

**Observables page**

- Show observable tables/plots and exact overlays with visible deviations when a reference exists.
- If no exact reference applies, state that this is ED-only for that parameter point.

### SPEC D - Implementation Decisions

- **D1 Input range:** family parameters only: `Jxy`, `Jz`, `K`, `hz`, `hx`. Future new terms should require builder extension, not a full data-model rewrite.
- **D2 Solver order:** ED first with exact comparison in known limits. The next solver family is TN, then NQS later.
- **D3 UI structure:** Streamlit multi-page app using `pages/`.
- **D4 App location:** `Projects/1D-multi-solver-demo/app/`.
- **D5 Cluster OBC:** bulk-only, center index `i=1..L-2`; PBC uses index mod `L`. This must be documented in `model-hamiltonian.md` before relying on it in code.

### Implementation Sequence

1. Record the cluster OBC rule in `Models/1d-spin-chains/model-hamiltonian.md` and project metadata.
2. Generalize the builder with `build_spin_chain(...)`, keeping `build_xxz_chain(...)` as a thin wrapper.
3. Implement project-local ED from the `change_form(ED)` payload.
4. Implement measurements for energy, `Sz`, correlations, and half-chain entanglement entropy.
5. Add exact-reference overlays for documented solvable limits.
6. Build the Streamlit pages: Home, Define, MethodForm, Solve, Observables.
7. Add builder, ED, and app-flow tests.
8. Add `streamlit` to project requirements.

### Detailed Implementation Notes

**Pipeline**

```
SpinSystem -> MethodForm(ED) -> SolverInput -> SolverResult -> ObservableResult -> Exact/Compare
```

**Builder**

- Target module: `one_dimensional_multi_solver_demo/spin_models.py`.
- Add `build_spin_chain(*, length, bc, jxy, jz, K, hz, hx)`.
- Generate XXZ, Zeeman, and cluster terms by boundary-condition rules.
- Store useful metadata such as model family and cluster coupling.
- Verify `change_form(system, ED)` already serializes arbitrary matrix terms, including three-body terms.

**ED solver**

- Target module: `one_dimensional_multi_solver_demo/solvers/ed.py`.
- Consume the ED method-form payload: local matrices, matrix terms, basis, and boundary condition.
- Assemble each matrix term with Kronecker products.
- Use sparse or dense diagonalization appropriate for small ED sizes.
- Return a project-local result object with energy, energy per site, state, wall time, and Hilbert dimension.

**Observables**

- Implement `E0`, `E0/L`, site-resolved `Sz`, connected `Sz-Sz` correlations, and half-chain entropy.
- For entropy, reshape the ground state across the half-chain bipartition and compute `-sum(p log p)` from singular values.

**Exact overlay**

- Use documented references for XX/XXZ/Heisenberg, TFIM, and cluster-Ising limits.
- If the parameter point does not match a supported exact limit, show "exact 기준 없음(ED만)".

**Reusable assets**

- `method_form.py::change_form`
- `spin_system.py`
- `Cluster_Ising` solver/result and exact-solution patterns, copied project-locally where needed rather than imported as an external project dependency.
- `Models/1d-spin-chains/exact-solutions/` for reference formulas.

## Repo Readiness Review Input

이 섹션은 사용자가 이 draft spec을 리뷰하기 전에 확인할 repo-side 입력 자료다. 구현 지시가 아니라, 현재 repo 상태와 이 plan 사이의 정합성 검토 포인트를 기록한다.

### Existing Prototype Surface

- 이 plan은 앞으로 구현할 계획처럼 쓰여 있지만, repo에는 이미 P0 slice와 겹치는 prototype/prior-attempt 구현이 있다.
- 이 기존 구현은 승인된 starting baseline이 아니다. 구현 단계에서는 각 부분을 `reuse`, `revise`, `discard`로 판정한 뒤 편입한다.
- 이 plan의 acceptance 기준은 기존 구현 상태가 아니라 `SPEC A-D`와 사용자의 review decision이다.
- `Projects/1D-multi-solver-demo/app/`에는 `Home`, `Define`, `MethodForm`, `Solve`, `Observables` Streamlit pages가 이미 있다.
- `Projects/1D-multi-solver-demo/one_dimensional_multi_solver_demo/`에는 `build_spin_chain(...)`, `change_form(system, ED)`, project-local ED solver, observables, exact-reference overlay가 이미 있다.
- `Models/1d-spin-chains/model-hamiltonian.md`는 cluster OBC rule을 이미 문서화한다: open boundary는 bulk-centered terms `i=1..L-2`, periodic boundary는 modulo index.
- Root `requirements.txt`에는 `streamlit>=1.58`가 이미 있다.
- Current prototype test status: `python -m pytest Projects/1D-multi-solver-demo/tests/` passes with 14 tests.
- Current dirty worktree observed during readiness review is limited to map/template navigation files, not P0 app/backend/test files.

### Review Questions Before Execution

1. 기존 app/backend 구현 중 어떤 부분을 새 plan의 구현 기반으로 재사용할 것인가? 각 주요 surface를 `reuse`, `revise`, `discard`로 판정한다.
2. `Define` page의 Hamiltonian term selector를 view/highlight selector로 확정할 것인가? 현재 UI copy에는 "choose active terms", "active term family"처럼 active toggle로 오해될 수 있는 표현이 남아 있다.
3. `Home` page는 현재처럼 Project/Scope/Current Implementation/Planned Implementation 설명을 유지할 것인가, 아니면 "clean and minimal" 기준에 맞춰 더 줄일 것인가?
4. Exact overlay acceptance는 현재 구현된 finite PBC XXZ Bethe reference와 pure cluster stabilizer limit까지만 둘 것인가, 아니면 이 draft에 언급된 TFIM limit까지 이번 ED UI slice에 포함할 것인가?
5. `Projects/1D-multi-solver-demo/_meta/current-status.md`와 `next-actions.md`는 현재 구현 상태보다 뒤처진 부분이 있다. P0 구현 전에 먼저 갱신할 것인가, 아니면 implementation close 단계에서 갱신할 것인가?

### Known Alignment Notes

- `Define` page already uses the two main body sections `Geometry` and `Hamiltonian`.
- Boundary condition is already user-editable on the Define page.
- `build_spin_chain(...)` already supports `Jxy`, `Jz`, `K`, `hz`, `hx`, `open`, and `periodic`.
- `change_form(system, ED)` already serializes arbitrary matrix terms, including three-body cluster terms.
- `solve_ed(...)` consumes the ED `MethodForm` payload and returns energy, energy per site, state, wall time, Hilbert dimension, boundary condition, and term count.
- Observable helpers already cover site-resolved `Sz`, connected `Sz-Sz`, spin-vector expectation, and half-chain entropy.

### Known Drift Or Risk

- The current `Define` page copy may conflict with the intended selector semantics. The selector should highlight/view term families; coefficient values determine active matrix terms.
- `Home.py` may contain more explanatory content than the intended minimal Home page.
- `exact_references.py` currently covers finite PBC XXZ Bethe and pure cluster stabilizer overlays; TFIM is not currently implemented as an app overlay.
- `_meta/current-status.md` includes an outdated directory structure block that omits current app pages, ED solver, observables, exact references, and additional tests.
- `_meta/next-actions.md` still describes earlier first-slice work and should not be treated as the latest execution checklist without reconciliation.

## Approval Needed

- User review of `SPEC B - Define Page Contract`, especially whether **Geometry** and **Hamiltonian** are the only top-level sections needed for the Define page.
- User review of the Hamiltonian term selector semantics: view/highlight selector versus active-term toggle.
- User review of how much theory belongs in Define expanders versus model notes.
- User confirmation before extending beyond ED into TN/NQS or dynamics.

## Verification

- `pytest Projects/1D-multi-solver-demo/tests/`
- `streamlit run Projects/1D-multi-solver-demo/app/Home.py`
- Manual page flow:
  - Define: edit `L`, boundary condition, and couplings.
  - MethodForm: confirm ED input summary.
  - Solve: run ED and inspect energy/time/state summary.
  - Observables: inspect `Sz`, correlations, entropy, and exact overlay behavior.
- Reference cases:
  - XX chain, small `L`, PBC: ED agrees with exact free-fermion reference.
  - Cluster-Ising, small `L`: ED agrees with project-local regression reference.

## Rollback Or Close Conditions

**Rollback**

- If the Define-page section contract is rejected, revert only the affected UI/spec slice and keep the solver/backend work separate.
- If the Hamiltonian family boundary changes, update `SPEC A-D` before changing code.

**Close**

- Close this note when the app implements the approved ED slice, tests pass, and the Define/MethodForm/Solve/Observables flow is manually verified.
- Move the note to `issue-notes/closed/` and update `TASK-QUEUE.md` plus `issue-notes/map-issue-notes.md` at close time.
