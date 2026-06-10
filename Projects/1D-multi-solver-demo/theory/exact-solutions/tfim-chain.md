# TFIM Model Exact Solution

## Introduction

- This note records the exact Jordan-Wigner reference for the TFIM model.
- In the generalized Hamiltonian family used here, the same model is obtained as the
  transverse-field Ising limit.
- The general Jordan-Wigner transformation is described in [method/jordan-wigner.md](method/jordan-wigner.md).
- The finite-size PBC reference must specify the fermion-parity sector before using the
  momentum-space spectrum.

## Definition

The TFIM model is obtained by setting $K=0$, $J_{xy}=0$, $J_z\ne0$, and $h_x\ne0$. The Hamiltonian is

$$
H_{\mathrm{TFIM}}
=J_z\sum_{\langle i,j\rangle}S_i^zS_j^z
-h_x\sum_{i=0}^{L-1}S_i^x.
$$

After a spin-axis rotation exchanging $S^z$ and $S^x$, this becomes the standard transverse-field
Ising form used for the Jordan-Wigner solution.

## Jordan-Wigner And Bogoliubov Form

The Jordan-Wigner transformation maps the rotated TFIM to a quadratic fermion Hamiltonian with
pairing terms. A Bogoliubov transformation diagonalizes it as

$$
H_{\mathrm{TFIM}}
=\sum_k \epsilon(k)\left(\gamma_k^\dagger\gamma_k-\frac{1}{2}\right),
$$

up to finite-size parity-sector boundary terms.

With the spin-operator normalization used in this project, the quasiparticle dispersion is

$$
\epsilon(k)
=2\sqrt{
\left(\frac{h_x}{2}+\frac{J_z}{4}\cos k\right)^2
+\left(\frac{J_z}{4}\sin k\right)^2
}.
$$

## Periodic Boundary Conditions

- For PBC, the Jordan-Wigner solution must be organized by fermion-parity sector.
- Each parity sector fixes the allowed momentum grid.
- The finite-size ground-state reference is the minimum over parity sectors after the
  Bogoliubov diagonalization.

## Discussion

- The TFIM limit is exactly solvable because the Jordan-Wigner image is quadratic, but it is not
  number conserving.
- The exact reference should record whether the calculation used OBC or PBC.
- For PBC, the parity sector and momentum grid are part of the benchmark definition.

## References

- [method/jordan-wigner.md](method/jordan-wigner.md)
