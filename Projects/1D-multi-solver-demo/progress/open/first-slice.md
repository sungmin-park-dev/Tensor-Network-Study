# First Slice

상태: open
범위: `1D-multi-solver-demo`의 첫 구현 slice에서 사용할 Hamiltonian subset과 benchmark 후보

## 1. Purpose

이 문서는 첫 구현 slice에만 해당하는 제한 조건을 관리한다. Full model Hamiltonian의 정의는
[Models/1d-spin-chains/model-hamiltonian.md](../../../../Models/1d-spin-chains/model-hamiltonian.md)에 두고,
여기서는 구현 시작점으로 사용할 부분계와 benchmark 후보만 기록한다.

정정된 목적은 1D solver 자체를 완성하는 것이 아니다. 1D chain은 2D spin-system solver 구조를
설계하기 전에, 같은 `SpinSystem` 정의가 ED, TN/DMRG, NQS, QuadHam에서 어떤 입력 형태로
갈라지는지 관찰하기 위한 controlled probe다.

첫 코드는 generic framework나 shared toolbox scaffold가 아니라 method-consumption probe로 둔다.
즉 `SpinSystem`을 만들고, `change_form(system, ED)`, `change_form(system, TN)`,
`change_form(system, NQS)`, `change_form(system, QuadHam)`이 각각 어떤 정보를 소비하고 어떤 추가
정보를 요구하는지 드러내는 데 집중한다.

System definition의 상세 설계 논의는
[260613-system-definition-design.md](../../../../GOVERNMENT/Working-Pad/issue-notes/open/260613-system-definition-design.md)에 둔다.

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

## 4. Observable Set And Convention

첫 slice의 observable set은 TN과 QuadHam/BdG 양쪽에서 계산 가능한 것으로 제한한다.

| Observable | Convention |
|---|---|
| 기저에너지 `E₀` | — |
| 에너지 밀도 `E₀/L` | — |
| 국소 자화 `<Si^z>` (site-resolved) | `S = σ/2`, 고유값 `±1/2` |
| Two-point correlator `C_c(i,j)` | connected primary; unconnected 플롯 병기 |
| Half-chain 얽힘 엔트로피 `S_{L/2}` | `S = -Tr(ρ ln ρ)`, nats 단위 |

시스템 크기 `L`은 자유 파라미터다. 첫 probe 시작값은 `L=8`이며 finite-size scaling을 위해 코드는 `L`을 인자로 받는다.

## 5. First Code Probe

The first code probe should expose method-specific input requirements before implementing solver
performance or a generic toolbox layer.

| Method selector | Meaning in this probe |
|---|---|
| `ED` | many-body basis plus local operator matrix terms |
| `TN` | named local operators, site type, bonds, and MPO-friendly term records |
| `NQS` | graph, local Hilbert space, and local operator records |
| `QuadHam` | quadratic Hamiltonian diagonalization form when the spin model admits it |

For periodic XX chains, `QuadHam` must surface the Jordan-Wigner boundary-sector requirement instead
of silently pretending that the spin PBC bond is already a single numeric hopping matrix.
