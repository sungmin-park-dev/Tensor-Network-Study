# Cluster-Ising Paper Reproduction

This project reproduces the main numerical claims of
`Phys. Rev. A 84, 022304 (2011)`, "Statistical mechanics of the cluster Ising model".

A structured digest of that source paper (model definition, exact-solution roadmap, order
parameters, entanglement, and central charge, with equation/section pointers) lives in the
model-theory notes at
[`Models/1d-spin-chains/exact-solutions/cluster-ising-chain.md`](../../Models/1d-spin-chains/exact-solutions/cluster-ising-chain.md).

## Quick start

From [Projects/Cluster_Ising](/Users/david/GitHub/Tensor-Network-Study/Projects/Cluster_Ising), run:

```bash
python scripts/reproduce_paper.py
```

For a stronger central-charge fit, include larger DMRG systems:

```bash
python scripts/reproduce_paper.py --with-dmrg
```

Outputs are written to `data/figures/paper_reproduction/` and include:

- order parameters and residual entanglement
- exact correlation curves
- free-energy equivalence to the effective Ising description
- pairwise concurrence checks
- central-charge extraction at the critical point

## Notes

- The lightweight reproduction path uses exact formulas and ED so that it can be
  rerun quickly.
- `--with-dmrg` improves the critical-point entropy fit at the cost of runtime.
- DMRG and NQS remain available in the rest of the project for larger-scale
  benchmarking, but they are not required for the default paper-reproduction run.
