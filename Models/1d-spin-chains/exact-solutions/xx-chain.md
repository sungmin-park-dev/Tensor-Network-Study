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

Use the Jordan-Wigner convention from [method/jordan-wigner.md](method/jordan-wigner.md):

$$
S_i^+=c_i^\dagger P_i,
\qquad
S_i^-=P_i c_i,
\qquad
P_i=\prod_{\ell<i}(1-2n_\ell).
$$

For nearest-neighbor bulk links, the Jordan-Wigner strings cancel and the spin exchange becomes a
fermion hopping term:

$$
S_i^+S_{i+1}^-+S_i^-S_{i+1}^+
=c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i,
\qquad 0\le i\le L-2.
$$

The only extra finite-chain issue is the PBC boundary link. Let
$\pi_i=1-2n_i$ and define the total fermion parity as

$$
\Pi=\prod_{i=0}^{L-1}\pi_i=(-1)^{N_f}.
$$

Because $P_0=1$ and $\pi_{L-1}^2=1$, the boundary string is

$$
P_{L-1}=\prod_{\ell=0}^{L-2}\pi_\ell=\Pi\pi_{L-1}.
$$

Using $c_{L-1}^\dagger\Pi=-\Pi c_{L-1}^\dagger$,
$c_{L-1}^\dagger\pi_{L-1}=c_{L-1}^\dagger$,
$\pi_{L-1}c_{L-1}=c_{L-1}$, and $c_{L-1}c_0^\dagger=-c_0^\dagger c_{L-1}$,
the two boundary exchange terms become

$$
\begin{aligned}
S_{L-1}^+S_0^-
&=c_{L-1}^\dagger P_{L-1}c_0
=c_{L-1}^\dagger\Pi\pi_{L-1}c_0
=-\Pi c_{L-1}^\dagger c_0,\\
S_{L-1}^-S_0^+
&=P_{L-1}c_{L-1}c_0^\dagger
=\Pi\pi_{L-1}c_{L-1}c_0^\dagger
=-\Pi c_0^\dagger c_{L-1}.
\end{aligned}
$$

Therefore

$$
S_{L-1}^+S_0^-+S_{L-1}^-S_0^+
=-\Pi\left(c_{L-1}^\dagger c_0+c_0^\dagger c_{L-1}\right).
$$

Thus OBC is a plain finite hopping chain, while PBC must be solved in fixed fermion-parity sectors.

### Open Boundary Condition

For OBC, no boundary hopping term crosses the Jordan-Wigner ordering cut. The fermion Hamiltonian is

$$
H_{\mathrm{XX}}^{\mathrm{OBC}}
=\frac{J_{xy}}{2}\sum_{i=0}^{L-2}
\left(c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i\right).
$$

For OBC, the one-particle energies are

$$
\epsilon_m=J_{xy}\cos\left(\frac{\pi m}{L+1}\right),
\qquad m=1,2,\ldots,L.
$$

### Periodic Boundary Condition

For PBC, the bulk hopping terms are unchanged, while the boundary hopping term is the
parity-sector-dependent term derived above.

In a fixed parity sector $\Pi=\lambda_{\Pi}$ with $\lambda_{\Pi}=\pm1$, the fermionic boundary
condition is

$$
c_L=-\lambda_{\Pi}\,c_0.
$$

Here $c_L$ is a boundary-condition shorthand, not an additional physical site.

The corresponding momenta are

$$
k_m=
\begin{cases}
\dfrac{2\pi m}{L}, & \lambda_{\Pi}=-1,\\
\dfrac{2\pi(m+1/2)}{L}, & \lambda_{\Pi}=+1,
\end{cases}
\qquad m=0,1,\ldots,L-1.
$$

Let $K_{\lambda_{\Pi}}$ denote the momentum grid associated with the parity sector
$\lambda_{\Pi}$.

The one-particle energies are

$$
\epsilon(k)=J_{xy}\cos k.
$$

## Physical Quantities

### Many-Body Energy From Filled Levels

The many-body energy is obtained by filling one-particle levels.

For OBC, the occupation variables are $n_m\in\{0,1\}$ for the standing-wave modes
$m=1,2,\ldots,L$. For PBC, the occupation variables are $n_k\in\{0,1\}$ on the momentum grid
$K_{\lambda_{\Pi}}$ of a fixed parity sector.

### Ground-State Energy

For OBC, the finite-$L$ ground-state energy is the finite sum over occupied negative one-particle
levels:

$$
E_0^{\mathrm{OBC}}=\sum_{\epsilon_m<0}\epsilon_m,
$$

up to finite-size zero-mode degeneracy. This is an exact finite-chain value, not a thermodynamic-limit
estimate.

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

For PBC, the same filling rule must be applied inside each fermion-parity sector. The finite-chain
ground-state energy is

$$
E_0^{\mathrm{PBC}}
=\min_{\lambda_{\Pi}=\pm1}
\min_{\{n_k\}:\,(-1)^{\sum_k n_k}=\lambda_{\Pi}}
\sum_{k\in K_{\lambda_{\Pi}}} n_k\,J_{xy}\cos k.
$$

This is also an exact finite-chain prescription: evaluate the two parity sectors and choose the lower
energy, allowing zero-mode degeneracy when $\epsilon(k)=0$.

For $J_{xy}>0$, the parity-constrained PBC result is

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

For even $L$, the ground sector is $\lambda_{\Pi}=+1$ when $L=0\pmod 4$ and
$\lambda_{\Pi}=-1$ when $L=2\pmod 4$. For odd $L$, the two parity sectors give the same ground-state
energy with $N_f=(L-1)/2$ or $N_f=(L+1)/2$.

For the first-slice benchmark point $L=8$, `periodic`, and $J_{xy}=1$, the two sectors give

$$
E_{\lambda_{\Pi}=-1}=-1-\sqrt{2},
$$

from the occupied momenta $k=3\pi/4,\pi,5\pi/4$, and

$$
E_{\lambda_{\Pi}=+1}
=2\cos\frac{5\pi}{8}+2\cos\frac{7\pi}{8}
=-\sqrt{2+\sqrt{2}}-\sqrt{2-\sqrt{2}}.
$$

Therefore the exact finite-chain PBC ground-state energy for this benchmark is

$$
E_0^{\mathrm{PBC}}(L=8,J_{xy}=1)
=-\sqrt{2+\sqrt{2}}-\sqrt{2-\sqrt{2}}
\approx -2.6131259298.
$$

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

## References

- [method/jordan-wigner.md](method/jordan-wigner.md)
