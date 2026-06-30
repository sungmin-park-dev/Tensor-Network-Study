"""Exact diagonalization backend for project-local SpinSystem objects."""

from __future__ import annotations

import time
from collections.abc import Mapping
from typing import Any

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

from ..method_form import ED, MethodForm, change_form
from ..results import SolverResult
from ..spin_system import SpinSystem


def _as_sparse(matrix: np.ndarray) -> sp.csr_matrix:
    return sp.csr_matrix(np.asarray(matrix, dtype=complex))


def _term_operator(
    *,
    term: Mapping[str, Any],
    n_sites: int,
    local_dimension: int,
    local_operator_matrices: Mapping[str, np.ndarray],
) -> sp.csr_matrix:
    identity = sp.identity(local_dimension, dtype=complex, format="csr")
    by_site: dict[int, sp.csr_matrix] = {}
    for operator in term["operators"]:
        site = int(operator["site"])
        matrix = _as_sparse(local_operator_matrices[operator["name"]])
        by_site[site] = matrix if site not in by_site else by_site[site] @ matrix

    full = sp.csr_matrix([[1.0 + 0.0j]])
    for site in range(n_sites):
        full = sp.kron(full, by_site.get(site, identity), format="csr")
    return full


def hamiltonian_matrix_from_form(form: MethodForm) -> sp.csr_matrix:
    """Assemble the sparse many-body Hamiltonian from an ED MethodForm."""

    if form.method != ED.name:
        raise ValueError(f"expected ED MethodForm, got {form.method!r}")
    basis = form.payload["basis"]
    n_sites = int(basis["n_sites"])
    local_dimension = int(basis["local_dimension"])
    dimension = int(basis["dimension"])
    local_operator_matrices = form.payload["local_operator_matrices"]

    hamiltonian = sp.csr_matrix((dimension, dimension), dtype=complex)
    for term in form.payload["matrix_terms"]:
        coefficient = complex(term["coefficient"])
        hamiltonian = hamiltonian + coefficient * _term_operator(
            term=term,
            n_sites=n_sites,
            local_dimension=local_dimension,
            local_operator_matrices=local_operator_matrices,
        )
    return hamiltonian


def _ground_state(hamiltonian: sp.csr_matrix, *, dense_threshold: int) -> tuple[float, np.ndarray, np.ndarray]:
    dimension = hamiltonian.shape[0]
    if dimension <= dense_threshold:
        eigenvalues, eigenvectors = np.linalg.eigh(hamiltonian.toarray())
    else:
        eigenvalues, eigenvectors = eigsh(hamiltonian, k=1, which="SA")
        order = np.argsort(eigenvalues)
        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]
    return float(np.real_if_close(eigenvalues[0])), np.asarray(eigenvectors[:, 0]), np.asarray(eigenvalues)


def solve_ed(system: SpinSystem, *, dense_threshold: int = 512) -> SolverResult:
    """Solve the ground state of a SpinSystem through its ED MethodForm."""

    started = time.perf_counter()
    form = change_form(system, ED)
    hamiltonian = hamiltonian_matrix_from_form(form)
    energy, state, eigenvalues = _ground_state(hamiltonian, dense_threshold=dense_threshold)
    wall_time = time.perf_counter() - started

    return SolverResult(
        solver_name="ED",
        energy=energy,
        energy_per_site=energy / system.length,
        state=state,
        state_type="vector",
        num_sites=system.length,
        model_params=dict(system.metadata),
        metadata={
            "hilbert_dim": hamiltonian.shape[0],
            "wall_time": wall_time,
            "eigenvalues": eigenvalues,
            "bc": system.bc,
            "term_count": len(system.terms),
        },
    )
