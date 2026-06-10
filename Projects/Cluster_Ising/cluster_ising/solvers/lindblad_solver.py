"""
Lindblad master equation solver (Phase 3 - placeholder).

Implements open quantum system dynamics:
    dρ/dt = -i[H, ρ] + Σ_k γ_k (L_k ρ L_k† - ½{L_k† L_k, ρ})

Approaches to implement:
1. MPO density matrix evolution on doubled Hilbert space
2. Quantum trajectory (stochastic unraveling) with MPS
3. Exact integration for small systems (ED-based)

Status: Placeholder with ED-based exact Lindblad for small systems.
"""

import numpy as np
from scipy.integrate import solve_ivp

from .base_solver import Timer


# --- Lindblad operators ---

def dephasing_ops(N):
    """Dephasing: L_k = σ^z_k for each site."""
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    ops = []
    for k in range(N):
        ops.append(('dephasing', k, sz))
    return ops


def amplitude_damping_ops(N):
    """Amplitude damping: L_k = σ⁻_k."""
    sm = np.array([[0, 0], [1, 0]], dtype=complex)
    ops = []
    for k in range(N):
        ops.append(('decay', k, sm))
    return ops


def depolarizing_ops(N):
    """Depolarizing: L_k^α = σ^α_k / √3 for α ∈ {x, y, z}."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex) / np.sqrt(3)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex) / np.sqrt(3)
    sz = np.array([[1, 0], [0, -1]], dtype=complex) / np.sqrt(3)
    ops = []
    for k in range(N):
        ops.append(('depol_x', k, sx))
        ops.append(('depol_y', k, sy))
        ops.append(('depol_z', k, sz))
    return ops


# --- ED-based exact Lindblad evolution (small systems) ---

def _build_full_operator(local_op, site, N):
    """Build 2^N × 2^N operator from local operator."""
    I2 = np.eye(2, dtype=complex)
    result = np.array([[1.0]], dtype=complex)
    for k in range(N):
        result = np.kron(result, local_op if k == site else I2)
    return result


def _lindblad_rhs(t, rho_vec, H, lindblad_ops_full, gammas):
    """
    Right-hand side of dρ/dt for scipy ODE solver.

    rho_vec is ρ flattened to a vector.
    """
    dim = H.shape[0]
    rho = rho_vec.reshape(dim, dim)

    # Unitary part: -i[H, ρ]
    drho = -1j * (H @ rho - rho @ H)

    # Dissipative part: Σ γ_k (L_k ρ L_k† - ½{L_k† L_k, ρ})
    for L, gamma in zip(lindblad_ops_full, gammas):
        Ld = L.conj().T
        LdL = Ld @ L
        drho += gamma * (L @ rho @ Ld - 0.5 * (LdL @ rho + rho @ LdL))

    return drho.flatten()


def run_lindblad_ed(H_matrix, rho_init, lindblad_ops, gammas, dt, N_steps,
                    measurements=None, progress=True):
    """
    Run exact Lindblad evolution for small systems.

    Parameters
    ----------
    H_matrix : ndarray (2^N, 2^N)
        Hamiltonian matrix.
    rho_init : ndarray (2^N, 2^N)
        Initial density matrix.
    lindblad_ops : list of (name, site, local_op)
        Lindblad operator specifications.
    gammas : list of float
        Dissipation rates (one per Lindblad operator).
    dt : float
        Time step.
    N_steps : int
        Number of steps.
    measurements : dict or None
        {name: callable(rho, t)} measurement functions.
    progress : bool
        Show progress bar.

    Returns
    -------
    dict with 'times', 'observables', 'final_rho'.
    """
    dim = H_matrix.shape[0]
    N = int(np.log2(dim))

    # Build full Lindblad operators
    L_full = []
    gamma_list = []
    for (name, site, local_op), gamma in zip(lindblad_ops, gammas):
        L_full.append(_build_full_operator(local_op, site, N))
        gamma_list.append(gamma)

    results = {'times': [], 'observables': {}}
    if measurements:
        for name in measurements:
            results['observables'][name] = []

    t_span = (0, N_steps * dt)
    t_eval = np.linspace(0, N_steps * dt, N_steps + 1)

    with Timer() as timer:
        sol = solve_ivp(
            _lindblad_rhs,
            t_span,
            rho_init.flatten(),
            t_eval=t_eval,
            args=(H_matrix, L_full, gamma_list),
            method='RK45',
            rtol=1e-8,
            atol=1e-10,
        )

    for i, t in enumerate(sol.t):
        rho = sol.y[:, i].reshape(dim, dim)
        results['times'].append(t)
        if measurements:
            for name, func in measurements.items():
                results['observables'][name].append(func(rho, t))

    results['times'] = np.array(results['times'])
    for name in results['observables']:
        results['observables'][name] = np.array(results['observables'][name])

    results['final_rho'] = sol.y[:, -1].reshape(dim, dim)
    results['wall_time'] = timer.elapsed

    return results


# --- Lindblad measurement functions ---

def measure_purity(rho, t):
    """Purity Tr(ρ²). Pure state = 1, maximally mixed = 1/d."""
    return np.real(np.trace(rho @ rho))


def measure_trace(rho, t):
    """Trace of ρ (should be 1)."""
    return np.real(np.trace(rho))


def measure_vn_entropy_dm(rho, t):
    """Von Neumann entropy S = -Tr(ρ log₂ ρ) from density matrix."""
    eigenvalues = np.linalg.eigvalsh(rho)
    eigenvalues = eigenvalues[eigenvalues > 1e-30]
    return -np.sum(eigenvalues * np.log2(eigenvalues))
