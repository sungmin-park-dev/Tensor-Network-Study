# Parameters And Symbols

상태: 1차 이론 명세  
범위: TNS 1D spin-chain model notes and projects의 system geometry symbol, model parameter, derived quantity, code field naming

## 1. Purpose

이 문서는 TNS의 1D spin-chain model notes와 관련 project에서 반복적으로 사용하는 기호와 코드
field 이름의 대응을 관리한다. 다른 이론 문서는 이 문서에서 정의한 기호를 참조한다. 이 문서에서는
system geometry와 model parameter를 명시적으로 구분한다. $L$과 $b$는 물리 시스템의 기하학적
specification이며, Hamiltonian model parameter가 아니다.

## 2. System Geometry Symbols

| Symbol | Code field | Meaning |
|---|---|---|
| $\mathcal{G}$ | `geometry` | system geometry |
| $L$ | `length` | number of spin-1/2 sites |
| $i,j$ | `site_i`, `site_j` where needed | site indices |
| $b$ | `bc` | boundary condition |
| $\langle i,j\rangle_b$ | `bonds` | nearest-neighbor bond set determined by $b$ |

The first-slice geometry is a 1D chain specified by $L$ and $b$. The allowed values of `bc` are
`open` and `periodic`.

## 3. Local Operators

| Symbol | Code field or label | Meaning |
|---|---|---|
| $\sigma^a$ | `pauli_<a>` where needed | Pauli operator for $a\in\{x,y,z\}$ |
| $S^a$ | `spin_<a>` where needed | spin operator, $S^a=\sigma^a/2$ |
| $S_{\mathrm{tot}}^z$ | `total_sz` | total longitudinal spin, $\sum_i S_i^z$ |

The default operator normalization for XXZ and Zeeman terms is $S^a$, not $\sigma^a$.

## 4. XXZ And Zeeman Model Parameters

| Symbol | Code field | Meaning |
|---|---|---|
| $J_{xy}$ | `jxy` | transverse XXZ exchange |
| $J_z$ | `jz` | longitudinal XXZ exchange |
| $h_z$ | `hz` | longitudinal Zeeman field |
| $h_x$ | `hx` | transverse Zeeman field |

The anisotropy parameter is derived as $\Delta=J_z/J_{xy}$ when $J_{xy}\ne 0$.

## 5. Cluster Model Parameters

| Symbol | Code field | Meaning |
|---|---|---|
| $K$ | `cluster_coupling` | generic cluster coupling before choosing normalization |
| $\mathcal{C}_{\mathrm{cl}}$ | `cluster_convention` | cluster operator normalization convention |
| $K_{\sigma}$ | `k_sigma` | Pauli-normalized cluster coupling |
| $K_S$ | `k_spin` | spin-normalized cluster coupling |

The cluster convention $\mathcal{C}_{\mathrm{cl}}$ determines whether $K$ is interpreted as
$K_{\sigma}$ or $K_S$. The two normalizations are related by $K_{\sigma}=K_S/8$ and
$K_S=8K_{\sigma}$.

The first implementation slice sets $K=0$ and therefore does not require choosing
$\mathcal{C}_{\mathrm{cl}}$.

The full model-parameter collection for the Hamiltonian family is
$\theta=(J_{xy},J_z,h_z,h_x,K,\mathcal{C}_{\mathrm{cl}})$. The geometry $\mathcal{G}$ is not part of
$\theta$.

## 6. Energy And Error Symbols

| Symbol | Code field | Meaning |
|---|---|---|
| $E_0$ | `energy` or `ground_state_energy` | total ground-state energy |
| $e_0$ | `energy_per_site` | site-normalized energy, $E_0/L$ |
| $\epsilon_E$ | `abs_energy_error` | absolute total-energy error |
| $\epsilon_e$ | `abs_energy_per_site_error` | absolute per-site energy error |

By default, $\epsilon_E=|E_{\mathrm{solver}}-E_{\mathrm{reference}}|$ and
$\epsilon_e=|e_{\mathrm{solver}}-e_{\mathrm{reference}}|$.

## 7. Benchmark-Point Labels

Benchmark points use the label form `BP-<family>-<index>`. Here `BP` means benchmark point.

| Label | Meaning |
|---|---|
| `BP-XXZ-1` | XX point finite-chain crosscheck candidate |
| `BP-XXZ-2` | Heisenberg point anchor and finite-size caveat candidate |

These labels identify reproducible experimental settings, not universal physical limits. A complete
benchmark record must include the geometry $\mathcal{G}$, model parameters, solver, random seed when
applicable, and tolerance.
