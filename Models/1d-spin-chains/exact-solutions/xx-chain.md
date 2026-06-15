# XX Model Exact Solution

## Introduction

- This note records the exact free-fermion reference for the XX model.
- In the generalized XXZ family, the same model is often described as the XX point.
- The general Jordan-Wigner transformation is described in [method/jordan-wigner.md](method/jordan-wigner.md).
- The finite-size reference must specify the boundary condition and, for PBC, the fermion-parity
  sector.

## Definition

The XX model is the isotropic XY spin-$1/2$ chain. It contains equal exchange couplings in the
$x$ and $y$ directions, with no $z$-exchange term. We write the Hamiltonian as

$$
H_{\mathrm{XX}}
=J_{xy}\sum_{\langle i,j\rangle}(S_i^xS_j^x+S_i^yS_j^y)
=\frac{J_{xy}}{2}\sum_{\langle i,j\rangle}(S_i^+S_j^-+S_i^-S_j^+).
$$

Here $\langle i,j\rangle$ denotes nearest-neighbor bonds of the chain. The second form follows from
$S_i^x=(S_i^++S_i^-)/2$ and $S_i^y=(S_i^+-S_i^-)/(2i)$.

## Solution

The XX model maps to a free-fermion hopping problem under the Jordan-Wigner transformation. We first
derive the fermionic Hamiltonians and then diagonalize them in the open and periodic boundary cases.

### Fermionic Hamiltonian

The Jordan-Wigner transformation turns the spin-flip exchange terms into quadratic fermion hopping
terms. The only boundary-dependent step is the parity factor on the periodic boundary link.

#### Jordan-Wigner Setup

We fix the Jordan-Wigner convention and derive the string-reduction formula for a general ordered
pair $i<j$. The convention follows [method/jordan-wigner.md](method/jordan-wigner.md):

$$
S_i^+=c_i^\dagger P_i,
\qquad
S_i^-=P_i c_i,
\qquad
P_i=\prod_{\ell<i}p_\ell,
\qquad
p_\ell=1-2n_\ell.
$$

The local parity operator satisfies

$$
\begin{aligned}
p_i c_i&=c_i,&
c_i p_i&=-c_i,\\
p_i c_i^\dagger&=-c_i^\dagger,&
c_i^\dagger p_i&=c_i^\dagger,
\end{aligned}
$$

and it commutes with fermion operators on all other sites. Thus $P_i$ commutes with
$c_k,c_k^\dagger$ for $k\ge i$, while $P_j$ anticommutes with $c_i,c_i^\dagger$ when $i<j$.

For two sites $i<j$, the spin-flip exchange operator becomes

$$
S_i^+S_j^-+S_i^-S_j^+
=c_i^\dagger Q_{ij}c_j+c_j^\dagger Q_{ij}c_i,
$$

where

$$
Q_{ij}:=\prod_{\ell=i+1}^{j-1}p_\ell.
$$

To see this, use $P_j=P_i p_i Q_{ij}$ and $P_i^2=1$:

$$
P_iP_j=p_iQ_{ij}.
$$

The two exchange terms are

$$
\begin{aligned}
S_i^+S_j^-
&=c_i^\dagger P_iP_j c_j\\
&=c_i^\dagger p_i Q_{ij} c_j\\
&=c_i^\dagger Q_{ij} c_j,
\end{aligned}
$$

and

$$
S_i^-S_j^+=P_i c_i c_j^\dagger P_j=c_i c_j^\dagger p_i Q_{ij}=-c_i c_j^\dagger Q_{ij}=c_j^\dagger Q_{ij}c_i.
$$

In the second term, only $P_i$ is moved through the endpoint fermions; $P_j$ is not moved through
$c_i$. After substituting $P_iP_j=p_iQ_{ij}$, the identities $c_ip_i=-c_i$ and
$c_i c_j^\dagger=-c_j^\dagger c_i$ give the compact line above.

#### OBC Hamiltonian

For OBC, every bond is a nearest-neighbor bulk link in the Jordan-Wigner ordering, so the general
formula reduces to a local hopping term. Since $Q_{i,i+1}=1$,

$$
S_i^+S_{i+1}^-+S_i^-S_{i+1}^+
=c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i,
\qquad 0\le i\le L-2.
$$

Therefore the OBC Hamiltonian is

$$
H_{\mathrm{XX}}^{\mathrm{OBC}}
=\frac{J_{xy}}{2}\sum_{i=0}^{L-2}
\left(c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i\right).
$$

#### PBC Hamiltonian

For PBC, the bulk links are unchanged, but the boundary link acquires a fermion-parity factor:

$$
S_{L-1}^+S_0^-+S_{L-1}^-S_0^+
=-\Pi\left(c_{L-1}^\dagger c_0+c_0^\dagger c_{L-1}\right),
$$

where

$$
\Pi=\prod_{i=0}^{L-1}p_i=(-1)^{N_f}.
$$

The boundary link is $(L-1,0)$. Since $P_0=1$, only the operator at site $L-1$ carries a
Jordan-Wigner string:

$$
P_{L-1}=\prod_{\ell=0}^{L-2}p_\ell.
$$

Multiplying by $p_{L-1}^2=1$ rewrites this string in terms of the total fermion parity:

$$
P_{L-1}=\left(\prod_{\ell=0}^{L-1}p_\ell\right)p_{L-1}=\Pi p_{L-1}.
$$

The two boundary exchange terms are

$$
\begin{aligned}
S_{L-1}^+S_0^-
&=c_{L-1}^\dagger P_{L-1}c_0
=c_{L-1}^\dagger\Pi p_{L-1}c_0
=-\Pi c_{L-1}^\dagger c_0,\\
S_{L-1}^-S_0^+
&=P_{L-1}c_{L-1}c_0^\dagger
=\Pi p_{L-1}c_{L-1}c_0^\dagger
=-\Pi c_0^\dagger c_{L-1}.
\end{aligned}
$$

Here $c_{L-1}^\dagger\Pi=-\Pi c_{L-1}^\dagger$,
$c_{L-1}^\dagger p_{L-1}=c_{L-1}^\dagger$,
$p_{L-1}c_{L-1}=c_{L-1}$, and $c_{L-1}c_0^\dagger=-c_0^\dagger c_{L-1}$.

This parity-dependent boundary term means PBC must be solved in fixed fermion-parity sectors. In a
sector $\Pi=\lambda_{\Pi}$, the Hamiltonian is

$$
H_{\mathrm{XX}}^{\mathrm{PBC}}(\lambda_{\Pi})
=\frac{J_{xy}}{2}
\left[
\sum_{i=0}^{L-2}
\left(c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i\right)
-\lambda_{\Pi}\left(c_{L-1}^\dagger c_0+c_0^\dagger c_{L-1}\right)
\right].
$$

Equivalently, the fermions satisfy the boundary condition

$$
c_L=-\lambda_{\Pi}\,c_0.
$$

Here $c_L$ is a boundary-condition shorthand, not an additional physical site.

### Diagonalization

The fermionic Hamiltonians above are quadratic hopping problems. We use
[method/free-fermion-diagonalization.md](method/free-fermion-diagonalization.md) with hopping
amplitude $t=J_{xy}/2$.

#### OBC Diagonalization

For OBC, the standing-wave one-particle energies are

$$
\epsilon_m=J_{xy}\cos\left(\frac{\pi m}{L+1}\right),
\qquad m=1,2,\ldots,L.
$$

#### PBC Diagonalization

For PBC, the fixed-sector boundary condition $c_L=-\lambda_{\Pi}c_0$ fixes the allowed momentum
grid:

$$
k_m=
\begin{cases}
\dfrac{2\pi m}{L}, & \lambda_{\Pi}=-1,\\
\dfrac{2\pi(m+1/2)}{L}, & \lambda_{\Pi}=+1,
\end{cases}
\qquad m=0,1,\ldots,L-1.
$$

Let $K_{\lambda_{\Pi}}$ denote the momentum grid associated with the parity sector
$\lambda_{\Pi}$. The one-particle energies are

$$
\epsilon(k)=J_{xy}\cos k.
$$

### Bridge to Physical Quantities

At this point, the spin problem has been reduced to one-particle fermionic levels with specified
boundary sectors. The next section fills these levels to compute many-body energies and spin
expectation values.

## Physical Quantities

### Many-Body Energy From Filled Levels

The many-body energy is obtained by filling one-particle fermion levels. For OBC,

$$
E[\{n_m\}]
=\sum_{m=1}^{L}n_m\,J_{xy}\cos\left(\frac{\pi m}{L+1}\right),
\qquad n_m\in\{0,1\}.
$$

For PBC, the filling must be evaluated inside a fixed fermion-parity sector:

$$
E[\{n_k\};\lambda_{\Pi}]
=\sum_{k\in K_{\lambda_{\Pi}}}n_k\,J_{xy}\cos k,
\qquad
(-1)^{\sum_k n_k}=\lambda_{\Pi}.
$$

### Ground-State Energy

The finite-chain ground-state energy is the minimum over the allowed fillings:

$$
E_0^{\mathrm{OBC}}
=\min_{\{n_m\}}\sum_{m=1}^{L}n_m\,J_{xy}\cos\left(\frac{\pi m}{L+1}\right),
$$

and

$$
E_0^{\mathrm{PBC}}
=\min_{\lambda_{\Pi}=\pm1}
\min_{\{n_k\}:\,(-1)^{\sum_k n_k}=\lambda_{\Pi}}
\sum_{k\in K_{\lambda_{\Pi}}}n_k\,J_{xy}\cos k.
$$

For $J_{xy}>0$, the OBC finite sum can be written as

$$
E_0^{\mathrm{OBC}}(L)
=
\begin{cases}
-\dfrac{J_{xy}}{2}
\left[
\csc\left(\dfrac{\pi}{2(L+1)}\right)-1
\right],
& L\ \mathrm{even},\\[1.2em]
-\dfrac{J_{xy}}{2}
\left[
\cot\left(\dfrac{\pi}{2(L+1)}\right)-1
\right],
& L\ \mathrm{odd}.
\end{cases}
$$

For PBC and $J_{xy}>0$, the parity-constrained result is

$$
E_0^{\mathrm{PBC}}(L)
=
\begin{cases}
-J_{xy}\csc\left(\dfrac{\pi}{L}\right),
& L\ \mathrm{even},\\[1.2em]
-J_{xy}\cot\left(\dfrac{\pi}{L}\right)
\cos\left(\dfrac{\pi}{2L}\right),
& L\ \mathrm{odd}.
\end{cases}
$$

### Ground-State Wavefunction

Let $a_\alpha$ denote the diagonal fermion modes. Each many-body eigenstate is a Slater determinant,

$$
|\{n_\alpha\}\rangle
=\prod_{\alpha:\,n_\alpha=1}a_\alpha^\dagger|0\rangle.
$$

The ground state is the allowed filling that minimizes the energy in the boundary sector under
consideration.

### Energy Density

The site-normalized energy is

$$
e_0=\frac{E_0}{L}.
$$

### Fermion Number And Total Spin

The total spin and fermion number are related by

$$
S_{\mathrm{tot}}^z=N_f-\frac{L}{2}.
$$

The local magnetization is

$$
\langle S_i^z\rangle
=\langle n_i\rangle-\frac{1}{2}.
$$

For a translation-invariant PBC filling state, this reduces to

$$
\langle S_i^z\rangle
=\frac{\langle S_{\mathrm{tot}}^z\rangle}{L}
=\frac{N_f}{L}-\frac{1}{2}.
$$

Number-conserving eigenstates also satisfy

$$
\langle S_i^x\rangle=\langle S_i^y\rangle=0.
$$

### Two-Point Correlators

The fermion one-body correlator is

$$
G_{ij}:=\langle c_i^\dagger c_j\rangle.
$$

For an OBC filling,

$$
G_{ij}
=\sum_{m:\,n_m=1}
\frac{2}{L+1}
\sin\left(\frac{\pi m(i+1)}{L+1}\right)
\sin\left(\frac{\pi m(j+1)}{L+1}\right).
$$

For a PBC filling,

$$
G_{ij}
=\frac{1}{L}\sum_{k:\,n_k=1}e^{ik(j-i)}.
$$

The longitudinal spin correlator follows directly from Wick's theorem. For $i\ne j$,

$$
\langle S_i^z\rangle=G_{ii}-\frac{1}{2},
\qquad
\langle S_i^zS_j^z\rangle
=\left(G_{ii}-\frac{1}{2}\right)
\left(G_{jj}-\frac{1}{2}\right)
-G_{ij}G_{ji}.
$$

Transverse correlators contain the Jordan-Wigner string and are computed as Gaussian Wick
determinants or Pfaffians.

### Entanglement Entropy

For a subsystem $A$, let $C_A$ be the restriction of $G_{ij}$ to sites in $A$. If $\nu_a$ are the
eigenvalues of $C_A$, the von Neumann entanglement entropy is

$$
S_A
=-\sum_a\left[
\nu_a\log\nu_a+(1-\nu_a)\log(1-\nu_a)
\right].
$$

### Correlation Length

The zero-field XX chain is gapless in the thermodynamic ground state, so its spin correlations are
algebraic and the correlation length is

$$
\xi=\infty.
$$

## References

- [method/free-fermion-diagonalization.md](method/free-fermion-diagonalization.md)
- [method/jordan-wigner.md](method/jordan-wigner.md)
