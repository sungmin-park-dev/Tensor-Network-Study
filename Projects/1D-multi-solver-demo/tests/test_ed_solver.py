"""Tests for project-local ED solving and observables."""

import numpy as np

from one_dimensional_multi_solver_demo import (
    build_spin_chain,
    connected_correlator_matrix,
    half_chain_entropy,
    match_exact_reference,
    site_expectations,
    solve_ed,
)


def test_ed_matches_finite_pbc_xx_bethe_reference():
    system = build_spin_chain(length=6, bc="periodic", jxy=1.0, jz=0.0, k=0.0, hz=0.0, hx=0.0)
    result = solve_ed(system)
    exact = match_exact_reference(system)

    assert exact is not None
    assert abs(result.energy - exact.energy) < 1e-10


def test_ed_matches_pure_cluster_stabilizer_energy():
    system = build_spin_chain(length=5, bc="open", jxy=0.0, jz=0.0, k=8.0, hz=0.0, hx=0.0)
    result = solve_ed(system)
    exact = match_exact_reference(system)

    assert exact is not None
    assert exact.energy == -3.0
    assert abs(result.energy - exact.energy) < 1e-10


def test_site_expectations_and_connected_correlator_for_product_state():
    system = build_spin_chain(length=3, bc="open", jxy=0.0, jz=0.0, k=0.0, hz=1.0, hx=0.0)
    result = solve_ed(system)

    sz = site_expectations(result, system, "Sz")
    corr = connected_correlator_matrix(result, system, "Sz")

    assert [row["Sz"] for row in sz] == [0.5, 0.5, 0.5]
    assert np.allclose(corr, np.zeros((3, 3)))
    assert half_chain_entropy(result) < 1e-12
