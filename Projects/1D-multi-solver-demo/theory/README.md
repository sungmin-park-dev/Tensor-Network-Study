# 1D Multi-Solver Demo Theory

상태: project-local theory bridge
범위: `1D-multi-solver-demo`에서 사용할 모델 이론 링크, 구현 slice, report/spec 후보

## Purpose

이 디렉터리는 이제 모델 이론의 정본을 직접 소유하지 않는다. 공통 모델 설명, Hamiltonian,
convention, exact reference는 `../../../Models/1d-spin-chains/`에서 관리한다.

여기에는 이 프로젝트의 구현 slice, progress, report 요구사항, project-local writing rule처럼
프로젝트 실행에 묶인 이론 작업만 둔다.

## Reading Order

| Order | Document | Responsibility |
|---|---|---|
| 1 | `../../../Models/1d-spin-chains/README.md` | reusable 1D spin-chain model theory entrypoint |
| 2 | `progress/open/first-slice.md` | first implementation slice and benchmark candidates |
| 3 | `writing-guidelines.md` | project-local writing and revision rules |

## Boundary

- Reusable model introductions and exact references belong in `../../../Models/1d-spin-chains/`.
- Project-local progress stays here.
- Concrete code and scripts for this project stay under the project root, not under `Models/`.
