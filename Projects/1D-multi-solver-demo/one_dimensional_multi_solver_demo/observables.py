"""Project-local observable calculations for ED results."""

from __future__ import annotations

import numpy as np

from .measurements import one_site_expectation, two_site_expectation
from .results import SolverResult
from .spin_system import SpinSystem


def site_expectations(result: SolverResult, system: SpinSystem, operator_name: str) -> list[dict[str, float]]:
    """Return one-site expectation values for a named local operator."""

    return [
        {"site": site.index, operator_name: one_site_expectation(result, system, operator_name, site.index)}
        for site in system.sites
    ]


def spin_vectors(result: SolverResult, system: SpinSystem) -> list[dict[str, float]]:
    """Return site-resolved <Sx>, <Sy>, <Sz> vectors."""

    rows = []
    for site in system.sites:
        sx = one_site_expectation(result, system, "Sx", site.index)
        sy = one_site_expectation(result, system, "Sy", site.index)
        sz = one_site_expectation(result, system, "Sz", site.index)
        rows.append(
            {
                "site": site.index,
                "Sx": sx,
                "Sy": sy,
                "Sz": sz,
                "norm": float(np.sqrt(sx**2 + sy**2 + sz**2)),
            }
        )
    return rows


def connected_correlator_matrix(
    result: SolverResult,
    system: SpinSystem,
    operator_name: str = "Sz",
) -> np.ndarray:
    """Return C_ij = <Oi Oj> - <Oi><Oj> for a named operator."""

    one_site = np.array(
        [one_site_expectation(result, system, operator_name, site.index) for site in system.sites],
        dtype=float,
    )
    corr = np.zeros((system.length, system.length), dtype=float)
    for i in range(system.length):
        for j in range(system.length):
            two_site = two_site_expectation(result, system, operator_name, i, j)
            corr[i, j] = two_site - one_site[i] * one_site[j]
    return corr


def half_chain_entropy(result: SolverResult) -> float:
    """Return the half-chain von Neumann entropy in nats."""

    left = result.num_sites // 2
    right = result.num_sites - left
    spectrum = np.linalg.svd(result.state.reshape(2**left, 2**right), compute_uv=False) ** 2
    spectrum = spectrum[spectrum > 1e-14]
    return float(-np.sum(spectrum * np.log(spectrum)))
