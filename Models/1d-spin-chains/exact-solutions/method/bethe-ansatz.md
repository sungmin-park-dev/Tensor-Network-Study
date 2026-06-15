# Bethe Ansatz

## Introduction

The Bethe ansatz solves a one-dimensional integrable spin chain by expressing its eigenstates through a
set of quasiparticle momenta whose only interaction is pairwise scattering. It is not a general
technique for arbitrary spin chains: it relies on factorized scattering and a sufficient number of
conserved quantities, which the XXZ family provides at $K=0$ and $h_x=0$.

This note records the coordinate Bethe ansatz machinery. The model-specific dispersion, scattering
phase, and energy belong to the corresponding model note; the XXZ specialization is in
[../xxz-chain.md](../xxz-chain.md).

## Coordinate Bethe Ansatz

Work in the ferromagnetic reference state $|0\rangle=|\!\uparrow\cdots\uparrow\rangle$ and treat each
down spin as a magnon. A magnon at site $x$ is $S_x^-|0\rangle$, and the conserved magnon number
$M=\tfrac{L}{2}-S_{\mathrm{tot}}^z$ labels the sector.

A single magnon is a plane wave $|k\rangle=\sum_{x=0}^{L-1}e^{ikx}S_x^-|0\rangle$ with a
model-supplied dispersion $\varepsilon(k)$. The $M$-magnon Bethe state superposes plane waves over all
orderings of the momenta $\{k_1,\ldots,k_M\}$,

$$
|\psi\rangle
=\sum_{x_1<\cdots<x_M}
\left(\sum_{P\in S_M}A_P\,\exp\Big(i\sum_{j=1}^{M}k_{P_j}x_j\Big)\right)
S_{x_1}^-\cdots S_{x_M}^-|0\rangle,
$$

with permutation amplitudes $A_P$. Away from coincident sites this is an eigenstate with energy

$$
E=E_{\mathrm{ref}}+\sum_{j=1}^{M}\varepsilon(k_j),
$$

so the interaction enters only through the amplitudes $A_P$.

## Bethe Equations

The eigenvalue equation at two coincident magnons fixes the ratio of amplitudes that differ by one
transposition. It takes the form

$$
\frac{A_{\ldots l j\ldots}}{A_{\ldots j l\ldots}}=-e^{i\theta(k_j,k_l)},
$$

with a model-specific two-body scattering phase $\theta(k_j,k_l)$. Imposing periodicity
$a(x_2,\ldots,x_M,x_1+L)=a(x_1,\ldots,x_M)$ then gives the Bethe equations

$$
e^{ik_jL}=(-1)^{M-1}\prod_{l\ne j}e^{i\theta(k_j,k_l)},
\qquad j=1,\ldots,M.
$$

These couple the momenta through the scattering phase. For a finite chain the solution is obtained by
solving this set numerically; the energy then follows from $E=E_{\mathrm{ref}}+\sum_j\varepsilon(k_j)$
evaluated on the solution.

## Thermodynamic Limit

For the antiferromagnetic ground state the relevant sector is $M=\tfrac{L}{2}$ with real momenta. As
$L\to\infty$ the momenta fill a distribution with density $\rho(k)$, and the Bethe equations become a
linear integral equation for $\rho$. The ground-state energy per site is then an integral of
$\varepsilon(k)$ weighted by $\rho(k)$.

The integral equation has a closed-form solution at special points. For the isotropic Heisenberg
antiferromagnet the thermodynamic ground-state energy per site is

$$
e_0=\frac{1}{4}-\log 2,
$$

in units of the exchange coupling. This value is a thermodynamic-limit anchor, not a finite-$L$
pass/fail threshold; the finite-size reference is obtained by solving the Bethe equations at the
desired $L$.

## Usage Boundary

This note only records the coordinate Bethe ansatz and the form of the Bethe equations. The
model-specific dispersion $\varepsilon(k)$, scattering phase $\theta(k_j,k_l)$, regime structure, and
ground-state energy belong in the corresponding model note.

## References

- H. Bethe, "Zur Theorie der Metalle. I.", Zeitschrift für Physik 71, 205 (1931).
- L. Hulthén, "Über das Austauschproblem eines Kristalles", Arkiv för Matematik, Astronomi och Fysik 26A, 1 (1938).
- C. N. Yang and C. P. Yang, "One-Dimensional Chain of Anisotropic Spin-Spin Interactions. I.", Physical Review 150, 321 (1966).
- [../xxz-chain.md](../xxz-chain.md)
- [../../model-hamiltonian.md](../../model-hamiltonian.md)
