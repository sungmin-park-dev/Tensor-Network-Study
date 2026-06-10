# Exact-Solution Methods

## 소개

이 폴더는 1D spin-chain 모델의 exact solution에 사용되는 대표적인 방법을 정리한다. 각 문서는
특정 benchmark point의 수치값을 고정하기보다, 해당 방법이 어떤 종류의 Hamiltonian에 적용되는지와
이 프로젝트에서 어떤 reference로 연결되는지를 설명한다.

## 정의

| Method | File | 연결되는 limit |
|---|---|---|
| Bethe ansatz | `bethe-ansatz.md` | XXZ chain, Heisenberg AFM point |
| Jordan-Wigner transformation | `jordan-wigner.md` | XX point, TFIM limit |

## 사용 원칙

이 방법론 문서들은 full Hamiltonian family 전체가 exact-solvable임을 주장하지 않는다. 일반적인
파라미터 영역에서는 정확해의 존재 또는 적분가능성이 기대되지 않으며, exact reference는 특정
solvable limit에서만 사용한다.

## 참고 문서

- [../../model-hamiltonian.md](../../model-hamiltonian.md)
- [1D multi-solver first slice](../../../../Projects/1D-multi-solver-demo/theory/progress/open/first-slice.md)
