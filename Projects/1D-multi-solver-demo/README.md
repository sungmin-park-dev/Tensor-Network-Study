# 1D Multi-Solver Demo

상태: project root note

## Goal

LSWT 코드를 리팩터링하기 전에, 같은 1D spin-chain `SpinSystem` 정의가 ED, TN/DMRG, NQS,
QuadHam(free-fermion/BdG) 솔버로 갈라질 때 각 솔버가 실제로 무엇을 소비하는지 먼저 확인하는
prep 데모/스파이크다. 솔버 결과 자체가 목적이 아니라, 시스템 정의와 솔버 입력 사이의 seam을
기록하는 것이 목적이다.

구현 목표 Hamiltonian:

$$
H = H_{XXZ} + H_{cluster} + H_{Zeeman}
$$

$$
H_{XXZ} = \sum_{\langle i,j \rangle} \left[ J_{xy} \left( S^x_i S^x_j + S^y_i S^y_j \right) + J_z S^z_i S^z_j \right]
$$

$$
H_{cluster} = -K \sum_i S^x_{i-1} S^z_i S^x_{i+1}
$$

$$
H_{Zeeman} = -h_z \sum_i S^z_i - h_x \sum_i S^x_i
$$

$H_{cluster}$는 표준 cluster(stabilizer graph-state) Hamiltonian이다 (`Cluster_Ising`이
Pauli $\sigma$ convention으로 먼저 구현). $H_{XXZ}$와 통일해 spin $S=\sigma/2$(고유값
$\pm1/2$) convention으로 둔다 — 기존 Pauli 결과와 비교할 때는 $K_{Pauli}=K_{spin}/8$로
환산한다 (3-body term, $(1/2)^3$). 현재 $K=0$.

최종 목표는 위 세 항을 같은 1D harness 안에서 term별로 on/off하며 동시에 비교 실행하는 것이다.

## Model Theory Boundary

이 프로젝트는 모델 이론의 정본을 직접 소유하지 않는다. 공통 모델 설명, Hamiltonian,
convention, exact reference는 `Models/1d-spin-chains/`에서 관리한다. 이 프로젝트에는 구현
slice, progress, report 요구사항, project-local writing rule처럼 실행에 묶인 작업만 둔다.

## Key Documents

| Document | Role |
|---|---|
| [_meta/PLAN.md](_meta/PLAN.md) | plan index — points to scope/status/next-action documents below |
| [_meta/scope-and-design.md](_meta/scope-and-design.md) | project scope, Hamiltonian family, and design rationale |
| [_meta/current-status.md](_meta/current-status.md) | current implementation status |
| [_meta/next-actions.md](_meta/next-actions.md) | roadmap, approved implementation order, open questions |
| [_meta/decision-log.md](_meta/decision-log.md) | time-ordered decision log — dated, point-in-time facts |
| [../../Models/1d-spin-chains/model-hamiltonian.md](../../Models/1d-spin-chains/model-hamiltonian.md) | canonical Hamiltonian and convention detail |
| [../../Models/1d-spin-chains/README.md](../../Models/1d-spin-chains/README.md) | reusable 1D spin-chain theory entrypoint |
| [../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md](../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md) | active `SpinSystem`/`MethodForm` design discussion |
| [_meta/progress/open/first-slice.md](_meta/progress/open/first-slice.md) | first implementation slice and benchmark candidates |
| [_meta/writing-guidelines.md](_meta/writing-guidelines.md) | project-local writing and revision rules |
