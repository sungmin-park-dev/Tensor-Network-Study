# XXZ Model Exact Solution

## Introduction

- This note records the Bethe ansatz reference for the XXZ chain.
- In the generalized family, the XXZ chain is the $K=0$, $h_x=0$ limit; the XX point ($\Delta=0$) and
  the isotropic Heisenberg point ($\Delta=1$) are special cases.
- The general coordinate Bethe ansatz is described in [method/bethe-ansatz.md](method/bethe-ansatz.md).
- Unlike the XX and TFIM limits, the XXZ chain is interacting. Finite-size references require solving
  the Bethe equations numerically; closed forms appear only at special points and in the
  thermodynamic limit.

## Definition

The XXZ chain is the anisotropic Heisenberg chain. With exchange $J_{xy}$ and anisotropy
$\Delta=J_z/J_{xy}$,

$$
H_{\mathrm{XXZ}}
=J_{xy}\sum_{\langle i,j\rangle}\left(S_i^xS_j^x+S_i^yS_j^y+\Delta\,S_i^zS_j^z\right)
=\sum_{\langle i,j\rangle}\left[\frac{J_{xy}}{2}\left(S_i^+S_j^-+S_i^-S_j^+\right)+J_zS_i^zS_j^z\right].
$$

For $J_{xy}>0$ the model is antiferromagnetic, and the anisotropy sets three regimes:

| Regime | Range | Character |
|---|---|---|
| gapless | $0\le\Delta<1$ | critical, algebraic correlations; $\Delta=0$ is the XX point |
| isotropic | $\Delta=1$ | Heisenberg antiferromagnet, gapless with logarithmic corrections |
| gapped | $\Delta>1$ | Ising-like Néel order, finite correlation length |

The $\Delta=0$ point has an independent free-fermion solution in
[xx-chain.md](xx-chain.md); this note covers the interacting $\Delta\ne0$ chain.

## Solution

### Magnon Reference And Dispersion

Take the ferromagnetic reference $|0\rangle=|\!\uparrow\cdots\uparrow\rangle$. Each bond contributes
$J_z/4$, so $E_{\mathrm{ref}}=J_{xy}\Delta L/4$. A single magnon $S_x^-$ hops with amplitude
$J_{xy}/2$ and breaks the two adjacent $S^zS^z$ bonds, giving the dispersion

$$
\varepsilon(k)=J_{xy}\left(\cos k-\Delta\right).
$$

The interaction between magnons does not change this dispersion; it enters only through the scattering
in the Bethe equations.

### XXZ Bethe Equations

Imposing the coordinate Bethe ansatz of [method/bethe-ansatz.md](method/bethe-ansatz.md), the XXZ
two-magnon scattering fixes the Bethe equations for the momenta $\{k_1,\ldots,k_M\}$:

$$
e^{ik_jL}
=\prod_{l\ne j}
\left(-\,\frac{1-2\Delta\,e^{ik_j}+e^{i(k_j+k_l)}}{1-2\Delta\,e^{ik_l}+e^{i(k_j+k_l)}}\right),
\qquad j=1,\ldots,M.
$$

At $\Delta=0$ each factor reduces to $-1$, recovering the free-fermion quantization of the XX chain.
The energy of a Bethe state is

$$
E=\frac{J_{xy}\Delta L}{4}+J_{xy}\sum_{j=1}^{M}\left(\cos k_j-\Delta\right).
$$

### Ground-State Sector

The zero-field antiferromagnetic ground state lies in the half-filled magnon sector
$M=\tfrac{L}{2}$, that is $S_{\mathrm{tot}}^z=0$, with all momenta real. For a finite chain the ground
state is obtained by solving the Bethe equations for the $L/2$ real momenta and substituting them into
$E$ above. There is no elementary closed form for these momenta at general $\Delta$.

## Physical Quantities

### Ground-State Energy

For a finite chain, $E_0$ is the energy on the half-filled real-momentum solution of the Bethe
equations. In the thermodynamic limit the momenta fill a density $\rho(k)$ that solves the linear
integral equation of the method note, and the ground-state energy per site has closed forms at the
special points:

$$
e_0=
\begin{cases}
-\dfrac{J_{xy}}{\pi}, & \Delta=0\ (\text{XX, see } \texttt{xx-chain.md}),\\[0.8em]
J_{xy}\left(\dfrac{1}{4}-\log 2\right), & \Delta=1\ (\text{Heisenberg}).
\end{cases}
$$

For general $0<\Delta<1$ the per-site energy is given by the root-density integral and is monotonic
between these values. Writing $\Delta=\cos\gamma$, the standard closed form is an integral whose
kernel must be matched to a reference before use as a benchmark.

### Magnetization Sectors

The conserved magnetization is $S_{\mathrm{tot}}^z=\tfrac{L}{2}-M$. The zero-field ground state sits at
$M=\tfrac{L}{2}$. A longitudinal field $h_z$ shifts the ground-state sector to a magnetized $M<L/2$,
whose energy and momenta again follow from the Bethe equations at fixed $M$.

### Correlators

The equal-time spin correlators of the XXZ chain are not free-fermion Wick contractions and have no
elementary finite-size closed form. They are computed from determinant or form-factor representations
of the algebraic Bethe ansatz. For benchmarking, the reliable exact quantities are the ground-state
energy from the Bethe roots and, in the thermodynamic limit, the known correlation exponents and
asymptotics.

### Correlation Length

The correlation length follows the regime structure: in the gapless range $0\le\Delta\le1$ the spin
correlations are algebraic and $\xi=\infty$, while in the gapped range $\Delta>1$ the Néel-ordered
chain has a finite $\xi$ set by the spectral gap.

## References

- [method/bethe-ansatz.md](method/bethe-ansatz.md)
- [xx-chain.md](xx-chain.md)
- C. N. Yang and C. P. Yang, "One-Dimensional Chain of Anisotropic Spin-Spin Interactions. I.", Physical Review 150, 321 (1966).
- J. des Cloizeaux and J. J. Pearson, "Spin-Wave Spectrum of the Antiferromagnetic Linear Chain", Physical Review 128, 2131 (1962).
- M. Takahashi, *Thermodynamics of One-Dimensional Solvable Models*, Cambridge University Press (1999).
