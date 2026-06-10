"""Tests for pairwise entanglement observables."""

import numpy as np

from cluster_ising.observables.pairwise_entanglement import (
    concurrence_from_density_matrix,
    exact_pairwise_concurrence,
    exact_two_spin_density_matrix,
)


def test_bell_state_has_unit_concurrence():
    """A Bell state should have concurrence 1."""
    psi = np.array([1.0, 0.0, 0.0, 1.0], dtype=complex) / np.sqrt(2.0)
    rho = np.outer(psi, psi.conj())
    assert np.isclose(concurrence_from_density_matrix(rho), 1.0, atol=1e-12)


def test_exact_two_spin_density_matrix_is_physical():
    """Exact thermodynamic two-spin state is Hermitian and normalized."""
    rho = exact_two_spin_density_matrix(3, 0.5)
    assert np.allclose(rho, rho.conj().T, atol=1e-12)
    assert np.isclose(np.trace(rho), 1.0, atol=1e-12)


def test_exact_pairwise_concurrence_vanishes_at_zero_temperature():
    """The exact thermodynamic pairwise concurrence vanishes in both phases."""
    for lam in [0.5, 1.0, 1.5]:
        for r in [1, 2, 3, 6]:
            assert exact_pairwise_concurrence(r, lam) < 1e-12


def test_exact_pairwise_concurrence_vanishes_at_finite_temperature():
    """The exact thermodynamic pairwise concurrence also vanishes thermally."""
    for beta in [5.0, 2.0, 1.0]:
        for r in [1, 2, 3, 6]:
            assert exact_pairwise_concurrence(r, 0.5, beta) < 1e-12
