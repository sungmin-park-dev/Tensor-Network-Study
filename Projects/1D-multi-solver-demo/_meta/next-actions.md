# 1D Multi-Solver Demo — 다음 작업

### 1. Roadmap 개요

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
   구현이 쉬우면 OBC와 PBC를 모두 구현해 같은 조건에서 정확도·수렴·속도를 비교한다 ([scope-and-design.md](scope-and-design.md) 6).

8. **NQS**
   energy estimate, variance, convergence history, seed를 포함해 stochastic solver 결과 스키마를 확인한다.

9. **Findings**
   1D에서 얻은 S1~S5 seam evidence를 정리하고, 2D 확장 및 LSWT 승격 위치는 결과를 보고 판단한다.

### 2. 승인 후 구현 순서

이 섹션은 1차 확정 이후의 실행 기준이다.

#### 2.1 첫 구현 slice: theory docs + system definition + MethodForm probe

1. `../../../Models/1d-spin-chains/README.md`: reusable model theory의 읽기 순서와 각 문서 책임을 정리.
2. `../../../Models/1d-spin-chains/parameters-and-symbols.md`: parameter, symbol, code field naming을 분리해 정의.
3. `../../../Models/1d-spin-chains/conventions.md`: spin/Pauli, sign, site indexing, OBC/PBC convention을 정리.
4. `../../../Models/1d-spin-chains/model-hamiltonian.md`: 최종적으로 풀 XXZ + Cluster + Zeeman 1D Hamiltonian을 작성.
5. `../../../Models/1d-spin-chains/exact-solutions/README.md`: exact solution 문서들의 공통 convention과 사용 목적을 정리.
6. `../../../Models/1d-spin-chains/exact-solutions/xx-chain.md`: XX point finite-L reference를 정리.
7. `../README.md`: reusable model theory와 project-local execution의 연결을 정리.
8. `../../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md`: `SpinSystem`, method selector, `MethodForm`, `change_form` split을 논의한다.
9. `progress/open/first-slice.md`: 첫 slice의 구현 범위와 benchmark 후보를 확정하되, 현재 code probe가 solver benchmark가 아님을 명시한다.
10. `../one_dimensional_multi_solver_demo/spin_system.py`: method-independent system data structures를 구현한다.
11. `../one_dimensional_multi_solver_demo/spin_models.py`: first-slice XXZ + Zeeman `SpinSystem` builder를 구현한다.
12. `../one_dimensional_multi_solver_demo/method_form.py`: ED, TN, NQS, QuadHam `MethodForm` export를 구현한다.
13. `../run_method_probe.py`: method consumption trace를 출력한다.
14. `../tests/test_method_forms.py`: method form behavior와 QuadHam boundary/interaction cases를 검증한다.
15. 이 probe 결과를 보고 benchmark/report slice 범위를 다시 논의한다.

#### 2.2 후속 slice 후보

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

### 3. 열려 있는 질문

현재 first code slice는 "theory docs + system definition + MethodForm probe"로 정리되었다. 구현 중에는 선택지를 다시 넓히지 않고, 아래 항목만 필요한 시점에 확인한다.

1. `LocalHilbertSpace`에 local operator matrix를 계속 둘지, operator registry로 분리할지.
2. 별도 `Geometry` object를 지금 만들지, 2D 확장 시점까지 `SpinSystem.sites/bonds/bc`로 둘지.
3. `Site`의 `sublattice`, `site_type`, `unit_cell`을 explicit field로 둘지, metadata로 둘지.
4. `change_form(system, method)`의 method selector 이름을 `ED`, `TN`, `NQS`, `QuadHam`으로 유지할지.
5. 첫 benchmark/report slice에서 `BP-XXZ-1`/`BP-XXZ-2` benchmark point 후보([scope-and-design.md](scope-and-design.md) 9.4)를 이대로 둘지.
6. Cluster coupling 기호를 `K`, `J_cluster`, `Jc` 중 무엇으로 쓸지.
7. Full benchmark CLI 이름을 `run_benchmarks.py`, `run_demo.py`, `run_experiments.py` 중 무엇으로 둘지.
