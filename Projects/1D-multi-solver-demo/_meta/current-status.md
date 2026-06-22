# 1D Multi-Solver Demo — 현재 상태

### 1. 구현 surface 현황 — package와 검증 스크립트의 분리

코드는 현재 두 개의 분리된 surface로 존재한다.

1. **Method-consumption probe package** (`one_dimensional_multi_solver_demo/`) — `SpinSystem`을
   ED/TN/NQS/QuadHam `MethodForm`으로 변환만 한다. 솔버를 실행하지 않는다.
2. **Standalone XXZ verification/comparison scripts** (project root: `verify_xxz_bethe.py`,
   `compare_xxz_solvers.py`, `compare_xxz_observables.py`, `compare_xxz_entanglement_decay.py`) —
   ED/Bethe/DMRG를 직접 호출해 에너지, spin gap, magnetization, nearest-neighbor correlator,
   entanglement entropy, correlation decay를 비교한다. 패키지의 `MethodForm`을 거치지 않는다.

이 둘은 아직 연결되어 있지 않다. (2)는 [scope-and-design.md](scope-and-design.md) 2 "제외"에
있던 "probe package 경로 안에서 ED/DMRG/NQS backend solver 구현"을 패키지 경로 밖에서 이미
수행한 상태이며, [next-actions.md](next-actions.md) 1 Roadmap 3 (Exact Crosscheck Spec)과 5
(ED Baseline)의 실질적인 내용을 standalone script로 먼저 끝낸 것에 해당한다. (1)이 만드는 form과
(2)의 솔버 호출 사이를 잇는 `ObservableSpec` / `SolverResult` / `ComparisonReport` 계약은
`../../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md`에서 논의
중이며, 확정되면 (2)의 솔버 호출 로직을 (1)을 거쳐 흐르도록 재배선하는 것이 다음 구조적 작업이다. (2)가 만든
figure를 모은 첫 findings 초안은 [reports/findings.md](../reports/findings.md)에 있고, 같은 데이터를
브라우저에서 직접 열어 보는 `reports/dashboard.html`은 `build_dashboard.py`가 CSV에서 생성한다.

현재 디렉터리 구조:

```text
Projects/1D-multi-solver-demo/
  README.md
  run_method_probe.py
  verify_xxz_bethe.py
  compare_xxz_solvers.py
  compare_xxz_observables.py
  compare_xxz_entanglement_decay.py
  build_dashboard.py
  xxz_solver_comparison.csv / .png
  xxz_observables_comparison.csv / .png
  xxz_entanglement_decay.csv / .png

  reports/
    findings.md
    dashboard.html

  one_dimensional_multi_solver_demo/
    __init__.py
    spin_system.py
    spin_models.py
    method_form.py

  tests/
    test_method_forms.py

  _meta/
    PLAN.md
    scope-and-design.md
    current-status.md
    next-actions.md
    decision-log.md
    writing-guidelines.md
    progress/
      open/
        first-slice.md
      close/
        README.md
```

`run_method_probe.py`가 지금 출력하는 것 (numerical result report가 아니라 method form trace다):

- shared `SpinSystem` summary: model name, length, boundary condition, bond list.
- ED form: consumed fields, payload keys, many-body basis/local matrix requirement.
- TN form: named operator, bond, MPO-friendly term requirement.
- NQS form: graph, Hilbert, local operator split plus stochastic metadata requirement.
- QuadHam form: free-fermion hopping form, `not_applicable` 또는 `partial` status, JW boundary-sector requirement.
- Tests: each method form's status, required_extra, dropped fields, and key payload content.

### 2. 우선 모델과 현재 구현 범위

현재 구현·검증은 `H_XXZ + H_Zeeman` 부분집합에 한정한다 (`K=0`, [scope-and-design.md](scope-and-design.md)
5.1/5.2). `H_cluster` 항은 아직 placeholder이며 어떤 빌더에도 들어 있지 않다. 이론 문서·검증
스크립트도 모두 이 subset (XX/TFIM/XXZ)을 우선 다룬다.

결정이 내려진 시점과 경위는 [decision-log.md](decision-log.md)를 본다.

