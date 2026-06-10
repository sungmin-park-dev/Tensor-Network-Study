"""Tests for thermodynamic reproduction helpers."""

import numpy as np

from cluster_ising.analysis.central_charge import verify_three_ising_decomposition
from cluster_ising.analysis.thermodynamics import (
    free_energy_equivalence,
    ising_free_energy_density,
)
from cluster_ising.models.exact_solution import free_energy_density


def test_ising_free_energy_matches_cluster_ising_ground_state():
    """At T=0, the effective Ising density matches the CIM density."""
    for lam in [0.5, 1.0, 1.5]:
        assert np.isclose(
            ising_free_energy_density(lam, np.inf),
            free_energy_density(lam, np.inf),
            atol=1e-12,
        )


def test_ising_free_energy_matches_cluster_ising_thermal_state():
    """At finite temperature, the effective Ising density still matches."""
    for beta in [5.0, 2.0, 1.0]:
        for lam in [0.5, 1.0, 1.5]:
            assert np.isclose(
                ising_free_energy_density(lam, beta),
                free_energy_density(lam, beta),
                atol=1e-12,
            )


def test_free_energy_equivalence_reports_small_error():
    """The reproduction helper should report machine-level agreement."""
    result = free_energy_equivalence(np.linspace(0.2, 1.8, 7), beta=2.0)
    assert result["max_error"] < 1e-10


def test_verify_three_ising_decomposition_uses_density_not_triple_density():
    """The decomposition check compares per-site densities correctly."""
    energies = np.array([-1.0, -1.2, -1.4])
    result = verify_three_ising_decomposition([0.5, 1.0, 1.5], energies, energies)
    assert result["max_error"] == 0.0
