# Jordan-Wigner Transformation

## Introduction

The Jordan-Wigner transformation maps a one-dimensional spin-$1/2$ chain to fermionic operators.

## Theoretical Motivation and Background

The Jordan-Wigner transformation is motivated by the idea of representing spin-$1/2$ degrees of
freedom in terms of fermionic creation and annihilation operators.

The nonlocal string is required because spin operators on different sites commute, whereas fermionic
operators on different sites must anticommute. In one dimension, the sites can be ordered along the
chain, so the string can count the fermion parity to the left of a given site and supply the sign
required by fermionic anticommutation.

## Definition

### Canonical Fermions

Let $c_j$ and $c_j^\dagger$ be canonical spinless fermion operators satisfying

$$
\{c_i,c_j^\dagger\}=\delta_{ij}, \qquad
\{c_i,c_j\}=0, \qquad
\{c_i^\dagger,c_j^\dagger\}=0.
$$

### Parity String

Let $n_j=c_j^\dagger c_j$ be the fermion number operator. For an ordered spin-$1/2$ chain, define
the parity string by

$$
P_j:=\prod_{\ell<j}p_\ell=\prod_{\ell<j}(1-2n_\ell).
$$

Here the local parity operator is

$$
p_\ell:=1-2n_\ell=e^{i\pi n_\ell}.
$$

Equivalently, the same string can be written as

$$
P_j=\exp\left(i\pi\sum_{\ell<j}n_\ell\right).
$$

Thus the Jordan-Wigner string can be written either as a product of local parity operators or as an
exponential of the fermion number to the left.

The parity string is Hermitian and unitary:

$$
P_j^\dagger=P_j,
\qquad
P_j^2=1.
$$

The parity string has the following exchange relations with fermionic operators. For sites included
in the string, it anticommutes:

$$
\{P_j,c_k\}=0,
\qquad
\{P_j,c_k^\dagger\}=0,
\qquad
k<j.
$$

For sites not included in the string, it commutes:

$$
[P_j,c_k]=0,
\qquad
[P_j,c_k^\dagger]=0,
\qquad
k\ge j.
$$

This is the sign structure that allows spin-flip operators to be represented by fermionic operators.

### Jordan-Wigner Transformation

A common Jordan-Wigner convention is

$$
S_j^+ = c_j^\dagger P_j, \qquad
S_j^- = P_j^\dagger c_j, \qquad
S_j^z = n_j-\frac{1}{2}.
$$

## Applications

Jordan-Wigner mappings can be defined beyond one dimension, but in higher dimensions they generally
introduce nonlocal strings, so they do not usually yield solvable fermionic Hamiltonians. The method
is therefore most useful in one-dimensional limits where the transformed Hamiltonian becomes
quadratic in fermionic operators.

| Spin-chain limit | Condition | Fermionic Hamiltonian |
|---|---|---|
| XX point | $K=0$, $h_x=h_z=0$, $J_z=0$ | number-conserving quadratic fermions |
| TFIM limit | $K=0$, $J_{xy}=0$, $J_z\ne0$, $h_x\ne0$ | quadratic fermions with pairing |

### XX Point

At the XX point, the $S_i^zS_j^z$ interaction is absent. The Jordan-Wigner transformation maps the
spin Hamiltonian to a hopping Hamiltonian of free fermions.

For the detailed finite-chain exact solution, see `../xx-chain.md`.

### Transverse-Field Ising Limit

In the transverse-field Ising limit, the Jordan-Wigner transformation gives a quadratic fermion
Hamiltonian with pairing terms. A Bogoliubov transformation then diagonalizes the model.

For the detailed finite-chain exact solution, see `../tfim-chain.md`.

## Discussion

### Periodic Boundary Conditions

Under spin periodic boundary conditions, the Jordan-Wigner map requires a separate finite-size
parity-sector treatment; the model-specific boundary terms are left to the corresponding
exact-solution notes.

## References

- E. Lieb, T. Schultz, and D. Mattis, "Two soluble models of an antiferromagnetic chain", Annals of Physics 16, 407 (1961).
- S. Katsura, "Statistical Mechanics of the Anisotropic Linear Heisenberg Model", Physical Review 127, 1508 (1962).
