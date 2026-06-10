# Conventions

상태: 1차 이론 명세  
범위: `1D-multi-solver-demo`의 문서, 코드, 리포트가 공유해야 하는 해석 규약

## 1. Purpose

이 문서는 `1D-multi-solver-demo`에서 사용하는 indexing, boundary condition, operator
normalization, sign convention, numerical comparison convention을 고정한다. 기호와 코드 field
이름은 [parameters-and-symbols.md](parameters-and-symbols.md)에서 관리하며, 이 문서는 그
기호들이 어떤 물리적 의미와 계산 규칙을 갖는지 정의한다.

이 convention은 [model-hamiltonian.md](model-hamiltonian.md)의 Hamiltonian 정의에 적용된다.
특히 geometry symbol $\mathcal{G}$, chain length $L$, boundary condition $b$, model parameters
$J_{xy}$, $J_z$, $h_z$, $h_x$, $K$, $\mathcal{C}_{\mathrm{cl}}$, 그리고 energy symbols $E_0$,
$e_0$의 정의는 [parameters-and-symbols.md](parameters-and-symbols.md)를 따른다.

## 2. Indexing And Bond Order

Site index는 0-based convention을 따른다. 길이 $L$의 chain에서 site는 $i=0,1,\ldots,L-1$로
label한다.

Nearest-neighbor bond list는 deterministic order를 가진다. Open boundary condition에서는
$(0,1),(1,2),\ldots,(L-2,L-1)$ 순서로 둔다. Periodic boundary condition에서는 마지막에
boundary bond $(L-1,0)$를 추가한다. 이 순서는 ED matrix construction, geometry diagram,
report table에서 동일해야 한다.

## 3. Boundary Conditions

Boundary condition은 `bc`라는 field로 표시한다.

| `bc` value | Meaning | Bond content |
|---|---|---|
| `open` | open boundary condition | nearest-neighbor bonds only |
| `periodic` | periodic boundary condition | nearest-neighbor bonds plus $(L-1,0)$ |

문서에서는 OBC와 PBC 약어를 사용할 수 있다. 코드와 serialized run metadata에서는 `open`과
`periodic`을 우선 사용한다.

PBC는 ED와 graph-based NQS에서는 자연스럽게 boundary edge를 추가하는 방식으로 구현된다.
TN/DMRG에서는 PBC가 알고리즘적으로 더 무거운 선택이므로, OBC와 PBC 결과를 같은 tolerance
기대값으로 취급하지 않는다. 이 차이는 오류가 아니라 solver seam evidence의 일부로 기록한다.

## 4. Operator Normalization

Pauli operator는 $\sigma^a$, spin operator는 $S^a=\sigma^a/2$로 쓴다. 여기서
$a\in\{x,y,z\}$이다.

기본 operator normalization은 spin operator $S^a$이다. 따라서 XXZ term과 Zeeman term은 별도
표기가 없는 한 $S^a$로 쓴다.

Cluster term은 아직 normalization을 확정하지 않는다. Pauli cluster convention은
$O^a=\sigma^a$를 사용하고, spin cluster convention은 $O^a=S^a$를 사용한다. 두 coupling의 변환은
`parameters-and-symbols.md`에서 관리한다.

## 5. Hamiltonian Sign Convention

XXZ interaction은 다음 sign convention을 따른다.

$$
H_{\mathrm{XXZ}}
= \sum_{\langle i,j\rangle}
\left[
J_{xy}(S_i^xS_j^x+S_i^yS_j^y)+J_zS_i^zS_j^z
\right].
$$

이 convention에서 $J_{xy}>0$, $J_z>0$은 antiferromagnetic coupling이다.

Zeeman term은 $H_{\mathrm{Zeeman}}=-h_z\sum_iS_i^z-h_x\sum_iS_i^x$로 쓴다. 따라서 positive
$h_z$는 $+z$ 방향의 spin polarization을 에너지적으로 선호한다.

Cluster term은 $H_{\mathrm{cluster}}=-K\sum_i O_{i-1}^{x}O_i^{z}O_{i+1}^{x}$의 minus-sign
convention을 따른다. 단, $O^a$의 normalization은 cluster slice에서 확정한다.

## 6. Symmetry And Conservation Labels

Total $S^z$는 $S_{\mathrm{tot}}^z=\sum_iS_i^z$로 둔다. XXZ Hamiltonian with $h_x=0$은 total
$S^z$를 보존한다. Transverse field $h_x$가 켜지면 이 conservation은 일반적으로 깨진다.

Solver metadata는 conservation assumption을 명시적으로 기록해야 한다. 예를 들어 DMRG run은
`conserve_sz=true` 또는 이에 대응하는 backend setting을 남기고, NQS run은 full Hilbert space와
fixed-$S^z$ sector 중 어느 쪽을 사용했는지 기록한다.

## 7. Numerical Comparison Convention

Ground-state energy는 $E_0$, site-normalized energy는 $e_0=E_0/L$로 쓴다. 두 값이 동시에
존재할 때 report table에는 둘을 모두 기록한다.

Error는 기본적으로 absolute error $|E_{\mathrm{solver}}-E_{\mathrm{reference}}|$와 per-site
error $|e_{\mathrm{solver}}-e_{\mathrm{reference}}|$를 함께 기록한다. Stochastic solver의 경우
energy variance, run seed, sample count 또는 iteration count를 추가 metadata로 남긴다.

Thermodynamic-limit anchor와 finite-$L$ exact reference는 같은 종류의 reference로 취급하지
않는다. Heisenberg value $1/4-\log 2$는 finite-$L$ ED pass/fail 기준이 아니라 scale 및
finite-size drift를 해석하기 위한 anchor다.

## 8. Document-To-Code Traceability

문서와 구현은 다음 대응 관계를 유지한다.

| Theory artifact | Code/report artifact |
|---|---|
| parameter and symbol table | `hamiltonian_specs.py`, serialized run metadata |
| site and boundary convention | `geometry.py`, geometry report panel |
| Hamiltonian term definitions | `hamiltonian_specs.py`, solver model builders |
| exact reference formulae | `exact_solutions.py`, validation tests |
| comparison tolerance | `validation.py`, report pass/fail table |
| solver-specific required inputs | `solver_seams.py`, `reports/findings.md` |

새로운 solver나 term을 추가할 때는 코드만 변경하지 않는다. 먼저 관련 theory 문서의 convention을
갱신하고, 그 갱신이 report metadata에 반영되는지 확인한다.
