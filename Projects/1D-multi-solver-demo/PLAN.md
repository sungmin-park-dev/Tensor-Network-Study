# 1D Multi-Solver Demo 계획서

상태: 1차 확정  
확정 기록: 사용자가 "plan.md는 1차로 완성되었다. 확정되었다"라고 명시함  
운영 규칙: 구현은 이 문서의 Roadmap과 11장 구현 순서를 따른다. 계획에서 벗어나는 범위 확장은 별도 확인 후 진행한다.

## 0. 전체 요약과 리뷰 지도

### 0.1 전체 요약

이 프로젝트는 LSWT 코드를 바로 리팩터링하기 전에, **1D spin-chain 모델을 여러 솔버로 풀면서 각 솔버가 시스템 정의에서 실제로 무엇을 읽는지** 확인하는 데모/스파이크다.

코드는 `Tensor-Network-Study` 레포 안의 새 프로젝트로 둔다.

```text
Projects/1D-multi-solver-demo/
```

이전 초안의 `Projects/XXZ_Multisolver/` 이름은 폐기한다.

핵심 결정:

- 2D 구현은 지금 계획에서 분리한다.
- 1D가 완성되기 전까지 2D `4x4` PBC는 생각하지 않는다.
- 첫 구현은 project-local package 안에만 둔다. 검증된 공통 코드는 별도 결정 후 `code-space/src/`로 승격한다.
- 후속 benchmark/report slice에서는 기존 `Projects/Cluster_Ising` 하네스의 CLI, solver dispatch, 결과표, 플롯, TeNPy/NetKet 패턴을 재사용한다.
- 최종 목표는 XXZ, Cluster, Zeeman term 조합을 같은 1D 하네스에서 동시 실행 가능하게 만드는 것이다.
- 첫 구현 slice는 solver benchmark부터 시작하지 않는다. 먼저 이론 문서와 system-definition 논의를 고정하고, `SpinSystem -> MethodForm` consumption probe를 project-local code로 구현한다.

이번 계획의 목적은 "범용 solver framework"를 만드는 것이 아니다. 목적은 LSWT Phase 0 설계에 필요한 seam evidence를 얻는 것이다.

### 0.2 현재 가장 중요한 설계 판단

1. **1D 우선**
   2D는 별도 후속 계획으로 둔다. 1D에서 geometry, Hamiltonian convention, ED/DMRG/NQS validation, exact benchmark, result schema가 안정화되기 전에는 2D로 가지 않는다.

2. **PBC는 가능하지만 DMRG/TN에서는 쉬운 기본값이 아니다**
   ED와 NetKet에서 1D PBC는 explicit edge만 넣으면 비교적 쉽다. 반면 MPS/DMRG에서는 OBC가 자연스럽고 PBC 또는 boundary coupling은 더 비싸고 수렴이 까다롭다. TeNPy 같은 일반 패키지로 1D PBC Hamiltonian/MPO를 만들 수는 있지만, DMRG 정확도와 효율은 OBC보다 불리하다.

3. **기술적으로 구현은 가능하다**
   `L=8` 같은 작은 1D PBC는 ED 기준 검증, NetKet graph, TeNPy MPO/DMRG 실험 모두 구현 가능하다. 다만 DMRG PBC는 "쉬운 벤치마크 기본값"으로 취급하지 않고, OBC와 PBC를 나누어 seam evidence로 기록해야 한다.

4. **1D Hamiltonian family는 XXZ + Cluster + Zeeman으로 둔다**
   이 프로젝트에서 생각하는 1D Hamiltonian은 XXZ interaction, Cluster term, Zeeman field를 포함하는 family다. 첫 slice에서는 exact solution이 분명한 XXZ limit부터 확인하고, 이후 Cluster term과 Zeeman term을 같은 Hamiltonian spec 안에 켠다.

5. **첫 구현 slice는 `SpinSystem -> MethodForm` consumption probe로 고정한다**
   첫 단계는 같은 physical system definition이 ED, TN/DMRG, NQS, QuadHam에서 어떤 form으로 갈라지는지 기록하는 것이다. Exact/ED benchmark, report, TeNPy/NetKet 실행은 이 probe가 안정화된 뒤 후속 slice로 둔다.

6. **우선 exact-solvable 모델 위주로 확인한다**
   여러 모델을 동시에 돌릴 수 있는 하네스가 최종 목적이지만, 첫 검증은 exact reference가 분명한 지점부터 시작한다. 즉, XXZ의 XX point와 Heisenberg thermodynamic anchor처럼 해석적 기준이 있는 설정을 먼저 확인한다.

7. **viewer는 단순 geometry viewer가 아니라 결과 리포트/대시보드다**
   geometry 그림은 viewer의 한 패널일 뿐이다. 최종 viewer/report는 Hamiltonian convention, benchmark point, exact/ED/LSWT/TN/NQS 결과표, 에너지/오차/수렴 플롯을 함께 보여주는 산출물로 설계한다.

### 0.3 섹션별 핵심과 현재 상태

| 섹션 | 핵심 | 현재 상태 |
|---|---|---|
| 1. 범위와 경계 | 1D demo만 수행, 2D는 후속 | 결정됨: 1D 완성 전까지 2D 제외 |
| 2. 프로젝트 이름/구조 | `Projects/1D-multi-solver-demo/` | 결정됨: 코드 위치는 이 프로젝트 내부 |
| 3. 기존 자산 재사용 | Cluster-Ising 하네스의 흐름 재사용 | 결정됨: 복사보다 얇은 재사용/회귀검증 중심 |
| 4. 1D 모델 범위 | XXZ + Cluster + Zeeman Hamiltonian family | 결정됨: exact-solvable 지점 우선 |
| 5. PBC/OBC 전략 | ED/NetKet PBC 쉬움, DMRG PBC는 seam으로 기록 | 결정됨: DMRG는 OBC primary, PBC exploratory |
| 6. 데이터 흐름 | `TheorySpec -> SpinSystem -> MethodForm -> consumption trace` | 유지: solver 실행보다 method consumption 기록을 먼저 고정 |
| 7. 파일 책임 | model theory / progress / probe code를 분리 | 결정됨: reusable model theory는 `Models/`, project-local progress는 `progress/` |
| 8. exact solution/validation | 각 term 조합의 검증 가능한 극단을 분리 | 유지: benchmark 후보는 남기되 code probe는 MethodForm 중심 |
| 9. 리포트/대시보드 | 보여줄 물리량과 플롯 항목을 후속 slice로 둔다 | deferred: viewer는 결과 리포트 역할 |
| 10. seam 기록 | S1~S5를 1D에서 먼저 정리 | 유지: 2D 없이 1D evidence부터 작성 |
| 11. 승인 후 구현 순서 | plan 확정 뒤 1D만 구현 | 결정됨: 첫 slice는 theory docs부터 시작 |

### 0.4 이번 응답으로 반영된 결정

1. 프로젝트 경로는 `Projects/1D-multi-solver-demo/`로 둔다.
2. 패키징 이름은 숫자와 kebab case를 살린 `1d-multi-solver-demo`로 둔다.
3. Python import package 디렉터리는 Python 문법 제약 때문에 `one_dimensional_multi_solver_demo`로 둔다.
4. 첫 구현 slice는 이론 문서, system-definition issue note, `SpinSystem`, `MethodForm`, `run_method_probe.py`, `test_method_forms.py` 순서로 진행한다.
5. XXZ, Cluster, Zeeman term은 최종적으로 같은 1D system family에서 on/off 가능해야 하지만, 현재 code probe는 XXZ + Zeeman subset과 method consumption trace에 한정한다.
6. `benchmark point`는 `검증 지점(benchmark point)`으로 풀어 쓰며, 아래 8.4에서 정의한다.
7. 첫 slice의 검증 지점 초안은 두 개다. 이 내용은 theory 문서와 exact reference 정리 과정에서 변경될 수 있다.
   - `BP-XXZ-1`: `L=8` PBC, `Delta=0`, XX free-fermion finite-L exact value와 ED 비교.
   - `BP-XXZ-2`: `L=8` PBC, `Delta=1`, ED finite-L 값과 Heisenberg thermodynamic anchor `1/4 - log(2)`를 구분해 기록.
8. Cluster term convention은 지금 확정하지 않고 `../../Models/1d-spin-chains/model-hamiltonian.md` 작성 중에 다시 검토한다.

### 0.5 Roadmap

1. **Theory And System Definition**
   최종적으로 풀 Hamiltonian과 first-slice system-definition boundary를 명시한다. sign convention, spin vs Pauli convention, OBC/PBC 정의, exact solution reference 위치를 문서화한다.

2. **Method-Consumption Probe**
   `SpinSystem`을 만들고 `change_form(system, ED/TN/NQS/QuadHam)`가 어떤 source field를 소비하고 어떤 추가 정보를 요구하는지 기록한다.

3. **Exact Crosscheck Spec**
   구현 전에 exact reference와 validation 기준을 먼저 고정한다. 현재 후보는 `BP-XXZ-1`과 `BP-XXZ-2`지만, theory 문서 작성 중 변경될 수 있다.

4. **Expected Results / Report Spec**
   사용자가 계산 결과를 보기 전에 알아야 할 기대값, 물리량, 표, 플롯 항목을 정한다. 이 단계에서 viewer/report의 형태도 정한다.

5. **ED Baseline**
   1D chain geometry와 Hamiltonian construction을 구현하고, ED로 finite-L 기준값을 만든 뒤 exact 기준과 비교한다.

6. **LSWT Approximation**
   1D spin-1/2 XXZ에서 LSWT는 정답 solver가 아니라 approximation/seam probe로 취급한다. ED/exact 기준을 먼저 확보한 뒤, LSWT가 어떤 system input을 요구하는지 확인한다.

7. **TN / DMRG**
   OBC를 primary benchmark로 두고, PBC는 exploratory seam probe로 기록한다.

8. **NQS**
   energy estimate, variance, convergence history, seed를 포함해 stochastic solver 결과 스키마를 확인한다.

9. **Findings**
   1D에서 얻은 S1~S5 seam evidence를 정리하고, 2D 확장 및 LSWT 승격 위치는 결과를 보고 판단한다.

## 1. 범위와 레포 경계

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
- 첫 probe 단계에서 ED/DMRG/NQS backend solver 구현.
- 첫 probe 단계에서 `reports/`, `data/`, packaging scaffold 생성.
- LSWT 패키지 리팩터.
- 검증 전 `code-space/src/` 공통 추상화 승격.
- LSWT repo 파일 수정.

2D는 1D 구현과 리뷰가 끝난 뒤 별도 `PLAN.md` 또는 별도 섹션으로 다시 논의한다.

## 2. 프로젝트 이름과 구조

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

현재 first-probe 구조:

```text
Projects/1D-multi-solver-demo/
  PLAN.md
  README.md
  run_method_probe.py

  progress/
    open/
      first-slice.md
    close/
      README.md

  writing-guidelines.md

  one_dimensional_multi_solver_demo/
    __init__.py
    spin_system.py
    spin_models.py
    method_form.py

  tests/
    test_method_forms.py
```

현재 판단:

- project-local package로 시작한다.
- 검증된 공통 코드는 바로 root package로 올리지 않고, 별도 결정 후 `code-space/src/`로 승격한다.
- 현재 first probe는 Cluster-Ising 스타일 benchmark harness가 아니라 system-definition consumption probe다.
- `README.md`는 reusable model theory와 project-local execution을 연결하는 얇은 project note다.
- `progress/`는 project-local implementation slice와 lifecycle note를 둔다.
- 재사용 가능한 Hamiltonian, parameter/symbol convention, exact solution 문서는 `../../Models/1d-spin-chains/`에서 관리한다.
- `one_dimensional_multi_solver_demo/`는 `SpinSystem`과 `MethodForm` probe 코드를 둔다.
- `run_method_probe.py`는 같은 `SpinSystem`을 ED, TN, NQS, QuadHam form으로 내보내며 consumption trace를 출력한다.
- `reports/`, `data/`, solver modules, `pyproject.toml`은 benchmark/report slice가 확정될 때 추가한다. 빈 placeholder directory는 만들지 않는다.

명칭 정리:

- `exact-solvable-limits.md` 같은 단일 문서보다 `../../Models/1d-spin-chains/exact-solutions/` 폴더를 사용한다. XX chain, Heisenberg chain처럼 exact solution별로 나누어 finite-size caveat와 reference 용도를 분리하기 위해서다.
- `SpinSystem`은 method-independent physical system definition이다.
- `MethodForm`은 method-specific payload와 consumption trace를 담는 record다.
- `change_form(system, method)`는 `SpinSystem`을 ED, TN, NQS, QuadHam별 form으로 변환한다.
- `View`라는 이름은 visualization으로 오해될 수 있으므로 쓰지 않는다.
- `run_method_probe.py`는 first probe 실행 파일이다. `run_benchmarks.py` 같은 이름은 solver benchmark slice가 생길 때 다시 결정한다.

## 3. 기존 Cluster-Ising 자산 재사용

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
- Cluster term의 Pauli convention과 XXZ spin convention을 섞지 않도록 방어.
- PBC/OBC가 solver별로 어떻게 구현되는지 metadata에 기록.

## 4. 1D 모델 범위

전체 프로젝트는 하나의 1D Hamiltonian family 안에서 XXZ, Cluster, Zeeman term을 켜고 끌 수 있게 구축하는 것을 목표로 한다. 다만 현재 first code slice는 `SpinSystem`과 method-specific `MethodForm` export에 한정한다. ED/exact benchmark와 report 산출물은 이 probe가 안정화된 뒤 후속 slice로 둔다.

### 4.1 목표 Hamiltonian family

후보 Hamiltonian:

```text
H = H_XXZ + H_cluster + H_Zeeman

H_XXZ =
  sum_<i,j> [ Jxy (Sx_i Sx_j + Sy_i Sy_j) + Jz Sz_i Sz_j ]

H_cluster =
  - K sum_i O^x_{i-1} O^z_i O^x_{i+1}

H_Zeeman =
  - hz sum_i Sz_i - hx sum_i Sx_i
```

여기서 `O`는 Cluster term의 local operator convention을 아직 확정하지 않은 placeholder다. 기존 Cluster-Ising 코드는 Pauli operator `sigma` convention을 사용한다. XXZ term은 spin operator `S = sigma/2` convention을 사용한다. 두 convention을 한 Hamiltonian 안에서 어떻게 통일할지는 확인이 필요하다.

### 4.2 첫 slice: XXZ + Zeeman subset

첫 slice에서는 Cluster term을 끄고 `H_XXZ + H_Zeeman` subset만 구현한다.

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

### 4.3 후속 slice: Cluster term

Cluster term은 첫 slice 이후 추가한다.

역할:

- 기존 Cluster-Ising 하네스 재사용 검증.
- pure cluster limit과 Cluster-Ising critical point에서 known exact formula 또는 기존 구현 결과와 비교.
- 3-body term이 ED, TeNPy, NetKet에서 어떤 입력 형태를 요구하는지 seam evidence로 기록.

확인 필요:

- Cluster term을 기존 Cluster-Ising처럼 Pauli operator `sigma^x sigma^z sigma^x`로 둘지, spin operator `Sx Sz Sx`로 재정규화할지.
- Cluster coupling 기호를 `K`, `J_cluster`, `Jc` 중 무엇으로 쓸지.

## 5. 1D PBC/OBC 전략

질문: 1D chain `L=8` PBC가 TN에서 쉬운가?

답:

- ED에서는 쉽다. bond list에 `(N-1, 0)`을 넣으면 된다.
- NetKet에서도 쉽다. `nk.graph.Chain(length=N, pbc=True)` 또는 explicit graph edges로 처리할 수 있다.
- TeNPy/DMRG에서는 가능하지만 OBC보다 어렵다. MPS는 OBC에 자연스럽고, PBC coupling은 MPO bond dimension과 수렴 난이도를 올린다. TeNPy가 PBC lattice/coupling을 지원하더라도 DMRG benchmark의 안정 기본값으로 두기에는 OBC보다 불리하다.

기술적 판단:

- `L=8` PBC는 구현 가능하다.
- 하지만 DMRG 정확도 목표를 처음부터 PBC에 강하게 걸면 계획 리스크가 불필요하게 커진다.
- 따라서 1D 구현은 OBC와 PBC를 분리한다.

제안:

1. OBC를 DMRG 안정성 기준으로 사용한다.
2. PBC는 ED/NetKet/exact 기준을 먼저 확인한다.
3. TeNPy PBC 또는 boundary coupling은 seam probe로 구현하고, 성능/정확도/수렴 차이를 기록한다.
4. PBC DMRG가 ED와 tight tolerance로 맞지 않으면 실패를 숨기지 않고 seam evidence로 남긴다.

## 6. 데이터 흐름

현재 first-probe 흐름:

```text
../../Models/1d-spin-chains/README.md
  -> ../../Models/1d-spin-chains/parameters-and-symbols.md
  -> ../../Models/1d-spin-chains/conventions.md
  -> ../../Models/1d-spin-chains/model-hamiltonian.md
  -> ../../Models/1d-spin-chains/exact-solutions/xx-chain.md
  -> ../../Models/1d-spin-chains/exact-solutions/tfim-chain.md
  -> README.md
  -> progress/open/first-slice.md
  -> GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md
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

## 7. 파일 책임

### 7.1 `README.md`

책임:

- reusable model theory와 project-local execution을 연결한다.
- active system-definition design note와 first-slice note로 읽기 순서를 안내한다.
- 모델 이론의 정본을 프로젝트 폴더가 직접 소유하지 않는다는 boundary를 명시한다.

### 7.2 `progress/open/first-slice.md`

책임:

- first slice의 제한 조건을 관리한다.
- 이 slice가 1D solver 완성이 아니라 method-consumption probe임을 명시한다.
- first-slice Hamiltonian subset과 benchmark 후보를 project-local로 기록한다.

### 7.3 `one_dimensional_multi_solver_demo/spin_system.py`

책임:

- `LocalHilbertSpace`, `Site`, `Bond`, `OperatorOnSite`, `HamiltonianTerm`, `SpinSystem`을 정의한다.
- `SpinSystem`은 method-independent source definition이어야 한다.
- 첫 probe에서는 별도 `Geometry` object를 만들지 않고 `SpinSystem`이 `sites`, `bonds`, `bc`를 직접 가진다.

### 7.4 `one_dimensional_multi_solver_demo/spin_models.py`

책임:

- first-slice XXZ + Zeeman spin system builder를 제공한다.
- 현재 builder는 `build_xxz_chain(...)`이다.
- Cluster term은 현재 builder에 넣지 않고 후속 cluster-term slice에서 다룬다.

### 7.5 `one_dimensional_multi_solver_demo/method_form.py`

책임:

- `ED`, `TN`, `NQS`, `QuadHam` method selector를 정의한다.
- `MethodForm` record를 정의한다.
- `change_form(system, method)`로 source `SpinSystem`을 method-specific payload와 consumption trace로 변환한다.
- Periodic XX chain의 `QuadHam` form은 JW fermion parity sector를 `required_extra`로 표면화해야 한다.

### 7.6 `run_method_probe.py`

책임:

- 하나의 shared `SpinSystem`을 만들고 ED, TN, NQS, QuadHam form으로 변환한다.
- 각 method가 소비한 field, 추가로 요구하는 정보, 버린 정보, payload key, seam note를 출력한다.
- solver benchmark CLI가 아니다.

### 7.7 `tests/test_method_forms.py`

책임:

- `SpinSystem`이 geometry와 terms를 method-independent하게 보존하는지 확인한다.
- ED, TN, NQS, QuadHam form이 기대한 field를 소비하고 필요한 추가 정보를 드러내는지 확인한다.
- Interacting XXZ가 `QuadHam`에서 `not_applicable`이 되는지 확인한다.

### 7.8 `../../Models/1d-spin-chains/parameters-and-symbols.md`

책임:

- System geometry symbol, Hamiltonian model parameter, derived quantity의 기호를 관리한다.
- 코드 field 이름과 theory symbol의 대응을 정의한다.
- 새 persistent parameter는 다른 theory 문서에서 사용하기 전에 여기서 먼저 정의한다.

### 7.9 `../../Models/1d-spin-chains/model-hamiltonian.md`

책임:

- 최종적으로 풀 1D Hamiltonian을 명시한다.
- XXZ, Zeeman, Cluster term의 물리적 정의를 쓴다.
- parameter/code-field mapping의 세부 표는 `parameters-and-symbols.md`로 넘긴다.

### 7.10 `../../Models/1d-spin-chains/conventions.md`

책임:

- spin operator와 Pauli operator convention을 분리한다.
- sign convention, site indexing, OBC/PBC convention을 정리한다.
- Hamiltonian 문서와 exact solution 문서가 같은 convention을 쓰도록 연결한다.

### 7.11 `../../Models/1d-spin-chains/exact-solutions/`

책임:

- exact solution을 한 파일에 몰아넣지 않고 solution family별로 나눈다.
- `README.md`: exact solution 문서들의 용도와 공통 convention.
- `method/bethe-ansatz.md`: Bethe ansatz method와 Heisenberg thermodynamic anchor.
- `method/jordan-wigner.md`: Jordan-Wigner transformation method.
- `xx-chain.md`: XX point finite-L/PBC reference.
- `tfim-chain.md`: transverse-field Ising limit reference.

### 7.12 Deferred benchmark/report files

아래 파일과 directory는 full benchmark/report slice가 확정될 때 추가한다. 현재 first probe에서는 만들지 않는다.

- `pyproject.toml`, `requirements.txt`
- `run_benchmarks.py`
- `reports/`
- `data/`
- `exact_solutions.py`, `validation.py`
- `solvers/`
- `reporting/`
- `visualization/`

## 8. exact solution과 validation 기준

### 8.1 Cluster-Ising

기준:

- 기존 Cluster-Ising exact solution을 재사용한다.
- 기존 ED/DMRG/NQS 결과와 새 demo 결과가 regression 없이 맞는지 본다.

극단:

- `lambda=0`
- `lambda=1`
- `lambda>1`

### 8.2 XXZ

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

### 8.3 초기 tolerance

- ED vs exact finite-L: `abs(dE/L) <= 1e-12`.
- DMRG OBC vs ED: 목표 `abs(dE/L) <= 1e-6`.
- DMRG PBC vs ED: 목표를 낮게 잡거나 exploratory로 기록한다. 확정 tolerance는 구현 결과를 보고 조정한다.
- NQS vs ED: 상대오차 약 `1%`, variance와 seed 기록 필수.

### 8.4 검증 지점(benchmark point)의 의미

`benchmark point`는 검증을 실행하는 하나의 구체적인 물리 설정이다. 문서 안에서는 짧게 `BP`로 표기할 수 있다. 단순히 `Delta=0` 같은 parameter 값 하나만 뜻하지 않는다.

하나의 benchmark point는 최소한 다음을 포함한다.

- model family: 예, `xxz`.
- system size: 예, `L=8`. L은 자유 파라미터이며 코드는 L을 인자로 받는다. 첫 probe 시작값은 L=8.
- boundary condition: 예, `PBC` 또는 `OBC`.
- couplings/fields: 예, `Jxy=1`, `Jz=0`, `hz=0`, `hx=0`.
- solver set: 예, 첫 slice에서는 `exact`, `ed`.
- reference: 예, XX finite-L free-fermion exact value.
- pass/fail criterion: 예, `abs(dE/L) <= 1e-12`.

후속 benchmark/report slice의 benchmark point는 XXZ 1D ED/exact/geometry에 한정해 시작한다. 아래 두 항목은 현재 후보이며, `../../Models/1d-spin-chains/exact-solutions/` 작성 과정에서 수정될 수 있다. 현재 method-consumption probe는 이 benchmark를 실행하지 않고, 같은 물리 설정을 method form으로 내보낼 수 있는지 먼저 확인한다.

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

## 9. 결과 리포트/대시보드 항목

후속 viewer/report는 단순히 geometry를 보여주는 도구가 아니다. 사용자가 solver 결과를 해석할 수 있도록 theory, benchmark point, numerical result, error, solver metadata를 한 곳에서 보여주는 리포트/대시보드 역할을 한다.

### 9.1 현재 method-consumption probe에서 보여줄 항목

현재 first probe는 numerical result report가 아니라 method form trace를 출력한다.

- shared `SpinSystem` summary: model name, length, boundary condition, bond list.
- ED form: consumed fields, payload keys, many-body basis/local matrix requirement.
- TN form: named operator, bond, MPO-friendly term requirement.
- NQS form: graph, Hilbert, local operator split plus stochastic metadata requirement.
- QuadHam form: free-fermion hopping form, `not_applicable` 또는 `partial` status, JW boundary-sector requirement.
- Tests: each method form's status, required_extra, dropped fields, and key payload content.

### 9.2 후속 benchmark/report slice에서 보여줄 항목

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

### 9.3 후속 solver slice에서 확장할 항목

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

## 10. seam 기록 방식

S1~S5를 1D에서 먼저 기록한다. 현재 first probe에서는 `MethodForm.consumed`, `MethodForm.required_extra`, `MethodForm.dropped`, `MethodForm.notes`, `tests/test_method_forms.py`, `run_method_probe.py` output이 seam evidence의 source다.

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

## 11. 승인 후 구현 순서

이 섹션은 1차 확정 이후의 실행 기준이다.

### 11.1 첫 구현 slice: theory docs + system definition + MethodForm probe

1. `../../Models/1d-spin-chains/README.md`: reusable model theory의 읽기 순서와 각 문서 책임을 정리.
2. `../../Models/1d-spin-chains/parameters-and-symbols.md`: parameter, symbol, code field naming을 분리해 정의.
3. `../../Models/1d-spin-chains/conventions.md`: spin/Pauli, sign, site indexing, OBC/PBC convention을 정리.
4. `../../Models/1d-spin-chains/model-hamiltonian.md`: 최종적으로 풀 XXZ + Cluster + Zeeman 1D Hamiltonian을 작성.
5. `../../Models/1d-spin-chains/exact-solutions/README.md`: exact solution 문서들의 공통 convention과 사용 목적을 정리.
6. `../../Models/1d-spin-chains/exact-solutions/xx-chain.md`: XX point finite-L reference를 정리.
7. `README.md`: reusable model theory와 project-local execution의 연결을 정리.
8. `GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md`: `SpinSystem`, method selector, `MethodForm`, `change_form` split을 논의한다.
9. `progress/open/first-slice.md`: 첫 slice의 구현 범위와 benchmark 후보를 확정하되, 현재 code probe가 solver benchmark가 아님을 명시한다.
10. `one_dimensional_multi_solver_demo/spin_system.py`: method-independent system data structures를 구현한다.
11. `one_dimensional_multi_solver_demo/spin_models.py`: first-slice XXZ + Zeeman `SpinSystem` builder를 구현한다.
12. `one_dimensional_multi_solver_demo/method_form.py`: ED, TN, NQS, QuadHam `MethodForm` export를 구현한다.
13. `run_method_probe.py`: method consumption trace를 출력한다.
14. `tests/test_method_forms.py`: method form behavior와 QuadHam boundary/interaction cases를 검증한다.
15. 이 probe 결과를 보고 benchmark/report slice 범위를 다시 논의한다.

### 11.2 후속 slice 후보

첫 slice가 통과한 뒤에만 논의한다.

- Cluster term regression을 기존 Cluster-Ising 구현과 비교해 같은 하네스에 연결.
- Exact/ED benchmark와 validation code.
- `reports/`, `data/`, packaging scaffold.
- TeNPy DMRG OBC benchmark.
- TeNPy PBC seam probe.
- NetKet graph/operator/VMC benchmark.
- `hx` transverse-field conservation seam probe.
- 1D findings 초안 작성.
- 구현 결과를 보고 2D 계획과 LSWT 승격 위치를 별도로 논의.

## 12. 알려진 리스크

- DMRG/MPS에서 PBC는 OBC보다 어렵다.
- PBC DMRG를 tight tolerance 기준으로 두면 초기 구현이 불안정해질 수 있다.
- Cluster-Ising Pauli convention과 XXZ spin convention이 섞일 수 있다.
- NetKet/JAX 설치와 실행이 무거울 수 있다.
- 기존 Cluster-Ising 코드를 새 demo로 옮길 때 regression이 생길 수 있다.
- LSWT 승격 위치를 미리 정하면 실제 산출물 성격과 어긋날 수 있다.

## 13. 구현 중 확인할 것

현재 first code slice는 "theory docs + system definition + MethodForm probe"로 정리되었다. 구현 중에는 선택지를 다시 넓히지 않고, 아래 항목만 필요한 시점에 확인한다.

1. `LocalHilbertSpace`에 local operator matrix를 계속 둘지, operator registry로 분리할지.
2. 별도 `Geometry` object를 지금 만들지, 2D 확장 시점까지 `SpinSystem.sites/bonds/bc`로 둘지.
3. `Site`의 `sublattice`, `site_type`, `unit_cell`을 explicit field로 둘지, metadata로 둘지.
4. `change_form(system, method)`의 method selector 이름을 `ED`, `TN`, `NQS`, `QuadHam`으로 유지할지.
5. 첫 benchmark/report slice에서 아래 benchmark point 후보를 이대로 둘지:
   - `BP-XXZ-1`: `L=8` PBC, `Delta=0`, exact vs ED.
   - `BP-XXZ-2`: `L=8` PBC, `Delta=1`, ED finite-L 값과 thermodynamic anchor 구분.
6. Cluster term convention은 cluster-term slice에서 다시 검토한다:
   - 기존 Cluster-Ising처럼 Pauli operator `sigma^x sigma^z sigma^x`로 둘지.
   - XXZ와 맞춰 spin operator `Sx Sz Sx`로 재정규화할지.
7. Cluster coupling 이름:
   - `K`
   - `J_cluster`
   - `Jc`
8. Full benchmark CLI 이름을 `run_benchmarks.py`, `run_demo.py`, `run_experiments.py` 중 무엇으로 둘지.
