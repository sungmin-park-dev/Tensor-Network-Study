"""
Exact Diagonalization solver for the Cluster-Ising Model.

Builds the full 2^N Hamiltonian and diagonalizes with scipy.
Suitable for small systems (N ≤ 16).
"""

import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

from .base_solver import SolverResult, Timer
from ..models.exact_solution import build_hamiltonian_matrix


def run_ed(model_params, n_states=4):
    """
    Run exact diagonalization.

    Parameters
    ----------
    model_params : dict
        Must contain:
        - 'L' : int, number of sites
        - 'lam' : float, coupling λ
        Optional:
        - 'bc' : str, 'periodic' or 'open' (default 'periodic')
        - 'J_c', 'J_xxz', 'J_I', 'Delta', 'hz' : float
    n_states : int
        Number of lowest eigenstates to compute.

    Returns
    -------
    SolverResult
        With state_type='vector', state=ground state eigenvector.
    """
    N = model_params['L']
    lam = model_params.get('lam', 1.0)
    bc = model_params.get('bc', 'periodic')

    ham_kwargs = {}
    for key in ('J_c', 'J_xxz', 'J_I', 'Delta', 'hz'):
        if key in model_params:
            ham_kwargs[key] = model_params[key]

    with Timer() as timer:
        H = build_hamiltonian_matrix(lam, N, bc, **ham_kwargs)
        H_sparse = csr_matrix(H)
        n_states = min(n_states, 2**N - 1)
        eigenvalues, eigenvectors = eigsh(H_sparse, k=n_states, which='SA')

    idx = np.argsort(eigenvalues)
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]

    E0 = eigenvalues[0]
    psi0 = eigenvectors[:, 0]

    return SolverResult(
        solver_name='ED',
        energy=E0,
        energy_per_site=E0 / N,
        state=psi0,
        state_type='vector',
        num_sites=N,
        model_params=dict(model_params),
        metadata={
            'eigenvalues': eigenvalues,
            'eigenvectors': eigenvectors,
            'n_states': n_states,
            'wall_time': timer.elapsed,
            'hilbert_dim': 2**N,
        }
    )


def measure_local_op_ed(psi, op_matrix, site, N):
    """
    Measure ⟨ψ|O_site|ψ⟩ for a local operator on a given site.

    Parameters
    ----------
    psi : ndarray (2^N,)
        State vector.
    op_matrix : ndarray (2, 2)
        Local operator matrix.
    site : int
        Site index (0-based).
    N : int
        Number of sites.

    Returns
    -------
    float
        Expectation value (real part).
    """
    I2 = np.eye(2, dtype=complex)
    full_op = np.array([[1.0]], dtype=complex)
    for i in range(N):
        full_op = np.kron(full_op, op_matrix if i == site else I2)
    return np.real(psi.conj() @ full_op @ psi)


def measure_two_site_op_ed(psi, op1, site1, op2, site2, N):
    """
    Measure ⟨ψ|O1_{site1} O2_{site2}|ψ⟩.

    Parameters
    ----------
    psi : ndarray (2^N,)
        State vector.
    op1, op2 : ndarray (2, 2)
        Local operators.
    site1, site2 : int
        Site indices.
    N : int
        Number of sites.

    Returns
    -------
    float
        Expectation value (real part).
    """
    I2 = np.eye(2, dtype=complex)
    full_op = np.array([[1.0]], dtype=complex)
    for i in range(N):
        if i == site1:
            full_op = np.kron(full_op, op1)
        elif i == site2:
            full_op = np.kron(full_op, op2)
        else:
            full_op = np.kron(full_op, I2)
    return np.real(psi.conj() @ full_op @ psi)
