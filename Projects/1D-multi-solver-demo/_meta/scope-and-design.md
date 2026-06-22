# 1D Multi-Solver Demo — 범위와 설계

## 목적과 범위

### 1. 목적과 핵심 결정

이 프로젝트는 LSWT 코드를 바로 리팩터링하기 전에, **1D spin-chain 모델을 여러 솔버로 풀면서 각 솔버가 시스템 정의에서 실제로 무엇을 읽는지** 확인하는 데모/스파이크다.

코드는 `Tensor-Network-Study` 레포 안의 새 프로젝트로 둔다.

```text
Projects/1D-multi-solver-demo/
```

이전 초안의 `Projects/XXZ_Multisolver/` 이름은 폐기한다.

이번 계획의 목적은 "범용 solver framework"를 만드는 것이 아니다. 목적은 LSWT Phase 0 설계에 필요한 seam evidence를 얻는 것이다.

핵심 결정 요약 (각 항목의 자세한 내용은 가리키는 섹션을 본다):

1. 2D 구현은 지금 계획에서 분리한다. 1D가 완성되기 전까지 2D는 생각하지 않는다 → 2, 6.
2. 구현이 쉬우면 PBC와 OBC를 모두 구현해 같은 조건에서 정확도/속도를 직접 비교한다. 구현이 어려운 method에서만 구현이 더 쉬운 쪽을 고른다 → 6.
3. 1D Hamiltonian family는 XXZ + Cluster + Zeeman term으로 둔다 → 5.
4. 첫 구현 slice는 solver benchmark가 아니라 `SpinSystem -> MethodForm` consumption probe로 고정한다 → 7, [next-actions.md](next-actions.md) 2.
5. 첫 검증은 exact reference가 분명한 지점부터 시작한다 → 9.
6. 검증된 공통 코드는 바로 승격하지 않고, 별도 결정 후 `code-space/src/`로 승격한다 → 3.
7. viewer는 단순 geometry viewer가 아니라 Hamiltonian/benchmark/결과/오차를 함께 보여주는 결과 리포트·대시보드다 → 10.

### 2. 범위와 레포 경계

작업 레포는 `/Users/david/GitHub/Tensor-Network-Study`이다.

이 계획의 구현 범위는 1D multi-solver demo다.

포함:

- 이론 문서: Hamiltonian, conventions, exact reference 위치.
- 1D chain geometry를 포함한 method-independent `SpinSystem`.
- ED, TN/DMRG, NQS, QuadHam `MethodForm` export.
- method별 consumed/required_extra/dropped/notes 기록.
- Periodic XX chain에서 QuadHam의 JW boundary-sector requirement 표면화.
- 후속 benchmark/report slice 후보 기록.

제외:

- 2D square lattice 구현.
- 2D `4x4` PBC DMRG/NQS benchmark.
- `SpinSystem -> MethodForm` probe package 경로 안에서 ED/DMRG/NQS backend solver 구현. (주: standalone 검증 스크립트로는 이미 수행됨 — [current-status.md](current-status.md) 1 참고. probe package와는 별개다.)
- 첫 probe 단계에서 `reports/`, `data/`, packaging scaffold 생성.
- LSWT 패키지 리팩터.
- 검증 전 `code-space/src/` 공통 추상화 승격.
- LSWT repo 파일 수정.

2D는 1D 구현과 리뷰가 끝난 뒤 별도 `PLAN.md` 또는 별도 섹션으로 다시 논의한다.

## 모델과 물리 설계

### 4. 기존 Cluster-Ising 자산 재사용

읽은 기준 자산:

- `Projects/Cluster_Ising/main.py`
- `Projects/Cluster_Ising/cluster_ising/solvers/base_solver.py`
- `Projects/Cluster_Ising/cluster_ising/solvers/ed_solver.py`
- `Projects/Cluster_Ising/cluster_ising/solvers/dmrg_solver.py`
- `Projects/Cluster_Ising/cluster_ising/solvers/nqs_solver.py`
- `Projects/Cluster_Ising/cluster_ising/models/cluster_ising_model.py`
- `Projects/Cluster_Ising/cluster_ising/models/exact_solution.py`
- `Projects/Cluster_Ising/tests/`

재사용할 것:

- CLI sweep 구조.
- solver dispatch 흐름.
- `SolverResult`와 `Timer`.
- 결과표와 plot panel 구성.
- optional dependency skip 방식.
- TeNPy/NetKet Hamiltonian을 ED와 비교하는 테스트 패턴.
- NQS convergence metadata 기록 방식.

새로 정리할 것:

- 1D Hamiltonian spec에서 XXZ, Cluster, Zeeman term을 on/off할 수 있게 분리.
- term별 operator convention을 명시.
- Cluster term은 spin convention(`Sx Sz Sx`, 5)으로 구현하고, 기존 Cluster-Ising의 Pauli
  결과(`K_Pauli`)와 직접 비교할 때는 `K_Pauli = K_spin / 8`로 환산해 섞이지 않도록 한다.
- PBC/OBC가 solver별로 어떻게 구현되는지 metadata에 기록.

### 5. 1D 모델 범위

전체 프로젝트는 하나의 1D Hamiltonian family 안에서 XXZ, Cluster, Zeeman term을 켜고 끌 수 있게 구축하는 것을 목표로 한다. 다만 첫 code slice는 `SpinSystem`과 method-specific `MethodForm` export에 한정한다. ED/exact benchmark와 report 산출물은 이 probe가 안정화된 뒤 후속 slice로 둔다.

#### 5.1 목표 Hamiltonian family

```text
H = H_XXZ + H_cluster + H_Zeeman

H_XXZ =
  sum_<i,j> [ Jxy (Sx_i Sx_j + Sy_i Sy_j) + Jz Sz_i Sz_j ]

H_cluster =
  - K sum_i Sx_{i-1} Sz_i Sx_{i+1}

H_Zeeman =
  - hz sum_i Sz_i - hx sum_i Sx_i
```

`H_cluster`의 형태(3-body stabilizer term `X-Z-X`) 자체는 미확정이 아니다. 기존
`Projects/Cluster_Ising/cluster_ising/models/cluster_ising_model.py`가 이미 표준 cluster-Ising
모델(PhysRevA.84.022304)을 Pauli operator `sigma` convention으로 구현해두었다.

Local operator convention은 spin operator `S = sigma/2`(고유값 `±1/2`)다. `H_XXZ`, `H_Zeeman`과
같은 convention으로 통일했다. 기존 `Cluster_Ising`의 Pauli convention 결과를 재사용/회귀검증할
때는 `K_Pauli = K_spin / 8`로 환산한다 (3-body term이므로 `(1/2)^3 = 1/8`). 결정 이력은
[decision-log.md](decision-log.md)를 본다.

#### 5.2 첫 slice: XXZ + Zeeman subset

첫 slice에서는 Cluster term을 끄고 `H_XXZ + H_Zeeman` subset만 구현한다. (지금 실제로 어디까지
구현되어 있는지는 [current-status.md](current-status.md) 2를 본다.)

기본 convention:

- `spin = 1/2`
- `Sx = sigma_x/2`
- `Sy = sigma_y/2`
- `Sz = sigma_z/2`
- `Delta = Jz / Jxy`
- `K = 0`

후보 benchmark:

- XX point: `Jxy=1`, `Jz=0`, `hz=0`, `hx=0`.
- Heisenberg AFM: `Jxy=1`, `Jz=1`, `hz=0`, `hx=0`.
- easy-plane XXZ: `Jxy=1`, `Jz=0.5`, `hz=0`, `hx=0`.
- longitudinal field: `Jxy=1`, `Jz=1`, `hz=0.5`, `hx=0`.
- transverse field seam: `Jxy=1`, `Jz=1`, `hz=0`, `hx>0`.

#### 5.3 후속 slice: Cluster term

Cluster term은 첫 slice 이후 추가한다.

역할:

- 기존 Cluster-Ising 하네스 재사용 검증.
- pure cluster limit과 Cluster-Ising critical point에서 known exact formula 또는 기존 구현 결과와 비교.
- 3-body term이 ED, TeNPy, NetKet에서 어떤 입력 형태를 요구하는지 seam evidence로 기록.

열려 있는 질문은 [next-actions.md](next-actions.md) 3을 본다.

### 6. 1D PBC/OBC 전략

원칙: 궁극적인 목표는 솔버 결과를 서로 비교하는 것이다. 구현 난이도가 낮으면 OBC와 PBC를
모두 구현해서 같은 model parameter에서 두 BC의 정확도·수렴(bond dimension, sweep count)·속도를
직접 비교한다. 이 비교 자체가 결과다. method 구현 난이도가 높아 둘 다 구현하기 어려운 경우에만
구현이 더 쉬운 쪽을 고른다.

method별 구현 난이도:

- ED: 쉽다. bond list에 `(N-1, 0)`을 넣으면 PBC가 된다.
- NetKet: 쉽다. `nk.graph.Chain(length=N, pbc=True)` 또는 explicit graph edges로 처리할 수 있다.
- TeNPy/DMRG: 쉽다. `bc_x` 플래그만 바꾸면 되므로 코드 구현 난이도는 OBC와 같다. 다만 물리적으로는
  PBC coupling이 MPO bond dimension과 수렴 난이도를 OBC보다 올린다 — 같은 정확도를 내려면 더 큰
  `chi_max`나 더 많은 sweep이 필요할 수 있다. 이 난이도 차이는 "PBC를 피해야 할 이유"가 아니라
  "OBC 대비 PBC가 얼마나 더 비싼지"를 보여주는 비교 결과로 취급한다.

실행:

1. ED, NetKet, TeNPy/DMRG 모두 OBC와 PBC를 둘 다 구현한다.
2. 같은 model parameter(`Jxy`, `Jz`, `hz`, `hx`, `L`)에서 OBC vs PBC의 energy, bond dimension,
   sweep count, wall time을 나란히 기록한다.
3. PBC DMRG가 ED/Bethe와 tight tolerance로 맞지 않거나 같은 정확도에 더 큰 `chi_max`가 필요하면
   실패를 숨기지 않고 그 차이를 seam evidence로 남긴다.
4. NQS처럼 특정 method에서 PBC graph 구성이 실제로 어려운 경우에만 예외적으로 구현이 더 쉬운
   BC 하나만 먼저 구현하고, 그 difficulty를 `MethodForm.notes`에 기록한다.

현재 standalone 검증 스크립트가 이미 이 비교의 일부를 수행했다 — `compare_xxz_solvers.py`와
`compare_xxz_observables.py`는 Bethe ansatz exact reference가 PBC로 풀이되는 해이므로 DMRG도
PBC로 맞춰 비교했고, `compare_xxz_entanglement_decay.py`는 엔트로피 스케일링(PBC)과 상관함수
decay(OBC)를 각각의 이론적 요구에 맞는 BC로 실행했다. 자세한 목록은
[current-status.md](current-status.md) 1을 본다.

## 코드/시스템 설계

### 3. 프로젝트 이름과 구조

프로젝트 경로:

```text
Projects/1D-multi-solver-demo/
```

Python package 이름:

```text
distribution/project name: 1d-multi-solver-demo
import package: one_dimensional_multi_solver_demo
```

이유:

- `pyproject.toml`의 project/distribution name은 `1d-multi-solver-demo`처럼 숫자와 kebab case를 쓸 수 있다.
- 실제 Python import package 디렉터리는 하이픈과 숫자 시작을 쓸 수 없으므로 `one_dimensional_multi_solver_demo`로 둔다.

구조 설계 판단:

- project-local package로 시작한다.
- 검증된 공통 코드는 바로 root package로 올리지 않고, 별도 결정 후 `code-space/src/`로 승격한다.
- 현재 first probe는 Cluster-Ising 스타일 benchmark harness가 아니라 system-definition consumption probe다.
- `../README.md`는 reusable model theory와 project-local execution을 연결하는 얇은 project note다.
- `progress/`는 project-local implementation slice와 lifecycle note를 둔다.
- 재사용 가능한 Hamiltonian, parameter/symbol convention, exact solution 문서는 `../../../Models/1d-spin-chains/`에서 관리한다.
- `../one_dimensional_multi_solver_demo/`는 `SpinSystem`과 `MethodForm` probe 코드를 둔다.
- `../run_method_probe.py`는 같은 `SpinSystem`을 ED, TN, NQS, QuadHam form으로 내보내며 consumption trace를 출력한다.
- `reports/`, `data/`, solver modules, `pyproject.toml`은 benchmark/report slice가 확정될 때 추가한다. 빈 placeholder directory는 만들지 않는다.

명칭 정리:

- `exact-solvable-limits.md` 같은 단일 문서보다 `../../../Models/1d-spin-chains/exact-solutions/` 폴더를 사용한다. XX chain, Heisenberg chain처럼 exact solution별로 나누어 finite-size caveat와 reference 용도를 분리하기 위해서다.
- `SpinSystem`은 method-independent physical system definition이다.
- `MethodForm`은 method-specific payload와 consumption trace를 담는 record다.
- `change_form(system, method)`는 `SpinSystem`을 ED, TN, NQS, QuadHam별 form으로 변환한다.
- `View`라는 이름은 visualization으로 오해될 수 있으므로 쓰지 않는다.
- `../run_method_probe.py`는 first probe 실행 파일이다. `run_benchmarks.py` 같은 이름은 solver benchmark slice가 생길 때 다시 결정한다.

실제 디렉터리 구조(지금 무엇이 존재하는지)는 [current-status.md](current-status.md) 1을 본다.

### 7. 데이터 흐름

```text
../../../Models/1d-spin-chains/README.md
  -> ../../../Models/1d-spin-chains/parameters-and-symbols.md
  -> ../../../Models/1d-spin-chains/conventions.md
  -> ../../../Models/1d-spin-chains/model-hamiltonian.md
  -> ../../../Models/1d-spin-chains/exact-solutions/xx-chain.md
  -> ../../../Models/1d-spin-chains/exact-solutions/tfim-chain.md
  -> ../README.md
  -> progress/open/first-slice.md
  -> ../../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md
  -> build_xxz_chain(...)
  -> SpinSystem
  -> change_form(system, method)
  -> MethodForm
  -> tests / run_method_probe.py output
```

`TheorySpec` 문서:

- Hamiltonian convention.
- spin vs Pauli convention.
- OBC/PBC 정의.
- exact solutions.
- 사용자가 결과를 보기 전에 알아야 할 기대값.

`SpinSystem`:

- method-independent physical system definition.
- `local_space`: local dimension, basis, local operator records.
- `sites`: deterministic site identity and coordinates.
- `bonds`: nearest-neighbor and boundary bond records.
- `bc`: `open` 또는 `periodic`
- `terms`: named local operator products with coefficients.
- `metadata`: current first-slice couplings and model family.

`MethodForm`:

- `method`: ED, TN, NQS, QuadHam selector.
- `status`: `ready`, `partial`, or `not_applicable`.
- `payload`: method-facing data.
- `consumed`: source fields read from `SpinSystem`.
- `required_extra`: information still needed before a backend solve.
- `dropped`: source concepts intentionally omitted from this method form.
- `notes`: seam explanation.

`SolverResult`, `ValidationReport`, tables, plots, and run summaries are deferred until the benchmark/report slice. They should consume `MethodForm` evidence rather than replacing it.

### 8. 파일 책임

#### 8.1 `../README.md`

책임:

- reusable model theory와 project-local execution을 연결한다.
- active system-definition design note와 first-slice note로 읽기 순서를 안내한다.
- 모델 이론의 정본을 프로젝트 폴더가 직접 소유하지 않는다는 boundary를 명시한다.

#### 8.2 `progress/open/first-slice.md`

책임:

- first slice의 제한 조건을 관리한다.
- 이 slice가 1D solver 완성이 아니라 method-consumption probe임을 명시한다.
- first-slice Hamiltonian subset과 benchmark 후보를 project-local로 기록한다.

#### 8.3 `../one_dimensional_multi_solver_demo/spin_system.py`

책임:

- `LocalHilbertSpace`, `Site`, `Bond`, `OperatorOnSite`, `HamiltonianTerm`, `SpinSystem`을 정의한다.
- `SpinSystem`은 method-independent source definition이어야 한다.
- 첫 probe에서는 별도 `Geometry` object를 만들지 않고 `SpinSystem`이 `sites`, `bonds`, `bc`를 직접 가진다.

#### 8.4 `../one_dimensional_multi_solver_demo/spin_models.py`

책임:

- first-slice XXZ + Zeeman spin system builder를 제공한다.
- 현재 builder는 `build_xxz_chain(...)`이다.
- Cluster term은 현재 builder에 넣지 않고 후속 cluster-term slice에서 다룬다.

#### 8.5 `../one_dimensional_multi_solver_demo/method_form.py`

책임:

- `ED`, `TN`, `NQS`, `QuadHam` method selector를 정의한다.
- `MethodForm` record를 정의한다.
- `change_form(system, method)`로 source `SpinSystem`을 method-specific payload와 consumption trace로 변환한다.
- Periodic XX chain의 `QuadHam` form은 JW fermion parity sector를 `required_extra`로 표면화해야 한다.

#### 8.6 `../run_method_probe.py`

책임:

- 하나의 shared `SpinSystem`을 만들고 ED, TN, NQS, QuadHam form으로 변환한다.
- 각 method가 소비한 field, 추가로 요구하는 정보, 버린 정보, payload key, seam note를 출력한다.
- solver benchmark CLI가 아니다.

#### 8.7 `../tests/test_method_forms.py`

책임:

- `SpinSystem`이 geometry와 terms를 method-independent하게 보존하는지 확인한다.
- ED, TN, NQS, QuadHam form이 기대한 field를 소비하고 필요한 추가 정보를 드러내는지 확인한다.
- Interacting XXZ가 `QuadHam`에서 `not_applicable`이 되는지 확인한다.

#### 8.8 `../../../Models/1d-spin-chains/parameters-and-symbols.md`

책임:

- System geometry symbol, Hamiltonian model parameter, derived quantity의 기호를 관리한다.
- 코드 field 이름과 theory symbol의 대응을 정의한다.
- 새 persistent parameter는 다른 theory 문서에서 사용하기 전에 여기서 먼저 정의한다.

#### 8.9 `../../../Models/1d-spin-chains/model-hamiltonian.md`

책임:

- 최종적으로 풀 1D Hamiltonian을 명시한다.
- XXZ, Zeeman, Cluster term의 물리적 정의를 쓴다.
- parameter/code-field mapping의 세부 표는 `parameters-and-symbols.md`로 넘긴다.

#### 8.10 `../../../Models/1d-spin-chains/conventions.md`

책임:

- spin operator와 Pauli operator convention을 분리한다.
- sign convention, site indexing, OBC/PBC convention을 정리한다.
- Hamiltonian 문서와 exact solution 문서가 같은 convention을 쓰도록 연결한다.

#### 8.11 `../../../Models/1d-spin-chains/exact-solutions/`

책임:

- exact solution을 한 파일에 몰아넣지 않고 solution family별로 나눈다.
- `README.md`: exact solution 문서들의 용도와 공통 convention.
- `method/README.md`: method 문서들의 읽기 순서와 역할 구분.
- `method/bethe-ansatz.md`: Bethe ansatz method와 Heisenberg thermodynamic anchor.
- `method/jordan-wigner.md`: Jordan-Wigner transformation method.
- `method/free-fermion-diagonalization.md`: free-fermion diagonalization method.
- `method/bogoliubov-diagonalization.md`: Bogoliubov diagonalization method.
- `xx-chain.md`: XX point finite-L/PBC reference.
- `xxz-chain.md`: XXZ finite-L/thermodynamic-limit reference.
- `tfim-chain.md`: transverse-field Ising limit reference.

#### 8.12 `reports/findings.md`

standalone 검증 스크립트(`verify_xxz_bethe.py`, `compare_xxz_solvers.py`,
`compare_xxz_observables.py`, `compare_xxz_entanglement_decay.py`)가 만든 figure를 모은 findings
초안이다. package의 `MethodForm`을 거치지 않은 결과이므로 잠정적인 evidence로 취급한다. 자세한
범위와 한계는 [reports/findings.md](../reports/findings.md) 5를 본다.

#### 8.13 `build_dashboard.py` / `reports/dashboard.html`

`build_dashboard.py`는 `xxz_solver_comparison.csv`, `xxz_observables_comparison.csv`,
`xxz_entanglement_decay.csv`를 읽어 `reports/dashboard.html`을 만든다. Chart.js CDN만 불러오고
나머지는 self-contained라 로컬 서버 없이 브라우저로 바로 열 수 있다. CSV가 바뀌면
`python3 build_dashboard.py`로 다시 만들어야 한다 — 자동으로 갱신되지 않는다.

#### 8.14 Deferred benchmark/report files

아래 파일과 directory는 full benchmark/report slice가 확정될 때 추가한다. 현재 first probe에서는 만들지 않는다.

- `pyproject.toml`, `requirements.txt`
- `run_benchmarks.py`
- `data/`
- `exact_solutions.py`, `validation.py`
- `solvers/`
- `reporting/`
- `visualization/`

## 검증과 산출물

### 9. Exact solution과 validation 기준

#### 9.1 Cluster-Ising

기준:

- 기존 Cluster-Ising exact solution을 재사용한다.
- 기존 ED/DMRG/NQS 결과와 새 demo 결과가 regression 없이 맞는지 본다.

극단:

- `lambda=0`
- `lambda=1`
- `lambda>1`

#### 9.2 XXZ

기준:

- XX point finite-L PBC는 ED와 machine precision 비교.
- XX thermodynamic limit은 `-1/pi`.
- Heisenberg thermodynamic limit은 `1/4 - log(2)`.
- Heisenberg finite `L=8`은 위 값과 같다고 주장하지 않고 수렴 anchor로만 사용한다.

주의:

- Yang-Yang 일반식은 출처 확인 전까지 구현 기준으로 쓰지 않는다.
- spin/Pauli normalization 차이를 validation table에 명시한다.

Observable convention (확정):

- Spin operator: `S = σ/2`. `Sz` 고유값 `±1/2`.
- Two-point correlator: connected `C_c(i,j) = <Si^z Sj^z> - <Si^z><Sj^z>` primary; unconnected 플롯 병기.
- 얽힘 엔트로피: `S = -Tr(ρ ln ρ)`, nats 단위 (TeNPy default).
- Observable set은 TN과 QuadHam/BdG 양쪽에서 계산 가능한 것으로 제한한다.

#### 9.3 초기 tolerance

- ED vs exact finite-L: `abs(dE/L) <= 1e-12`.
- DMRG OBC vs ED: 목표 `abs(dE/L) <= 1e-6`.
- DMRG PBC vs ED: 목표를 낮게 잡거나 exploratory로 기록한다. 확정 tolerance는 구현 결과를 보고 조정한다.
- NQS vs ED: 상대오차 약 `1%`, variance와 seed 기록 필수.

#### 9.4 검증 지점(benchmark point)의 의미

`benchmark point`는 검증을 실행하는 하나의 구체적인 물리 설정이다. 문서 안에서는 짧게 `BP`로 표기할 수 있다. 단순히 `Delta=0` 같은 parameter 값 하나만 뜻하지 않는다.

하나의 benchmark point는 최소한 다음을 포함한다.

- model family: 예, `xxz`.
- system size: 예, `L=8`. L은 자유 파라미터이며 코드는 L을 인자로 받는다. 첫 probe 시작값은 L=8.
- boundary condition: 예, `PBC` 또는 `OBC`.
- couplings/fields: 예, `Jxy=1`, `Jz=0`, `hz=0`, `hx=0`.
- solver set: 예, 첫 slice에서는 `exact`, `ed`.
- reference: 예, XX finite-L free-fermion exact value.
- pass/fail criterion: 예, `abs(dE/L) <= 1e-12`.

후속 benchmark/report slice의 benchmark point는 XXZ 1D ED/exact/geometry에 한정해 시작한다. 아래 두 항목은 현재 후보이며, `../../../Models/1d-spin-chains/exact-solutions/` 작성 과정에서 수정될 수 있다. 현재 method-consumption probe는 이 benchmark를 실행하지 않고, 같은 물리 설정을 method form으로 내보낼 수 있는지 먼저 확인한다.

```text
BP-XXZ-1:
  model = XXZ
  geometry = 1D chain
  L = 8
  bc = periodic
  Jxy = 1
  Jz = 0
  Delta = 0
  hz = 0
  hx = 0
  solvers = exact, ed
  purpose = XX finite-L exact reference와 ED convention 검증

BP-XXZ-2:
  model = XXZ
  geometry = 1D chain
  L = 8
  bc = periodic
  Jxy = 1
  Jz = 1
  Delta = 1
  hz = 0
  hx = 0
  solvers = ed
  reference = thermodynamic anchor 1/4 - log(2)
  purpose = finite-L 값과 thermodynamic-limit anchor를 구분해 기록
```

`BP-XXZ-2`는 ED와 thermodynamic-limit 값을 같다고 판정하는 테스트가 아니다. finite-size 차이를 의도적으로 보여주는 기준점이다.

### 11. Seam 기록 방식

S1~S5를 1D에서 먼저 기록한다. 현재 first probe에서는 `MethodForm.consumed`, `MethodForm.required_extra`, `MethodForm.dropped`, `MethodForm.notes`, `../tests/test_method_forms.py`, `../run_method_probe.py` output이 seam evidence의 source다.

- S1 Term operator content: numeric coupling, named operator, raw matrix.
- S2 LocalSpace: Pauli/spin convention, local dimension, charge conservation.
- S3 Geometry: OBC/PBC bond list, MPS order, NetKet graph.
- S4 Magnetic order: 1D ED/DMRG/NQS는 magnetic order input이 필요 없는지.
- S5 Observable/result schema: energy 공통화와 solver-specific state/metadata 차이.

후속 benchmark/report slice의 프로젝트 내부 findings 초안 후보:

```text
Projects/1D-multi-solver-demo/reports/findings.md
```

LSWT 승격 위치는 method-consumption probe와 후속 benchmark 결과를 보고 판단한다. 지금은 정하지 않는다.

### 10. 결과 리포트/대시보드 항목

후속 viewer/report는 단순히 geometry를 보여주는 도구가 아니다. 사용자가 solver 결과를 해석할 수 있도록 theory, benchmark point, numerical result, error, solver metadata를 한 곳에서 보여주는 리포트/대시보드 역할을 한다. (현재 method-consumption probe가 지금 보여주는 항목은 [current-status.md](current-status.md) 1을 본다.)

#### 10.1 후속 benchmark/report slice에서 보여줄 항목

표:

- Hamiltonian convention summary.
- benchmark point summary.
- geometry summary: `N`, `bc`, sites, bonds, PBC edge.
- exact reference table.
- ED energy table: total energy, energy per site.
- exact vs ED error table.

플롯/그림:

- 1D chain geometry diagram: site index, bonds, PBC edge.
- energy per site comparison: exact vs ED.
- absolute error plot 또는 compact error marker.
- Heisenberg thermodynamic anchor comparison: ED finite-L value와 `1/4 - log(2)`를 같은 값으로 판정하지 않고 reference line/annotation으로 표시.

문서/리포트:

- `reports/theory-summary.md`: Hamiltonian과 exact limit 요약.
- `reports/run-summary.md`: benchmark/report slice 실행 결과 요약.

#### 10.2 후속 solver slice에서 확장할 항목

LSWT:

- assumed classical order 또는 reference state.
- LSWT가 요구한 추가 system input.
- ED/exact 대비 energy 또는 qualitative comparison.

TN/DMRG:

- energy per site.
- ED 대비 error.
- bond dimension.
- sweep count.
- truncation metadata.
- OBC/PBC 차이.

NQS:

- final energy estimate.
- ED 대비 error.
- energy variance.
- convergence history.
- seed, samples, iterations.

공통:

- solver wall time.
- skipped solver와 이유.
- solver-specific state type.
- S1~S5 seam evidence 링크.

## 리스크

### 12. 알려진 리스크

- DMRG/MPS에서 PBC는 OBC보다 어렵다.
- PBC DMRG를 tight tolerance 기준으로 두면 초기 구현이 불안정해질 수 있다.
- Cluster term을 spin convention으로 결정했지만(5), 기존 Cluster-Ising 결과(Pauli)와 비교할 때 `K_Pauli = K_spin / 8` 환산을 빠뜨리면 여전히 convention이 섞일 수 있다.
- NetKet/JAX 설치와 실행이 무거울 수 있다.
- 기존 Cluster-Ising 코드를 새 demo로 옮길 때 regression이 생길 수 있다.
- LSWT 승격 위치를 미리 정하면 실제 산출물 성격과 어긋날 수 있다.
