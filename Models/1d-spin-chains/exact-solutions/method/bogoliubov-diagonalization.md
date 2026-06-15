# Bogoliubov Diagonalization

## Introduction

This note records the diagonalization of a quadratic fermion Hamiltonian with pairing terms. The
method replaces the original fermions with quasiparticle operators that diagonalize the associated
Bogoliubov-de Gennes problem. It also records the ground-state two-point correlations, which are the
inputs a model note needs to evaluate observables.

## Quadratic Hamiltonian With Pairing

Consider canonical fermions $c_i,c_i^\dagger$ with a quadratic Hamiltonian

$$
H
=\sum_{i,j}c_i^\dagger A_{ij}c_j
+\frac{1}{2}\sum_{i,j}\left(c_i^\dagger B_{ij}c_j^\dagger+c_j B_{ij}^*c_i\right)
+E_{\mathrm{const}},
$$

where $A=A^\dagger$ and $B=-B^T$. In the Nambu basis

$$
\Psi=
\begin{pmatrix}
c_0\\
\vdots\\
c_{L-1}\\
c_0^\dagger\\
\vdots\\
c_{L-1}^\dagger
\end{pmatrix},
$$

the Hamiltonian can be written as

$$
H=\frac{1}{2}\Psi^\dagger
\begin{pmatrix}
A & B\\
-B^* & -A^*
\end{pmatrix}
\Psi
+E_{\mathrm{shift}}.
$$

The matrix in this expression is the Bogoliubov-de Gennes (BdG) matrix, denoted $M$. The constant
$E_{\mathrm{shift}}=E_{\mathrm{const}}+\tfrac{1}{2}\operatorname{Tr}A$ collects the term produced when
the $c_i c_i^\dagger$ piece of $\tfrac{1}{2}\Psi^\dagger M\Psi$ is normal ordered.

## Quasiparticle Modes

The particle-hole structure of $M$ makes its spectrum symmetric: eigenvalues come in pairs $\pm
E_\alpha$ with $E_\alpha\ge 0$. Each positive-energy eigenvector $(u^{(\alpha)},v^{(\alpha)})$ defines
a quasiparticle operator

$$
\gamma_\alpha
=\sum_i\left(u_i^{(\alpha)*}c_i+v_i^{(\alpha)*}c_i^\dagger\right).
$$

When the eigenvectors are normalized so that the transformation preserves the canonical
anticommutation relations, the Hamiltonian becomes

$$
H=E_{\mathrm{vac}}+\sum_{\alpha:E_\alpha>0}E_\alpha\,\gamma_\alpha^\dagger\gamma_\alpha,
\qquad
E_{\mathrm{vac}}
=E_{\mathrm{const}}+\frac{1}{2}\operatorname{Tr}A
-\frac{1}{2}\sum_{\alpha:E_\alpha>0}E_\alpha.
$$

The many-body spectrum is obtained by filling the quasiparticle levels $E_\alpha$, and $E_{\mathrm{vac}}$
is the energy of the Bogoliubov vacuum $|\Omega\rangle$ defined by $\gamma_\alpha|\Omega\rangle=0$ for
all positive-energy modes.

## Ground-State Correlations

Inverting the transformation expresses the original fermions through the positive-energy modes,

$$
c_i=\sum_{\alpha:E_\alpha>0}\left(u_i^{(\alpha)}\gamma_\alpha+v_i^{(\alpha)*}\gamma_\alpha^\dagger\right).
$$

Evaluating the two-point functions in $|\Omega\rangle$ with $\gamma_\alpha|\Omega\rangle=0$ leaves only
the $\gamma_\alpha\gamma_\alpha^\dagger$ contractions, so

$$
\langle c_i^\dagger c_j\rangle
=\sum_{\alpha:E_\alpha>0}v_i^{(\alpha)}v_j^{(\alpha)*},
\qquad
\langle c_i c_j\rangle
=\sum_{\alpha:E_\alpha>0}u_i^{(\alpha)}v_j^{(\alpha)*}.
$$

These two matrices are the only inputs Wick's theorem needs: every higher correlator of a Gaussian
state factorizes into them. A model note builds its observables, including Majorana covariance
matrices and string correlators, from these contractions.

## Translation-Invariant Two-Mode Form

For a translation-invariant one-dimensional system, the BdG problem splits into independent $(k,-k)$
sectors. If the sector Hamiltonian is written with real functions $A(k)$ and $B(k)$ as

$$
H_k
=2A(k)\left(c_k^\dagger c_k-\frac{1}{2}\right)
+iB(k)\left(c_k^\dagger c_{-k}^\dagger+c_k c_{-k}\right),
$$

then the quasiparticle energy is

$$
E(k)=2\sqrt{A(k)^2+B(k)^2}.
$$

The Bogoliubov angle $\theta_k$ that diagonalizes the block satisfies $\tan 2\theta_k=B(k)/A(k)$, and
the paired vacuum amplitudes are $u_k=\cos\theta_k$ and $v_k=i\sin\theta_k$. The paired-sector vacuum
energy is

$$
E_{\mathrm{vac}}=-\frac{1}{2}\sum_k E(k),
$$

summed over the momentum grid of the sector.

The allowed momentum grid is not fixed by the Bogoliubov method itself. It must be supplied by the
model-specific boundary condition and, when present, by the fermion-parity sector.

## Usage Boundary

This note only states the diagonalization procedure and the Gaussian ground-state correlations for
quadratic fermion Hamiltonians with pairing. The model-specific mapping, boundary-sector choice,
coefficient functions $A(k)$ and $B(k)$, and physical observables belong in the corresponding
exact-solution note.
