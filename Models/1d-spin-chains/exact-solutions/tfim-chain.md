# TFIM Model Exact Solution

## Introduction

- This note records the exact Jordan-Wigner reference for the TFIM model.
- In the generalized Hamiltonian family used here, the same model is obtained as the
  transverse-field Ising limit.
- The general Jordan-Wigner transformation is described in [method/jordan-wigner.md](method/jordan-wigner.md).
- The generic Bogoliubov-de Gennes diagonalization and its Gaussian ground-state correlations are
  described in [method/bogoliubov-diagonalization.md](method/bogoliubov-diagonalization.md).
- The finite-size PBC reference must specify the fermion-parity sector before using the
  momentum-space spectrum.

## Definition

The TFIM model is obtained by setting $K=0$, $J_{xy}=0$, $J_z\ne0$, and $h_x\ne0$. The Hamiltonian is

$$
H_{\mathrm{TFIM}}
=J_z\sum_{\langle i,j\rangle}S_i^zS_j^z
-h_x\sum_{i=0}^{L-1}S_i^x.
$$

Choose rotated axes $\tau_i^x=S_i^z$ and $\tau_i^z=-S_i^x$. Then the Hamiltonian becomes the standard
transverse-field Ising form used for the Jordan-Wigner solution:

$$
H_{\mathrm{TFIM}}
=J_z\sum_{\langle i,j\rangle}\tau_i^x\tau_j^x
+h_x\sum_{i=0}^{L-1}\tau_i^z.
$$

Here $\tau$ denotes the rotated spin-$1/2$ operators, with $\tau^a=\sigma^a/2$ in the rotated frame.

## Solution

The TFIM maps to a quadratic fermion Hamiltonian with pairing terms under the Jordan-Wigner
transformation. We first reduce the rotated Ising bond to fermions, then fix the boundary term, and
then diagonalize with a Bogoliubov transformation.

### Fermionic Hamiltonian

#### Jordan-Wigner Setup

We use the convention from [method/jordan-wigner.md](method/jordan-wigner.md):

$$
\tau_i^+=c_i^\dagger P_i,
\qquad
\tau_i^-=P_i c_i,
\qquad
\tau_i^z=n_i-\frac{1}{2},
\qquad
P_i=\prod_{\ell<i}p_\ell,
\qquad
p_\ell=1-2n_\ell.
$$

Because $\tau_i^x=\tfrac{1}{2}(\tau_i^++\tau_i^-)$ and the site-$i$ operators commute with the string
$P_i$ built from sites $\ell<i$,

$$
\tau_i^x=\frac{1}{2}\left(c_i^\dagger P_i+P_i c_i\right)=\frac{1}{2}P_i\left(c_i^\dagger+c_i\right).
$$

The local parity operator satisfies

$$
p_i c_i=c_i,
\qquad
p_i c_i^\dagger=-c_i^\dagger,
$$

so that $(c_i^\dagger+c_i)p_i=c_i^\dagger-c_i$.

For a bulk bond $(i,i+1)$ use $P_{i+1}=P_i p_i$ and $P_i^2=1$:

$$
\begin{aligned}
\tau_i^x\tau_{i+1}^x
&=\frac{1}{4}P_i\left(c_i^\dagger+c_i\right)P_i p_i\left(c_{i+1}^\dagger+c_{i+1}\right)\\
&=\frac{1}{4}\left(c_i^\dagger+c_i\right)p_i\left(c_{i+1}^\dagger+c_{i+1}\right)\\
&=\frac{1}{4}\left(c_i^\dagger-c_i\right)\left(c_{i+1}^\dagger+c_{i+1}\right).
\end{aligned}
$$

The Ising bond therefore becomes a fermion hopping-plus-pairing term. The transverse field is already
diagonal in the fermion number, since $\tau_i^z=n_i-\tfrac{1}{2}$.

#### OBC Hamiltonian

For OBC no bond crosses the Jordan-Wigner ordering cut, so summing the bulk bond over the chain gives

$$
H_{\mathrm{TFIM}}^{\mathrm{OBC}}
=\frac{J_z}{4}\sum_{i=0}^{L-2}
\left(c_i^\dagger-c_i\right)\left(c_{i+1}^\dagger+c_{i+1}\right)
+h_x\sum_{i=0}^{L-1}\left(n_i-\frac{1}{2}\right).
$$

#### PBC Hamiltonian

For PBC the boundary bond $(L-1,0)$ crosses the cut and carries the full parity string. With $P_0=1$
and $P_{L-1}=\prod_{\ell=0}^{L-2}p_\ell$, inserting $p_{L-1}^2=1$ gives

$$
P_{L-1}=\left(\prod_{\ell=0}^{L-1}p_\ell\right)p_{L-1}=\Pi\,p_{L-1},
\qquad
\Pi=\prod_{i=0}^{L-1}p_i=(-1)^{N_f}.
$$

Using $\tau_0^x=\tfrac{1}{2}(c_0^\dagger+c_0)$ and $p_{L-1}(c_{L-1}^\dagger+c_{L-1})=-(c_{L-1}^\dagger-c_{L-1})$,

$$
\tau_{L-1}^x\tau_0^x
=\frac{1}{4}\Pi\,p_{L-1}\left(c_{L-1}^\dagger+c_{L-1}\right)\left(c_0^\dagger+c_0\right)
=-\frac{1}{4}\Pi\left(c_{L-1}^\dagger-c_{L-1}\right)\left(c_0^\dagger+c_0\right).
$$

The boundary bond is the bulk fermion term times $-\Pi$, so PBC must be solved in fixed fermion-parity
sectors. In a sector $\Pi=\lambda_{\Pi}$, absorbing the factor $-\lambda_{\Pi}$ into a boundary
condition $c_L=-\lambda_{\Pi}c_0$ writes the Hamiltonian as a single bulk sum:

$$
H_{\mathrm{TFIM}}^{\mathrm{PBC}}(\lambda_{\Pi})
=\frac{J_z}{4}\sum_{i=0}^{L-1}
\left(c_i^\dagger-c_i\right)\left(c_{i+1}^\dagger+c_{i+1}\right)
+h_x\sum_{i=0}^{L-1}\left(n_i-\frac{1}{2}\right),
\qquad c_L=-\lambda_{\Pi}c_0.
$$

Here $c_L$ is a boundary-condition shorthand, not an additional physical site. The parity sector is
therefore part of the finite-size TFIM definition.

### Diagonalization

Both Hamiltonians are quadratic with pairing. We diagonalize them with
[method/bogoliubov-diagonalization.md](method/bogoliubov-diagonalization.md), which maps a Hamiltonian
$\sum_{ij}c_i^\dagger A_{ij}c_j+\tfrac{1}{2}\sum_{ij}(c_i^\dagger B_{ij}c_j^\dagger+\text{h.c.})$ to
quasiparticle modes.

#### OBC Diagonalization

Expanding the bulk term, $(c_i^\dagger-c_i)(c_{i+1}^\dagger+c_{i+1})
=c_i^\dagger c_{i+1}+c_{i+1}^\dagger c_i+c_i^\dagger c_{i+1}^\dagger-c_ic_{i+1}$, so
$H_{\mathrm{TFIM}}^{\mathrm{OBC}}$ has the BdG matrices

$$
A_{ii}=h_x,
\qquad
A_{i,i+1}=A_{i+1,i}=\frac{J_z}{4},
\qquad
B_{i,i+1}=-B_{i+1,i}=\frac{J_z}{4},
\qquad
E_{\mathrm{const}}=-\frac{h_xL}{2},
$$

with all other entries zero. Diagonalizing the $2L\times2L$ BdG matrix built from $A$ and $B$ gives the
finite-chain quasiparticle energies $\epsilon_\alpha$ and modes $(u^{(\alpha)},v^{(\alpha)})$.

#### PBC Diagonalization

In a sector, the boundary condition $c_L=-\lambda_{\Pi}c_0$ fixes the allowed momentum grid through
$e^{ikL}=-\lambda_{\Pi}$:

$$
k_m=
\begin{cases}
\dfrac{2\pi m}{L}, & \lambda_{\Pi}=-1,\\[0.8em]
\dfrac{2\pi(m+1/2)}{L}, & \lambda_{\Pi}=+1,
\end{cases}
\qquad m=0,1,\ldots,L-1.
$$

Let $K_{\lambda_{\Pi}}$ denote this grid. Fourier transforming with $c_j=L^{-1/2}\sum_{k}e^{ikj}c_k$,
the number-conserving part gives $\sum_k(h_x+\tfrac{J_z}{2}\cos k)c_k^\dagger c_k$, and antisymmetrizing
the pairing part gives a coefficient proportional to $\sin k$. The sector Hamiltonian therefore reduces
to the translation-invariant two-mode form of the method note with

$$
A(k)=\frac{h_x}{2}+\frac{J_z}{4}\cos k,
\qquad
B(k)=\frac{J_z}{4}\sin k.
$$

The quasiparticle spectrum is then

$$
\epsilon(k)
=2\sqrt{A(k)^2+B(k)^2}
=2\sqrt{
\left(\frac{h_x}{2}+\frac{J_z}{4}\cos k\right)^2
+\left(\frac{J_z}{4}\sin k\right)^2
}.
$$

### Bridge to Physical Quantities

The spin problem is now reduced to Bogoliubov quasiparticle levels with specified boundary sectors,
together with the Gaussian ground-state correlations of the method note. The next section fills these
levels and contracts these correlations to obtain energies and spin expectation values.

## Physical Quantities

### Many-Body Energy From Quasiparticle Levels

After Bogoliubov diagonalization the Hamiltonian has the form
$H=E_{\mathrm{vac}}+\sum_\alpha\epsilon_\alpha\gamma_\alpha^\dagger\gamma_\alpha$, so the many-body
energy is

$$
E[\{n_\alpha\}]
=E_{\mathrm{vac}}+\sum_\alpha n_\alpha\epsilon_\alpha,
\qquad n_\alpha\in\{0,1\}.
$$

For a translation-invariant PBC sector the levels are $\epsilon(k)$ on $K_{\lambda_{\Pi}}$ and the
vacuum energy is $E_{\mathrm{vac}}(\lambda_{\Pi})=-\tfrac{1}{2}\sum_{k\in K_{\lambda_{\Pi}}}\epsilon(k)$.

### Ground-State Energy

The finite-chain ground-state energy minimizes over the parity sectors and the allowed occupations:

$$
E_0
=\min_{\lambda_{\Pi}=\pm1}\ \min_{\{n_\alpha\}\in\mathcal{H}_{\lambda_{\Pi}}}
\left(E_{\mathrm{vac}}(\lambda_{\Pi})+\sum_\alpha n_\alpha\epsilon_\alpha\right).
$$

The inner minimization is not unconstrained: a state is physical in the sector $\lambda_{\Pi}$ only if
its total fermion parity equals $\lambda_{\Pi}$. The recipe a solver implements is

1. for each sector, build the grid $K_{\lambda_{\Pi}}$ and the spectrum $\epsilon(k)$, including the
   unpaired modes $k=0$ and (for the appropriate grid) $k=\pi$, whose occupation sets the parity of the
   Bogoliubov vacuum;
2. take the paired vacuum energy $E_{\mathrm{vac}}(\lambda_{\Pi})$ when its parity matches
   $\lambda_{\Pi}$, and otherwise add the smallest $\epsilon(k)$ in that sector to flip the parity;
3. take $E_0$ as the smaller of the two sector results.

This selection rule is what makes the finite-$L$ TFIM energy reproducible against ED.

### Ground-State Wavefunction

In a fixed sector the ground state is the Bogoliubov vacuum $\gamma_\alpha|\Omega_{\lambda_{\Pi}}\rangle=0$
for every positive-energy mode. In the translation-invariant paired sectors it has the BCS form

$$
|\Omega_{\lambda_{\Pi}}\rangle
\propto
\prod_{0<k<\pi}\left(u_k+v_k\,c_k^\dagger c_{-k}^\dagger\right)|0\rangle,
\qquad
u_k=\cos\theta_k,
\quad
v_k=i\sin\theta_k,
\quad
\tan2\theta_k=\frac{B(k)}{A(k)},
$$

with the unpaired $k=0$ and $k=\pi$ modes occupied or empty according to the sector parity.

### Energy Density

The site-normalized energy is $e_0=E_0/L$. In the thermodynamic limit of the translation-invariant
chain the parity constraint drops out and

$$
e_0
=-\frac{1}{4\pi}\int_0^{2\pi}\epsilon(k)\,dk.
$$

### Transverse Magnetization

The rotated transverse magnetization is $\langle\tau_i^z\rangle=\langle n_i\rangle-\tfrac{1}{2}$, and
since $\tau_i^z=-S_i^x$,

$$
\langle S_i^x\rangle=\frac{1}{2}-\langle n_i\rangle.
$$

The occupation follows from the ground-state correlation $\langle n_i\rangle=\langle c_i^\dagger c_i\rangle
=\sum_{\alpha:\epsilon_\alpha>0}v_i^{(\alpha)}v_i^{(\alpha)*}$ of the method note. For a
translation-invariant sector the per-mode occupation is $\langle n_k\rangle=\tfrac{1}{2}(1-2A(k)/\epsilon(k))$,
so the uniform transverse magnetization has the closed form

$$
\langle S_i^x\rangle
=\frac{1}{L}\sum_{k\in K_{\lambda_{\Pi}}}\frac{A(k)}{\epsilon(k)}.
$$

### Correlators

All spin correlators are Gaussian contractions of the Majorana operators

$$
w_{2i}=c_i+c_i^\dagger,
\qquad
w_{2i+1}=i\left(c_i^\dagger-c_i\right),
$$

with the real antisymmetric covariance matrix $\Gamma_{ab}=\tfrac{i}{2}\langle[w_a,w_b]\rangle$. The
covariance is assembled from the method-note contractions $\langle c_i^\dagger c_j\rangle$ and
$\langle c_ic_j\rangle$, so $\Gamma$ is fixed entirely by the Bogoliubov solution.

Local and short-range quantities are direct entries or Wick products of $\Gamma$:

$$
\langle S_i^x\rangle=-\frac{1}{2}\Gamma_{2i,2i+1},
\qquad
\langle S_i^xS_j^x\rangle
=\langle\tau_i^z\tau_j^z\rangle
=\frac{1}{4}\bigl(\Gamma_{2i,2i+1}\Gamma_{2j,2j+1}
-\Gamma_{2i,2j}\Gamma_{2i+1,2j+1}
+\Gamma_{2i,2j+1}\Gamma_{2i+1,2j}\bigr).
$$

The Ising order-parameter correlator $\langle S_i^zS_j^z\rangle=\langle\tau_i^x\tau_j^x\rangle$ carries
the Jordan-Wigner string, since $\tau_i^x=\tfrac{1}{2}P_iw_{2i}$. For $i<j$ the string is the ordered
product of the Majoranas $w_{2i+1},w_{2i+2},\ldots,w_{2j}$, an even set of size $2(j-i)$, so the
correlator is the Pfaffian of the covariance restricted to those indices:

$$
\langle S_i^zS_j^z\rangle
=\frac{1}{4}\,\operatorname{Pf}\Gamma\big|_{\{2i+1,\,2i+2,\,\ldots,\,2j\}}.
$$

Both forms are computable directly from $\Gamma$, so theory and code evaluate the same object.

### Entanglement Entropy

For a subsystem $A$, restrict the Majorana covariance to the sites of $A$ and bring it to the block
form with eigenvalue pairs $\pm\nu_a$ of $i\Gamma_A$. The von Neumann entanglement entropy is

$$
S_A
=-\sum_a\left[
\frac{1+\nu_a}{2}\log\frac{1+\nu_a}{2}
+\frac{1-\nu_a}{2}\log\frac{1-\nu_a}{2}
\right].
$$

### Correlation Length

The gap is $\Delta=\min_k\epsilon(k)$. With $A(k)$ and $B(k)$ above, $\epsilon(k)^2$ is minimized at
$k=\pi$, so

$$
\Delta=\left|h_x-\frac{J_z}{2}\right|.
$$

The correlation length is set by the imaginary momentum $k=i\kappa$ at which $\epsilon(i\kappa)=0$,
the nearest singularity of the spin correlator. In the gapped phases this gives the closed form

$$
\xi^{-1}=\left|\log\frac{2h_x}{J_z}\right|,
$$

which diverges, $\xi\to\infty$, on the critical line $\lvert 2h_x/J_z\rvert=1$ where the gap closes.

## References

- [method/jordan-wigner.md](method/jordan-wigner.md)
- [method/bogoliubov-diagonalization.md](method/bogoliubov-diagonalization.md)
- E. Lieb, T. Schultz, and D. Mattis, "Two soluble models of an antiferromagnetic chain", Annals of Physics 16, 407 (1961).
- P. Pfeuty, "The one-dimensional Ising model with a transverse field", Annals of Physics 57, 79 (1970).
