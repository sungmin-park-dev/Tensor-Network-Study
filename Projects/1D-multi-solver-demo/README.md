# 1D Multi-Solver Demo

상태: project root note
범위: `1D-multi-solver-demo`에서 사용할 모델 이론 링크, 구현 slice, report/spec 후보

## Purpose

이 프로젝트는 모델 이론의 정본을 직접 소유하지 않는다. 공통 모델 설명, Hamiltonian,
convention, exact reference는 `../../Models/1d-spin-chains/`에서 관리한다.

여기에는 이 프로젝트의 구현 slice, progress, report 요구사항, project-local writing rule처럼
프로젝트 실행에 묶인 작업만 둔다.

## Reading Order

| Order | Document | Responsibility |
|---|---|---|
| 1 | `PLAN.md` | project scope, roadmap, and implementation order |
| 2 | `../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md` | active system-definition design discussion |
| 3 | `../../Models/1d-spin-chains/README.md` | reusable 1D spin-chain model theory entrypoint |
| 4 | `progress/open/first-slice.md` | first implementation slice and benchmark candidates |
| 5 | `writing-guidelines.md` | project-local writing and revision rules |

## Current Probe Surface

The current code surface is a method-consumption probe, not a solver benchmark harness.

| File | Role |
|---|---|
| `one_dimensional_multi_solver_demo/spin_system.py` | method-independent `SpinSystem` source structures |
| `one_dimensional_multi_solver_demo/spin_models.py` | first-slice XXZ + Zeeman system builder |
| `one_dimensional_multi_solver_demo/method_form.py` | ED, TN, NQS, QuadHam `MethodForm` exports |
| `run_method_probe.py` | prints consumed fields, required extras, dropped fields, and payload keys |
| `tests/test_method_forms.py` | verifies method-form behavior and QuadHam boundary/interacting cases |

## Boundary

- Reusable model introductions and exact references belong in `../../Models/1d-spin-chains/`.
- Project-local progress stays under `progress/`.
- Concrete code and scripts for this project stay under the project root, not under `Models/`.
