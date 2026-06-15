# Free-Fermion Diagonalization

## Introduction

This note records the diagonalization of a number-conserving quadratic fermion Hamiltonian. The
method reduces the many-body problem to the diagonalization of a single-particle Hermitian matrix.

## Quadratic Hamiltonian

Consider canonical fermions $c_i,c_i^\dagger$ with a number-conserving quadratic Hamiltonian

$$
H=\sum_{i,j=0}^{L-1} c_i^\dagger h_{ij} c_j,
\qquad
h=h^\dagger.
$$

The matrix $h$ is the one-particle Hamiltonian. Let $u^{(\alpha)}$ be its normalized eigenvectors:

$$
\sum_{j=0}^{L-1}h_{ij}u_j^{(\alpha)}
=\epsilon_\alpha u_i^{(\alpha)}.
$$

Define new fermion operators by

$$
a_\alpha=\sum_{i=0}^{L-1}u_i^{(\alpha)*}c_i,
\qquad
c_i=\sum_\alpha u_i^{(\alpha)}a_\alpha.
$$

Then the Hamiltonian becomes

$$
H=\sum_\alpha \epsilon_\alpha a_\alpha^\dagger a_\alpha.
$$

Thus the spectrum is obtained by filling one-particle levels $\epsilon_\alpha$ with occupation
numbers $n_\alpha\in\{0,1\}$.

## Uniform Nearest-Neighbor Hopping

For a uniform hopping chain with hopping amplitude $t$, the open-boundary Hamiltonian is

$$
H_{\mathrm{OBC}}
=t\sum_{j=0}^{L-2}\left(c_j^\dagger c_{j+1}+c_{j+1}^\dagger c_j\right).
$$

The one-particle eigenvectors are standing waves,

$$
u_j^{(m)}
=\sqrt{\frac{2}{L+1}}
\sin\left(\frac{\pi m(j+1)}{L+1}\right),
\qquad m=1,2,\ldots,L,
$$

with one-particle energies

$$
\epsilon_m=2t\cos\left(\frac{\pi m}{L+1}\right).
$$

For a periodic or twisted chain, impose

$$
c_L=e^{i\phi}c_0.
$$

The momentum modes satisfy $e^{ikL}=e^{i\phi}$, so

$$
k_m=\frac{2\pi m+\phi}{L},
\qquad m=0,1,\ldots,L-1.
$$

The one-particle eigenvectors are plane waves,

$$
u_j^{(k)}=\frac{1}{\sqrt{L}}e^{ikj},
$$

with one-particle energies

$$
\epsilon(k)=2t\cos k.
$$

## Usage Boundary

This method note only diagonalizes number-conserving quadratic fermion Hamiltonians. Model-specific
mappings, boundary-sector constraints, level filling rules, and physical observables belong in the
corresponding exact-solution note.
