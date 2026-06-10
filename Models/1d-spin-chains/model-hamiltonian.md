# 1D Spin-Chain Model Hamiltonian

상태: 1차 이론 명세  
범위: TNS 프로젝트에서 재사용할 1D spin-1/2 Hamiltonian family

## 1. 도입

- 이 문서는 TNS 프로젝트에서 재사용할 1D spin-1/2 Hamiltonian family를 정의한다.
- Geometry symbol, model parameter, code field 이름의 표준 정의는
  [parameters-and-symbols.md](parameters-and-symbols.md)에서 관리한다.
- Indexing, boundary condition, operator normalization, sign convention은
  [conventions.md](conventions.md)를 따른다.
- 본 문서는 위 두 문서의 정의를 전제로 하여 Hamiltonian의 항별 구조와 first-slice 부분계를
  명시한다.
- 따라서 이 문서에서는 기호와 convention을 반복 설명하지 않고, Hamiltonian 자체의 수학적
  구조에 집중한다.

## 2. 모델 해밀토니안

본 프로젝트에서 고려하는 Hamiltonian는 XXZ exchange, Zeeman field, cluster interaction의 항으로 정의된다.
$$
H (\mathbf{J}, \mathbf{h}, K; {\mathcal{G}} )= H_{\mathrm{XXZ}} (\mathbf{J}; {\mathcal{G}}) + H_{\mathrm{Zeeman}} (\mathbf{h}; {\mathcal{G}})  + H_{\mathrm{cluster}} (K; {\mathcal{G}}).
$$
여기서 ${\mathcal{G}}$는 모델의 geometry를 나타내고, Section 2.1에서 정의한다. 
해밀토니안의 항별 세부적인 정의와 파라미터는 Section 2.2에서 정의한다. 

### 2.1 격자 구조 (${\mathcal{G}}$)

Hamiltonian은 먼저 고정된 system geometry 위에서 정의한다. Geometry는 $\mathcal{G}$로 표시한다.
이 기호는 model parameter와 구분되는 물리 시스템의 기하학적 specification을 가리킨다.

First slice의 geometry는 길이 $L$의 1D chain이다. Site index는 $i=0,1,\ldots,L-1$로 둔다.
`open` boundary condition에서는 nearest-neighbor bond가 $(i,i+1)$, $i=0,\ldots,L-2$로 주어진다.
`periodic` boundary condition에서는 여기에 boundary bond $(L-1,0)$를 추가한다.

이 문서의 나머지 부분에서는 geometry가 문맥상 고정되어 있다고 보고 $\mathcal{G}$ 아래첨자를
생략한다. 따라서 $\sum_{\langle i,j\rangle}$는 현재 선택된 1D chain geometry의 nearest-neighbor
bond에 대한 합을 의미한다.

### 2.2 해밀토니안($H$)과 상호작용 항

아래의 각 항은 Section 2.1의 site indexing과 boundary convention을 공유한다.

#### 2.2.1 XXZ Exchange Term

XXZ interaction은 다음과 같이 정의한다.

$$
H_{\mathrm{XXZ}}(J_{xy},J_z)
= \sum_{\langle i,j\rangle}
\left[
J_{xy}\left(S_i^x S_j^x + S_i^y S_j^y\right)
+ J_z S_i^z S_j^z
\right].
$$

여기서 $\langle i,j\rangle$는 선택된 geometry의 nearest-neighbor bond를 의미한다.
Anisotropy는 $\Delta=J_z/J_{xy}$로 정의한다.

#### 2.2.2 Zeeman Term

Zeeman field는 longitudinal field $h_z$와 transverse field $h_x$를 모두 허용한다.

$$
H_{\mathrm{Zeeman}}(h_z,h_x)
= -h_z \sum_{i=0}^{L-1} S_i^z
- h_x \sum_{i=0}^{L-1} S_i^x .
$$

#### 2.2.3 Cluster Term

Cluster interaction은 spin operator의 세 site 곱으로 둔다.

$$
H_{\mathrm{cluster}}(K)
= -K \sum_i S_{i-1}^{x} S_i^{z} S_{i+1}^{x}.
$$

이 cluster term은 1D chain term으로 해석한다. Periodic boundary condition에서는 site index를
modulo $L$로 해석한다. Open boundary condition에서 cluster term을 어떻게 truncate할지는
cluster-term slice에서 별도로 확정한다.

## 3. Exact Solution

일반적인 파라미터 영역에서는 정확해의 존재(exact solutions) 또는 적분가능성(integrability)이
기대되지 않는다. 그러나 특정 limit에서는 Jordan-Wigner transformation 또는 Bethe ansatz를 통해
exact reference를 얻을 수 있다.
참조 노트 파일은 `exact-solutions/` 아래에서 관리한다.

| Limit | Condition | Method | Reference note |
|---|---|---|---|
| XXZ chain | $K=0$, $h_x=0$ | Bethe ansatz | `exact-solutions/method/bethe-ansatz.md` |
| XX point | $K=0$, $h_x=h_z=0$, $J_z=0$ | Jordan-Wigner / free fermion | `xx-chain.md` |
| Heisenberg AFM point | $K=0$, $h_x=h_z=0$, $J_{xy}=J_z=1$ | Bethe ansatz | `exact-solutions/method/bethe-ansatz.md` |
| TFIM limit | $K=0$, $J_{xy}=0$, $J_z\ne0$, $h_x\ne0$ | Jordan-Wigner | `tfim-chain.md` |



Exact solution의 세부 derivation과 finite-size caveat는 `exact-solutions/`에서 관리한다.
프로젝트별 benchmark 사용 방식은 해당 project의 progress나 plan에서 관리한다. 예:
[1D multi-solver first slice](../../Projects/1D-multi-solver-demo/theory/progress/open/first-slice.md).

## 4. 모델 해밀토니안의 물리적 특성

이 섹션은 추후 작성한다.

## 5. 참고 문서

이 문서는 다음 theory 문서와 함께 읽는다.

| Document | Role |
|---|---|
| `parameters-and-symbols.md` | geometry symbol, model parameter, code field 이름의 source of truth |
| `conventions.md` | indexing, boundary condition, operator normalization, sign convention |
| [1D multi-solver first slice](../../Projects/1D-multi-solver-demo/theory/progress/open/first-slice.md) | 첫 구현 slice의 부분 Hamiltonian과 benchmark 후보 |
| `exact-solutions/README.md` | exact solution 문서들의 공통 사용 규칙 |
| `exact-solutions/xx-chain.md` | XX point finite-chain reference |
| `exact-solutions/method/bethe-ansatz.md` | Bethe ansatz method and Heisenberg thermodynamic anchor |
