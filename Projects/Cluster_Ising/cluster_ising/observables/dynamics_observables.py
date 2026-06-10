"""
Observables for time-dependent dynamics (Phase 2).

Provides measurement functions for use with TDVP evolution,
tracking how observables evolve under time-dependent Hamiltonians.
"""

import numpy as np


def magnetization_profile(state, L, state_type='mps'):
    """
    Local magnetization profile ⟨σ^z_j⟩ for all sites.

    Parameters
    ----------
    state : MPS or ndarray
        Quantum state.
    L : int
        Number of sites.
    state_type : str
        'mps' or 'vector'.

    Returns
    -------
    ndarray of shape (L,)
        Local magnetization at each site.
    """
    if state_type == 'mps':
        return np.real(state.expectation_value('Sigmaz'))
    elif state_type == 'vector':
        from .order_parameters import _local_expectations_ed, _SIGMA_Z
        return _local_expectations_ed(state, _SIGMA_Z, L)


def total_magnetization(state, L, state_type='mps'):
    """Total magnetization M = Σ ⟨σ^z_j⟩."""
    return np.sum(magnetization_profile(state, L, state_type))


def loschmidt_echo(psi_t, psi_0):
    """
    Loschmidt echo |⟨ψ₀|ψ(t)⟩|².

    Parameters
    ----------
    psi_t : MPS
        Time-evolved state.
    psi_0 : MPS
        Initial state.

    Returns
    -------
    float
        Loschmidt echo (0 ≤ L ≤ 1).
    """
    overlap = psi_t.overlap(psi_0)
    return np.abs(overlap)**2


def entanglement_growth_rate(times, entropies):
    """
    Compute entanglement growth rate dS/dt.

    For quench to a critical point, expect linear growth: S(t) ~ v_E * t.

    Parameters
    ----------
    times : ndarray
        Time values.
    entropies : ndarray
        Entanglement entropy values.

    Returns
    -------
    v_E : float
        Entanglement velocity (slope of S vs t).
    """
    if len(times) < 2:
        return 0.0

    # Linear fit to the initial growth regime
    mask = entropies < 0.8 * np.max(entropies)  # before saturation
    if np.sum(mask) < 2:
        mask = np.ones_like(times, dtype=bool)

    coeffs = np.polyfit(times[mask], entropies[mask], 1)
    return coeffs[0]


def stroboscopic_observables(times, observable_values, period):
    """
    Extract stroboscopic data from Floquet dynamics.

    Returns observable values at integer multiples of the driving period.

    Parameters
    ----------
    times : ndarray
        All time values.
    observable_values : ndarray
        Observable at each time.
    period : float
        Driving period T = 2π/ω.

    Returns
    -------
    stroboscopic_times : ndarray
    stroboscopic_values : ndarray
    """
    n_periods = int(times[-1] / period)
    strob_times = []
    strob_values = []

    for n in range(1, n_periods + 1):
        t_target = n * period
        idx = np.argmin(np.abs(times - t_target))
        strob_times.append(times[idx])
        strob_values.append(observable_values[idx])

    return np.array(strob_times), np.array(strob_values)
