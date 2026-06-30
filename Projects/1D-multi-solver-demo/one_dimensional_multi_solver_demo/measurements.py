"""ED state measurement helpers."""

from __future__ import annotations

from collections.abc import Mapping

import numpy as np
import scipy.sparse as sp

from .results import SolverResult
from .spin_system import SpinSystem


def many_body_operator(
    system: SpinSystem,
    local_operators: Mapping[int, np.ndarray],
) -> sp.csr_matrix:
    """Build a sparse product operator from site-indexed local matrices."""

    local_dimension = system.local_space.dimension
    identity = sp.identity(local_dimension, dtype=complex, format="csr")
    full = sp.csr_matrix([[1.0 + 0.0j]])
    for site in range(system.length):
        matrix = local_operators.get(site)
        full = sp.kron(
            full,
            identity if matrix is None else sp.csr_matrix(np.asarray(matrix, dtype=complex)),
            format="csr",
        )
    return full


def expectation_value(
    result: SolverResult,
    system: SpinSystem,
    local_operators: Mapping[int, np.ndarray],
) -> complex:
    """Return <psi|O|psi> for an ED state vector."""

    operator = many_body_operator(system, local_operators)
    psi = result.state
    return complex(psi.conj() @ (operator @ psi))


def one_site_expectation(result: SolverResult, system: SpinSystem, operator_name: str, site: int) -> float:
    matrix = system.local_space.operators[operator_name]
    value = expectation_value(result, system, {site: matrix})
    return float(np.real_if_close(value))


def two_site_expectation(
    result: SolverResult,
    system: SpinSystem,
    operator_name: str,
    site_i: int,
    site_j: int,
) -> float:
    matrix = system.local_space.operators[operator_name]
    if site_i == site_j:
        value = expectation_value(result, system, {site_i: matrix @ matrix})
    else:
        value = expectation_value(result, system, {site_i: matrix, site_j: matrix})
    return float(np.real_if_close(value))
