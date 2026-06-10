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

The only extra finite-chain issue is the PBC boundary link. With total fermion parity
$\Pi=(-1)^{N_f}$,

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

- The many-body energy is obtained by filling one-particle levels.
- For OBC, the ground-state energy is

$$
E_0^{\mathrm{OBC}}=\sum_{\epsilon_m<0}\epsilon_m,
$$

  up to finite-size zero-mode degeneracy.
- For PBC, the ground-state energy is the minimum over parity-consistent fillings:

$$
E_0^{\mathrm{PBC}}
=\min_{\lambda_{\Pi}=\pm1}
\min_{\{n_k\}:\,(-1)^{\sum_k n_k}=\lambda_{\Pi}}
\sum_{k\in K_{\lambda_{\Pi}}} n_k\,J_{xy}\cos k.
$$

- The site-normalized energy is $e_0=E_0/L$.
- The total spin and fermion number are related by $S_{\mathrm{tot}}^z=N_f-L/2$.

## References

- [method/jordan-wigner.md](method/jordan-wigner.md)
