# Exact-Solution Methods

## Introduction

This folder collects the main methods used to obtain exact solutions of 1D spin-chain models. Rather
than fixing the numerical value of a specific benchmark point, each note explains which kind of
Hamiltonian the method applies to and which reference it provides in this project.

## Methods

| Method | File | Connected limit |
|---|---|---|
| Bethe ansatz | `bethe-ansatz.md` | XXZ chain, Heisenberg AFM point |
| Bogoliubov diagonalization | `bogoliubov-diagonalization.md` | Quadratic fermions with pairing |
| Free-fermion diagonalization | `free-fermion-diagonalization.md` | Number-conserving quadratic fermions |
| Jordan-Wigner transformation | `jordan-wigner.md` | XX point, TFIM limit |

## Usage Principles

These method notes do not claim that the full Hamiltonian family is exactly solvable. For generic
parameter ranges, neither an exact solution nor integrability is expected, and an exact reference is
used only in specific solvable limits.

## References

- [../../model-hamiltonian.md](../../model-hamiltonian.md)
- [1D multi-solver first slice](../../../../Projects/1D-multi-solver-demo/progress/open/first-slice.md)
