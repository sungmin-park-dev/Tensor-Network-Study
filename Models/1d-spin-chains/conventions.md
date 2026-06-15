# Conventions

Status: first theory specification  
Scope: the interpretation rules shared by the documents, code, and reports of the TNS 1D spin-chain
model notes and projects

## 1. Purpose

This document fixes the indexing, boundary condition, operator normalization, sign convention, and
numerical comparison convention used by the TNS 1D spin-chain model notes and the related projects.
Symbols and code field names are managed in [parameters-and-symbols.md](parameters-and-symbols.md);
this document defines the physical meaning and computational rules attached to those symbols.

These conventions apply to the Hamiltonian definition in
[model-hamiltonian.md](model-hamiltonian.md). In particular, the definitions of the geometry symbol
$\mathcal{G}$, chain length $L$, boundary condition $b$, model parameters $J_{xy}$, $J_z$, $h_z$,
$h_x$, $K$, $\mathcal{C}_{\mathrm{cl}}$, and the energy symbols $E_0$ and $e_0$ follow
[parameters-and-symbols.md](parameters-and-symbols.md).

## 2. Indexing And Bond Order

Site indices follow a 0-based convention. On a chain of length $L$, the sites are labeled
$i=0,1,\ldots,L-1$.

The nearest-neighbor bond list has a deterministic order. Under open boundary conditions it is
$(0,1),(1,2),\ldots,(L-2,L-1)$. Under periodic boundary conditions the boundary bond $(L-1,0)$ is
appended at the end. This order must be identical across ED matrix construction, geometry diagrams,
and report tables.

## 3. Boundary Conditions

The boundary condition is carried by a field named `bc`.

| `bc` value | Meaning | Bond content |
|---|---|---|
| `open` | open boundary condition | nearest-neighbor bonds only |
| `periodic` | periodic boundary condition | nearest-neighbor bonds plus $(L-1,0)$ |

The abbreviations OBC and PBC may be used in prose. In code and serialized run metadata, prefer
`open` and `periodic`.

PBC is realized naturally in ED and graph-based NQS by adding the boundary edge. In TN/DMRG, PBC is an
algorithmically heavier choice, so OBC and PBC results are not held to the same tolerance expectation.
This difference is recorded as part of the solver-seam evidence, not as an error.

## 4. Operator Normalization

Pauli operators are written $\sigma^a$ and spin operators $S^a=\sigma^a/2$, with
$a\in\{x,y,z\}$.

The default operator normalization is the spin operator $S^a$. Unless stated otherwise, the XXZ term
and the Zeeman term are therefore written with $S^a$.

The cluster term does not yet fix a normalization. The Pauli cluster convention uses $O^a=\sigma^a$
and the spin cluster convention uses $O^a=S^a$. The conversion between the two couplings is managed in
`parameters-and-symbols.md`.

## 5. Hamiltonian Sign Convention

The XXZ interaction follows the sign convention

$$
H_{\mathrm{XXZ}}
= \sum_{\langle i,j\rangle}
\left[
J_{xy}(S_i^xS_j^x+S_i^yS_j^y)+J_zS_i^zS_j^z
\right].
$$

In this convention, $J_{xy}>0$ and $J_z>0$ are antiferromagnetic couplings.

The Zeeman term is written $H_{\mathrm{Zeeman}}=-h_z\sum_iS_i^z-h_x\sum_iS_i^x$. A positive $h_z$
therefore energetically favors spin polarization along $+z$.

The cluster term follows the minus-sign convention
$H_{\mathrm{cluster}}=-K\sum_i O_{i-1}^{x}O_i^{z}O_{i+1}^{x}$. The normalization of $O^a$ is fixed in
the cluster slice.

## 6. Symmetry And Conservation Labels

The total $S^z$ is $S_{\mathrm{tot}}^z=\sum_iS_i^z$. The XXZ Hamiltonian with $h_x=0$ conserves total
$S^z$. Once the transverse field $h_x$ is turned on, this conservation is generally broken.

Solver metadata must record the conservation assumption explicitly. For example, a DMRG run records
`conserve_sz=true` or the corresponding backend setting, and an NQS run records whether it used the
full Hilbert space or a fixed-$S^z$ sector.

## 7. Numerical Comparison Convention

The ground-state energy is written $E_0$ and the site-normalized energy $e_0=E_0/L$. When both values
exist, the report table records both.

By default, the error is recorded as the absolute error
$|E_{\mathrm{solver}}-E_{\mathrm{reference}}|$ together with the per-site error
$|e_{\mathrm{solver}}-e_{\mathrm{reference}}|$. For a stochastic solver, the energy variance, run seed,
and sample or iteration count are recorded as additional metadata.

A thermodynamic-limit anchor and a finite-$L$ exact reference are not treated as the same kind of
reference. The Heisenberg value $1/4-\log 2$ is not a finite-$L$ ED pass/fail threshold but an anchor
for interpreting scale and finite-size drift.

## 8. Document-To-Code Traceability

The documents and the implementation maintain the following correspondence.

| Theory artifact | Code/report artifact |
|---|---|
| parameter and symbol table | `spin_models.py` metadata now; later serialized run metadata |
| site and boundary convention | `spin_system.py`, `spin_models.py`, `run_method_probe.py` output |
| Hamiltonian term definitions | `spin_system.py`, `spin_models.py`, `method_form.py` term records |
| method-specific required inputs | `method_form.py`, `tests/test_method_forms.py` |
| exact reference formulae | deferred `exact_solutions.py`, validation tests |
| comparison tolerance | deferred `validation.py`, report pass/fail table |
| solver-result and findings schema | deferred `reports/findings.md` and benchmark/report artifacts |

When a new solver or term is added, the code is not changed alone. First update the convention in the
relevant theory document, then confirm that the update is reflected in the report metadata.
