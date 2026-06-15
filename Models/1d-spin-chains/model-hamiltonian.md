# 1D Spin-Chain Model Hamiltonian

Status: first theory specification  
Scope: the reusable 1D spin-1/2 Hamiltonian family for the TNS project

## 1. Introduction

This document defines the 1D spin-1/2 Hamiltonian family reused across the TNS project. The standard
definitions of the geometry symbols, model parameters, and code field names are managed in
[parameters-and-symbols.md](parameters-and-symbols.md), and the indexing, boundary condition,
operator normalization, and sign convention follow [conventions.md](conventions.md). Taking those two
documents as given, this note specifies the term-by-term structure of the Hamiltonian and the
first-slice subsystem. It therefore does not repeat the symbols and conventions, and concentrates on
the mathematical structure of the Hamiltonian itself.

## 2. Model Hamiltonian

The Hamiltonian considered in this project is defined by an XXZ exchange term, a Zeeman field term,
and a cluster interaction term.

$$
H (\mathbf{J}, \mathbf{h}, K; {\mathcal{G}} )= H_{\mathrm{XXZ}} (\mathbf{J}; {\mathcal{G}}) + H_{\mathrm{Zeeman}} (\mathbf{h}; {\mathcal{G}})  + H_{\mathrm{cluster}} (K; {\mathcal{G}}).
$$

Here $\mathcal{G}$ denotes the model geometry, defined in Section 2.1. The term-by-term definitions
and parameters of the Hamiltonian are given in Section 2.2.

### 2.1 Lattice Geometry (${\mathcal{G}}$)

The Hamiltonian is first defined on a fixed system geometry, denoted $\mathcal{G}$. This symbol refers
to the geometric specification of the physical system, as distinct from the model parameters.

The first-slice geometry is a 1D chain of length $L$. The site indices are $i=0,1,\ldots,L-1$. Under
`open` boundary conditions, the nearest-neighbor bonds are $(i,i+1)$ for $i=0,\ldots,L-2$. Under
`periodic` boundary conditions, the boundary bond $(L-1,0)$ is added to these.

In the rest of this document the geometry is taken to be fixed by context, and the $\mathcal{G}$
subscript is omitted. Thus $\sum_{\langle i,j\rangle}$ means the sum over the nearest-neighbor bonds
of the currently chosen 1D chain geometry.

### 2.2 The Hamiltonian ($H$) And Its Interaction Terms

Each term below shares the site indexing and boundary convention of Section 2.1.

#### 2.2.1 XXZ Exchange Term

The XXZ interaction is defined as

$$
H_{\mathrm{XXZ}}(J_{xy},J_z)
= \sum_{\langle i,j\rangle}
\left[
J_{xy}\left(S_i^x S_j^x + S_i^y S_j^y\right)
+ J_z S_i^z S_j^z
\right].
$$

Here $\langle i,j\rangle$ denotes the nearest-neighbor bonds of the chosen geometry. The anisotropy is
defined as $\Delta=J_z/J_{xy}$.

#### 2.2.2 Zeeman Term

The Zeeman field allows both a longitudinal field $h_z$ and a transverse field $h_x$.

$$
H_{\mathrm{Zeeman}}(h_z,h_x)
= -h_z \sum_{i=0}^{L-1} S_i^z
- h_x \sum_{i=0}^{L-1} S_i^x .
$$

#### 2.2.3 Cluster Term

The cluster interaction is taken as a three-site product of spin operators.

$$
H_{\mathrm{cluster}}(K)
= -K \sum_i S_{i-1}^{x} S_i^{z} S_{i+1}^{x}.
$$

This cluster term is interpreted as a 1D chain term. Under periodic boundary conditions, the site
indices are read modulo $L$. How the cluster term is truncated under open boundary conditions is fixed
separately in the cluster-term slice.

## 3. Exact Solution

For generic parameter ranges, neither an exact solution nor integrability is expected. In specific
limits, however, an exact reference can be obtained through the Jordan-Wigner transformation or the
Bethe ansatz. The reference notes are managed under `exact-solutions/`.

| Limit | Condition | Method | Reference note |
|---|---|---|---|
| XXZ chain | $K=0$, $h_x=0$ | Bethe ansatz | `exact-solutions/xxz-chain.md` |
| XX point | $K=0$, $h_x=h_z=0$, $J_z=0$ | Jordan-Wigner / free fermion | `exact-solutions/xx-chain.md` |
| Heisenberg AFM point | $K=0$, $h_x=h_z=0$, $J_{xy}=J_z=1$ | Bethe ansatz | `exact-solutions/xxz-chain.md` |
| TFIM limit | $K=0$, $J_{xy}=0$, $J_z\ne0$, $h_x\ne0$ | Jordan-Wigner | `exact-solutions/tfim-chain.md` |

The detailed derivations and finite-size caveats of the exact solutions are managed under
`exact-solutions/`. How each project uses these benchmarks is managed in that project's progress or
plan, for example
[1D multi-solver first slice](../../Projects/1D-multi-solver-demo/progress/open/first-slice.md).

## 4. Physical Properties Of The Model Hamiltonian

This section is written later.

## 5. References

This document is read together with the following theory documents.

| Document | Role |
|---|---|
| `parameters-and-symbols.md` | source of truth for geometry symbols, model parameters, and code field names |
| `conventions.md` | indexing, boundary condition, operator normalization, sign convention |
| [1D multi-solver first slice](../../Projects/1D-multi-solver-demo/progress/open/first-slice.md) | first-slice partial Hamiltonian and benchmark candidates |
| `exact-solutions/README.md` | shared usage rules for the exact-solution notes |
| `exact-solutions/xx-chain.md` | XX point finite-chain reference |
| `exact-solutions/xxz-chain.md` | XXZ chain Bethe ansatz reference |
| `exact-solutions/method/bethe-ansatz.md` | coordinate Bethe ansatz method |
