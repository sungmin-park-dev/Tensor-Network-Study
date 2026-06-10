# First Slice

상태: open  
범위: `1D-multi-solver-demo`의 첫 구현 slice에서 사용할 Hamiltonian subset과 benchmark 후보

## 1. Purpose

이 문서는 첫 구현 slice에만 해당하는 제한 조건을 관리한다. Full model Hamiltonian의 정의는
[Models/1d-spin-chains/model-hamiltonian.md](../../../../../Models/1d-spin-chains/model-hamiltonian.md)에 두고,
여기서는 구현 시작점으로 사용할 부분계와 benchmark 후보만 기록한다.

## 2. First-Slice Hamiltonian

첫 구현 slice에서는 cluster interaction을 끈다. 즉 $K=0$이며 $H_{\mathrm{cluster}}=0$이다.
또한 exact crosscheck 후보에서는 별도로 명시하지 않는 한 $h_z=h_x=0$으로 둔다.

따라서 첫 구현 대상은 다음 부분계다.

$$
H_{\mathrm{first}}(J_{xy},J_z,h_z,h_x)
= H_{\mathrm{XXZ}}(J_{xy},J_z)
+ H_{\mathrm{Zeeman}}(h_z,h_x).
$$

## 3. Benchmark Candidates

현재 benchmark-point 후보는 다음 두 개다. 이 목록은 exact reference와 validation criteria를
작성하는 과정에서 수정될 수 있다.

| Label | Geometry | Model parameters | Intended role |
|---|---|---|---|
| BP-XXZ-1 | $L=8$, `periodic` | $J_{xy}=1,\ J_z=0,\ h_z=h_x=0,\ K=0$ | XX/free-fermion finite-chain check |
| BP-XXZ-2 | $L=8$, `periodic` | $J_{xy}=1,\ J_z=1,\ h_z=h_x=0,\ K=0$ | Heisenberg anchor and finite-size caveat check |
