---
frontmatter-version: 1
title: System Definition Design
section: issue-notes/open
issue-type: discussion
status: draft
last-edited-by: claude
created: 2026-06-13
updated: 2026-06-14
---

# System Definition Design

상태: open issue note  
범위: 2D spin-system solver 구조를 설계하기 위한 `SpinSystem` 정의와 method-specific form 분기

## 1. Purpose

이 문서는 `1D-multi-solver-demo`에서 사용할 system definition을 어떻게 나눌지 논의한다. 1D
chain은 최종 산출물이 아니라, 2D spin system을 여러 방법으로 풀기 전에 같은 physical system을
각 method가 어떻게 다르게 소비하는지 관찰하기 위한 controlled probe다.

따라서 이 문서는 solver 구현 문서가 아니다. 목표는 `SpinSystem`에 무엇을 넣고, 무엇을
`change_form(system, method)` 단계로 넘길지 결정하는 것이다.

## 2. Design Goal

최종 목표는 여러 방법으로 2D spin system을 풀 수 있는 solver 구조를 설계하는 것이다. 문제는
각 방법이 같은 physical system definition을 서로 다른 형태로 요구한다는 점이다.

이 1D probe에서는 다음 질문을 관찰한다.

- local Hilbert space가 어떻게 표현되어야 하는가.
- geometry, site, boundary, bond 정보가 어디까지 공통인가.
- Hamiltonian term은 matrix, named operator, graph, MPO, basis 중 어떤 형태로 변환되어야 하는가.
- ED, TN/DMRG, NQS, QuadHam 각각에 어떤 method-specific form이 필요한가.
- observable/result schema는 어디까지 공유 가능하고 어디서 갈라지는가.

## 3. Current Naming

현재 논의 기준 이름은 다음과 같다.

| Name | Role |
|---|---|
| `SpinSystem` | method-independent physical system definition |
| `ED` | exact diagonalization method selector |
| `TN` | tensor-network / DMRG method selector |
| `NQS` | neural quantum state method selector |
| `QuadHam` | quadratic Hamiltonian diagonalization method selector |
| `change_form(system, method)` | `SpinSystem`을 method-specific form으로 변환하는 함수 |
| `MethodForm` | 변환 결과와 consumption trace를 담는 공통 결과 record |

`View`라는 이름은 시각화처럼 오해될 수 있으므로 쓰지 않는다. `Representation`은 너무 길고,
method-specific 산출물을 과도하게 class hierarchy로 고정하는 느낌이 있으므로 현재는 쓰지 않는다.

## 4. Proposed Source-Of-Truth Split

`SpinSystem`은 method-independent physical system definition이어야 한다. ED, TN, NQS, QuadHam 중
어느 하나의 backend input shape에 종속되면 안 된다.

현재 working assumption은 다음 분리다.

```text
SpinSystem
  LocalHilbertSpace
  Sites
  Geometry / Bonds
  HamiltonianTerms
  Conventions / Metadata
```

### 4.1 LocalHilbertSpace

`LocalHilbertSpace`는 한 site의 자유도를 정의한다.

현재 후보 필드:

- `name`: 예, `spin_half`.
- `dimension`: 예, `2`.
- `basis`: 예, `("up", "down")`.
- `operators`: 예, `Sx`, `Sy`, `Sz`, `Sp`, `Sm`, `I`.
- `convention`: 예, `spin`.

열린 질문:

- local operator matrix를 `LocalHilbertSpace`의 기본 표현으로 둘 것인가.
- 아니면 `LocalHilbertSpace`에는 operator name만 두고, matrix는 ED form에서 생성할 것인가.
- TN backend가 요구하는 named operator와 ED matrix를 같은 source에서 관리할 수 있는가.

현재 임시 판단:

- spin-1/2 probe에서는 local operator matrix를 `LocalHilbertSpace`에 둔다.
- 단, 이것을 ED 전용 표현으로 해석하지 않는다. 이것은 local operator의 기준 표현이고,
  method-specific backend object는 `change_form` 단계에서 만든다.

### 4.2 Site

`Site`는 physical site의 identity를 정의한다.

현재 후보 필드:

- `index`: deterministic integer id.
- `coordinate`: 1D에서는 `(i,)`, 2D에서는 `(x, y)`.
- `label`: optional display/debug label.
- `metadata`: sublattice, site type, orbital, layer 등이 필요해질 때 확장 후보.

열린 질문:

- 2D 확장을 위해 `sublattice`와 `site_type`을 지금부터 명시 필드로 둘 것인가.
- 아니면 first probe에서는 `metadata`로만 열어둘 것인가.

현재 임시 판단:

- 지금은 `index`, `coordinate`, `label`만 둔다.
- 2D lattice나 multi-site unit cell이 들어올 때 `metadata` 또는 명시 필드로 승격한다.

### 4.3 Geometry / Bonds

Geometry는 site 사이의 관계를 정의한다. Hamiltonian term과 geometry는 분리되어야 한다.

현재 후보 필드:

- `bonds`: nearest-neighbor bond list.
- bond fields: `site_i`, `site_j`, `kind`, `boundary`.
- `bc`: `open` 또는 `periodic`.

열린 질문:

- `Geometry`를 별도 object로 둘 것인가, 아니면 `SpinSystem` 안에 `sites`, `bonds`, `bc`를 직접 둘 것인가.
- 2D에서 directed bond, bond orientation, bond type, unit-cell offset을 어떻게 표현할 것인가.
- PBC는 단순 boundary bond 추가인가, 아니면 translation vector / wrapping metadata가 필요한가.

현재 임시 판단:

- 첫 probe에서는 `SpinSystem`이 `sites`, `bonds`, `bc`를 직접 가진다.
- 2D 확장에서 wrapping vector 또는 bond orientation이 필요해지면 `Geometry` object를 분리한다.

### 4.4 HamiltonianTerm

`HamiltonianTerm`은 spin Hamiltonian을 local operator product의 합으로 표현한다. 이 단계에서는 ED
matrix, MPO, graph local operator, quadratic matrix가 아니다.

현재 후보 필드:

- `label`: 예, `xx_exchange`, `yy_exchange`, `zz_exchange`.
- `coefficient`: numeric coupling.
- `operators`: `(OperatorOnSite("Sx", i), OperatorOnSite("Sx", j))`.
- `source`: model builder 또는 transformed term의 provenance.

열린 질문:

- Hermitian conjugate, complex coefficient, oriented terms를 어떻게 표현할 것인가.
- term support가 bond와 일치해야 하는지, 아니면 cluster/field처럼 독립적으로 허용할 것인가.
- coefficient가 scalar가 아니라 site-dependent function이면 어떻게 표현할 것인가.

현재 임시 판단:

- term은 geometry bond에서 생성될 수 있지만, geometry에 종속된 객체는 아니다.
- field term, cluster term, longer-range term을 위해 support는 arbitrary tuple로 허용한다.

## 5. Method-Specific Form Split

`change_form(system, method)`는 `SpinSystem`이 method별로 어떻게 소비되는지 드러내야 한다. 이 함수는
단순 변환뿐 아니라, method가 소비한 정보와 추가로 요구하는 정보를 record로 남겨야 한다.

현재 `MethodForm` 후보:

- `method`: method label.
- `status`: `ready`, `partial`, `not_applicable`.
- `payload`: method-facing data.
- `consumed`: `SpinSystem`에서 소비한 정보.
- `required_extra`: solver/backend 실행 전에 추가로 필요한 정보.
- `dropped`: 이 method form에서 버린 정보.
- `notes`: seam 설명.

## 6. Method-Specific Requirements

| Method | Consumes | Requires extra | Important seam |
|---|---|---|---|
| `ED` | local matrices, product basis, Hamiltonian terms | basis-sector policy later | basis ordering and Hilbert-space size |
| `TN` | named local operators, site type, bonds, MPO-friendly terms | backend site class, MPO builder policy | PBC is solver-cost seam |
| `NQS` | graph, local Hilbert space, local operator records | ansatz, sampler, random seed | stochastic metadata and graph/operator split |
| `QuadHam` | quadratic/free limit data | JW mapping and boundary sector when needed | interacting terms may be not applicable |

`QuadHam`은 tight-binding model을 뜻하지 않는다. 여기서는 quadratic Hamiltonian diagonalization form이다.
XX chain에서는 hopping matrix가 나오고, TFIM처럼 JW 이후 pairing이 생기는 경우에는 BdG form이
필요해질 수 있다.

## 7. Current Probe Boundary

현재 probe는 작은 1D chain으로 시작한다.

- first system: XXZ + Zeeman subset.
- first exact quadratic case: XX limit, `J_z=h_z=h_x=0`.
- `QuadHam`은 interacting `J_z`가 켜지면 `not_applicable`이어야 한다.
- periodic XX chain에서 `QuadHam`은 boundary hopping을 바로 numeric matrix로 완성하지 않는다.
  Jordan-Wigner boundary sector, 즉 fermion parity choice를 추가 요구사항으로 표면화해야 한다.

## 8. Open Design Questions

1. `LocalHilbertSpace`에 local operator matrix를 항상 둘 것인가, 아니면 operator registry로 분리할 것인가.
2. `Geometry`를 지금부터 별도 object로 만들 것인가, 2D 확장 시점까지 `SpinSystem` fields로 둘 것인가.
3. `Site`의 `sublattice`, `site_type`, `unit_cell`을 explicit field로 둘 것인가.
4. `HamiltonianTerm`의 coefficient는 scalar로 충분한가, 아니면 site-dependent coupling을 바로 고려할 것인가.
5. symmetry/conservation 정보는 `SpinSystem`이 명시해야 하는가, `change_form`이 추론해야 하는가.
6. observable/result schema는 `SpinSystem`에 연결할 것인가, solver result layer에서 별도로 둘 것인가.
7. `change_form(system, method)`의 method selector는 `ED`, `TN`, `NQS`, `QuadHam` 상수로 충분한가.

## 9. External Package Survey

This section records how related packages separate system definition, solving, measurement, and
result handling. The point is not to copy their folder structure, but to identify robust boundaries
for this project.

### 9.1 QuTiP

QuTiP centers computation around `Qobj`, a matrix-backed quantum object that can represent states,
operators, bras, kets, and superoperators. A `Qobj` carries data, dimensions, shape, Hermiticity, and
type information, so QuTiP does not keep a separate lattice/system-definition layer for spin systems
by default.

Observed split:

- physical input is already operator/state form: `Qobj`, tensor products, predefined operators.
- solver input is Hamiltonian/collapse operators/initial state/time list.
- observable input is `e_ops`, passed to solvers as operators or callables.
- solver output is `Result`, which stores `states`, `expect`, `times`, `solver`, `stats`, and options.

Design implication:

- QuTiP is close to an ED/dense-operator style backend form.
- It supports the idea that `ED` should consume matrix/operator objects and return state/result
  records, but it is not a good model for preserving geometry as a first-class object.

Sources:

- <https://qutip.readthedocs.io/en/latest/guide/guide-basics.html>
- <https://qutip.readthedocs.io/en/latest/apidoc/solver.html>

### 9.2 TeNPy

TeNPy separates local Hilbert space, lattice geometry, model Hamiltonian construction, algorithms,
simulations, and measurements more explicitly than QuTiP.

Observed split:

- local Hilbert space is handled by `Site` objects such as `SpinHalfSite`; charge conservation is
  chosen at the site level.
- geometry is handled by `Lattice` classes, with unit cells, lattice basis vectors, size, and boundary
  conditions.
- Hamiltonian construction is usually model-level, often through `CouplingMPOModel`, which turns
  coupling terms into MPO machinery.
- algorithm execution is separated from model definition.
- high-level `Simulation` ties parameters, model, algorithm, measurements, and saved output together.
- measurements are functions receiving `results`, `psi`, `model`, and `simulation`; they write into
  the `results` dictionary.

Design implication:

- `SpinSystem` should not be a TeNPy model, but our `TN` method form should expose exactly the pieces
  TeNPy-like backends need: site type/operators, lattice/bonds, boundary conditions, MPO-friendly
  term records, and conservation choices.
- Observable computation should be split into shared observable intent and method-specific
  measurement functions. TeNPy strongly supports this separation.

Sources:

- <https://tenpy.readthedocs.io/en/latest/intro/model.html>
- <https://tenpy.readthedocs.io/en/latest/intro/simulations.html>
- <https://tenpy.readthedocs.io/en/latest/intro/measurements.html>

### 9.3 ITensorMPS

ITensorMPS also shows a useful tensor-network split. A typical DMRG example creates site indices,
builds operator terms with `OpSum`, converts them into an `MPO`, creates an initial `MPS`, sets sweep
parameters, and runs `dmrg`, which returns energy and optimized MPS.

Observed split:

- local Hilbert space / site type: `siteinds(...)`.
- Hamiltonian term specification: `OpSum`.
- method-specific Hamiltonian form: `MPO(os, sites)`.
- initial state / ansatz: `random_mps(sites)` or another MPS.
- solve plan: sweep count, max bond dimension, cutoff.
- solver output: energy and MPS.

Design implication:

- TN backends often require an explicit conversion from symbolic/local operator terms into MPO form.
- `SolvePlan` should not be folded into `SpinSystem`; bond dimensions, cutoffs, and sweep schedules
  belong to method execution.

Source:

- <https://docs.itensor.org/ITensorMPS/stable/>

### 9.4 NetKet

NetKet makes the NQS split especially explicit. Its Heisenberg tutorial defines graph, Hilbert space,
Hamiltonian operator, exact diagonalization reference, ansatz model, sampler, variational state,
optimizer, and VMC driver as separate objects.

Observed split:

- graph: lattice/connectivity, e.g. `nk.graph.Hypercube`.
- Hilbert space: local spin space and optional constraints, e.g. fixed total magnetization.
- operator/Hamiltonian: graph-aware operator acting on a Hilbert space.
- reference calculation: `nk.exact.lanczos_ed`.
- ansatz/model: neural wavefunction model.
- sampler: sampling rule and chain count.
- variational state: combines sampler and ansatz.
- driver: optimization loop, e.g. `VMC_SR`.
- logging and observable APIs are separate from the physical system definition.

Design implication:

- `NQS` method form should expose graph, Hilbert, local operator records, and constraints, but not
  choose ansatz, sampler, optimizer, or run schedule.
- NQS observables are estimator/statistics problems, so result records need sampling metadata,
  variance/error bars, and seed.

Sources:

- <https://netket.readthedocs.io/en/latest/tutorials/gs-heisenberg.html>
- <https://netket.readthedocs.io/en/latest/user-guides/sr.html>

### 9.5 Cross-Package Pattern

The common package-level split is closer to the following than to a direct
`system / solver / physical quantities` folder split:

```text
physical definition
  -> method-specific form
  -> solve plan / backend configuration
  -> executor / driver / algorithm
  -> solution state or solver output
  -> observable specification
  -> method-specific measurement / estimator
  -> result record
  -> validation / report
```

Working conclusion:

- `SpinSystem` should own physical definition only.
- `change_form(system, method)` should produce method-specific input forms.
- `SolvePlan` should be separate from both `SpinSystem` and `MethodForm`.
- `ObservableSpec` should be shared, but `Measurement` or `Estimator` should be method-specific.
- `ResultRecord` should be shared enough for comparison, but retain method-specific metadata.
- Folder structure should not directly mirror the three conceptual stages `system`, `solve`,
  `physical quantities`; those labels are useful for prose but too coarse for code ownership.

## 10. User Comments

이 섹션은 설계 논의 중 사용자가 직접 남기거나, Codex가 사용자의 확인된 발언을 옮겨 적는 공간이다.
아직 확정 decision으로 승격하지 않은 코멘트는 이곳에 둔다.

- 2026-06-13: 1D model은 최종 산출물이 아니라 2D solver 구조를 설계하기 위한 controlled probe다.
- 2026-06-13: first code는 generic framework나 toolbox scaffold가 아니라 method가 system definition을
  어떻게 소비하는지 드러내는 최소 실험 코드여야 한다.
- 2026-06-13: `View`는 시각화처럼 들리므로 피한다.
- 2026-06-13: `Representation`은 너무 길다.
- 2026-06-13: `QuadHam`은 tight-binding이 아니라 quadratic Hamiltonian diagonalization을 뜻한다.

## 11. Decision Ledger

확정된 결정은 이 섹션으로 승격한다.

| Date | Decision | Notes |
|---|---|---|
| 2026-06-13 | Use `SpinSystem` for the method-independent source definition. | Exact field set still open. |
| 2026-06-13 | Use `change_form(system, method)` for method-specific export. | Method selector names remain reviewable. |
| 2026-06-13 | Use `QuadHam` for quadratic Hamiltonian diagonalization form. | Not a generic tight-binding label. |
| 2026-06-14 | Use `L` uniformly for system size; `L` is a free parameter for finite-size scaling. `N` notation removed. | First probe uses `L=8` as starting point; code takes `L` as an argument. |
| 2026-06-14 | TN path: fix `SolverInput` and measurement contract first; TeNPy DMRG execution is a later slice. | Step-by-step approach confirmed. |
| 2026-06-14 | Spin operator convention: `S = σ/2`. `Sz` eigenvalues `±1/2`. Applies to all numeric comparisons. | Standard condensed-matter convention. |
| 2026-06-14 | Primary two-point correlator: connected `C_c(i,j) = <Si^z Sj^z> - <Si^z><Sj^z>`. Unconnected `<Si^z Sj^z>` plotted alongside. | For zero-field XX chain `<Sz>=0` so both coincide; distinction appears at finite field or TFIM. |
| 2026-06-14 | Entanglement entropy: `S = -Tr(ρ ln ρ)` in nats (natural-log convention). | Matches TeNPy default. Differs from log₂ convention by factor of `ln 2`. |
| 2026-06-14 | `SolverResult` is not a uniform type. ED: full eigenvector; QuadHam: correlation matrix; TN: MPS handle; NQS: stochastic estimator. Method-specific measurement functions produce `ObservableResult`. | Difference in result type is itself seam evidence. |
| 2026-06-14 | First observable set is constrained to quantities computable by both TN and QuadHam/BdG. | Ensures cross-method comparison is valid for the XX-chain slice where QuadHam applies. |

## 12. Draft Next Plan For Critique

이 섹션은 확정 decision이 아니라 다음 대화를 위한 비판 대상 초안이다.

### 12.1 Revised Objective

다음 설계 목표는 `XX chain` OBC, 가능하면 `L=6` 또는 `L=8`, `Jxy=1`, `Jz=hz=hx=0`인 하나의
method-independent `SpinSystem`에서 ED, TN/DMRG, quadratic Hamiltonian method가 각자 필요한
method-specific form을 만들고, 공통 `ObservableSpec`으로 요청한 물리량을 method별 measurement로 계산한
뒤 하나의 comparison record로 정렬할 수 있는지 확인하는 것이다. 이것은 solver framework 자체가 아니라,
같은 system definition에서 공통 observable 계산과 비교 flow가 가능한지 증명하는 최소 slice다.

PBC XX chain은 후속 slice로 둔다. 이유는 `QuadHam`에서 Jordan-Wigner fermion parity sector를 정해야
하고, TN/DMRG에서는 PBC가 OBC보다 비용과 수렴 측면에서 별도 seam이 되기 때문이다.

### 12.2 Minimal Folder And Module Structure

현재 first-probe 파일은 유지하고, benchmark/report slice가 승인될 때만 아래 모듈을 추가하는 방향으로 둔다.

```text
Projects/1D-multi-solver-demo/
  one_dimensional_multi_solver_demo/
    spin_system.py          # physical source definition
    spin_models.py          # XXZ/Zeeman system builders
    method_form.py          # SpinSystem -> MethodForm export

    benchmark_points.py     # named physical settings, starting from XX OBC
    solve_plan.py           # backend/method execution knobs, not physics
    solver_input.py         # MethodForm + SolvePlan -> backend-ready input
    results.py              # SolverResult, ObservableResult, ComparisonReport
    observables.py          # shared ObservableSpec definitions
    measurements.py         # method-specific observable evaluation dispatch
    comparison.py           # align methods and observables into report rows

    solvers/
      ed.py                 # exact diagonalization baseline
      quad_ham.py           # free-fermion/quadratic path
      tn_dmrg.py            # TN/DMRG adapter after backend choice is fixed
```

이 구조는 `system / solve / physical quantities`처럼 큰 단계 이름을 그대로 폴더로 만들지 않는다. 대신
code ownership이 갈라지는 지점에 맞춘다: physical definition, method form, solve plan, solver input,
solver result, observable spec, method-specific measurement, comparison.

### 12.3 Calculation Flow Draft

```text
SpinSystem
  -> MethodForm
  -> SolverInput
  -> SolverResult
  -> ObservableSpec
  -> ObservableResult
  -> ComparisonReport
```

- `SpinSystem`: sites, bonds, boundary condition, local spin operator convention, Hamiltonian terms,
  model metadata만 가진다. 무엇을 계산할지나 어떤 backend knob를 쓸지는 넣지 않는다.
- `MethodForm`: `change_form(system, ED/TN/QuadHam)`의 출력이다. method가 소비한 source field,
  버린 field, backend 실행 전에 필요한 추가 정보를 기록한다.
- `SolverInput`: `MethodForm + SolvePlan`에서 만든다. ED의 matrix/basis, TN의 MPO/site policy,
  `QuadHam`의 hopping matrix 또는 correlation machinery처럼 backend-ready 입력을 담는다.
- `SolverResult`: method별 ground state 또는 충분한 state handle을 담는다. ED eigenvector, TN MPS,
  quadratic modes/correlation data는 같은 type으로 억지 통일하지 않는다.
- `ObservableSpec`: ground-state energy, energy density, local magnetization `<S_i^z>`,
  two-point correlator `<S_i^z S_j^z>`, half-chain entanglement entropy처럼 공통으로 요청할 물리량을
  표현한다.
- `ObservableResult`: 각 method-specific measurement가 `SolverResult`와 `ObservableSpec`을 소비해 만든
  값, error estimate, metadata를 담는다.
- `ComparisonReport`: benchmark point, method, observable, value, ED/exact 대비 차이, tolerance,
  skipped/partial reason을 한 표로 정렬한다.

### 12.4 First Observable Set

첫 comparison slice의 공통 물리량은 **TN과 QuadHam/BdG 양쪽에서 계산 가능한 것**으로 제한한다.

| Observable | Convention | QuadHam 계산 경로 |
|---|---|---|
| 기저에너지 `E₀` | — | quasiparticle vacuum energy 합산 |
| 에너지 밀도 `E₀/L` | — | `E₀` 나누기 `L` |
| 국소 자화 `<Si^z>` (site-resolved) | `S = σ/2`, 고유값 `±1/2` | `<Si^z> = 1/2 - <ni>`, 상관 행렬 대각 원소 |
| two-point correlator `C_c(i,j)` | connected 우선; unconnected 플롯 병기 | Wick: `<ni nj>_c = <ni nj> - <ni><nj>` |
| half-chain 얽힘 엔트로피 `S_{L/2}` | `S = -Tr(ρ ln ρ)`, nats 단위 | 상관 행렬 고유값으로 free-fermion 공식 적용 |

이 단계에서는 all-pairs correlator matrix나 full entanglement spectrum처럼 report complexity를 크게 늘리는
항목은 넣지 않는다.

### 12.5 Next Questions — Resolved (2026-06-14)

모든 항목은 2026-06-14 대화에서 확정되어 §11로 승격되었다.

1. **`L`로 통일, 자유 파라미터.** `L=6` vs `N=8` 대신 `L`을 인자로 받는다. 첫 probe 시작값은 `L=8`.
   → §11 (2026-06-14)
2. **TN: `SolverInput` + measurement contract 먼저.** TeNPy DMRG 실행은 후속 slice.
   → §11 (2026-06-14)
3. **Convention 확정.** `S = σ/2`; connected `C_c` primary, unconnected 플롯 병기; natural-log entropy nats.
   → §11 (2026-06-14)
4. **`SolverResult`는 method-specific, 통일 불가.** 각 메서드가 natural state handle 보존.
   → §11 (2026-06-14)
5. **GOVERNMENT Decision Ledger 먼저.** 이후 `PLAN.md`, `first-slice.md` 반영.
   → §11 (2026-06-14)
