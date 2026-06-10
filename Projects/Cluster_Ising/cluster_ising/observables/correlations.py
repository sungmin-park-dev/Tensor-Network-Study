"""
Spin-spin correlation functions for the Cluster-Ising Model.

R^α_r(T) = ⟨σ^α_j σ^α_{j+r}⟩    α = x, y, z

Key properties from the exact solution:
- R^z_r = 0 identically (z magnetization vanishes)
- R^x_r ≠ 0 only when r is a multiple of 3
- R^y_r is always nonvanishing

Supports both MPS and state vector representations.
"""

import numpy as np

_SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
_SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def correlation_function(state, L, op_name, r_max=None, state_type='mps',
                         site_ref=None):
    """
    Compute two-point correlation function ⟨O_j O_{j+r}⟩ for r = 1..r_max.

    Parameters
    ----------
    state : MPS or ndarray
        Quantum state.
    L : int
        Number of sites.
    op_name : str
        Operator name: 'Sigmax', 'Sigmay', or 'Sigmaz'.
    r_max : int or None
        Maximum distance. None = L//2.
    state_type : str
        'mps' or 'vector'.
    site_ref : int or None
        Reference site j. None = L//2 (center).

    Returns
    -------
    distances : ndarray
        Distance values [1, 2, ..., r_max].
    correlations : ndarray
        Correlation values R^α_r.
    """
    if r_max is None:
        r_max = L // 2
    if site_ref is None:
        site_ref = L // 4  # offset from center to allow room

    distances = np.arange(1, r_max + 1)

    if state_type == 'mps':
        corr = _correlation_mps(state, op_name, site_ref, r_max)
    elif state_type == 'vector':
        op_matrix = _name_to_matrix(op_name)
        corr = _correlation_ed(state, op_matrix, site_ref, r_max, L)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")

    return distances, corr


def correlation_Rx(state, L, r_max=None, state_type='mps', **kwargs):
    """R^x_r = ⟨σ^x_j σ^x_{j+r}⟩."""
    return correlation_function(state, L, 'Sigmax', r_max, state_type, **kwargs)


def correlation_Ry(state, L, r_max=None, state_type='mps', **kwargs):
    """R^y_r = ⟨σ^y_j σ^y_{j+r}⟩."""
    return correlation_function(state, L, 'Sigmay', r_max, state_type, **kwargs)


def correlation_Rz(state, L, r_max=None, state_type='mps', **kwargs):
    """R^z_r = ⟨σ^z_j σ^z_{j+r}⟩. Should be identically zero."""
    return correlation_function(state, L, 'Sigmaz', r_max, state_type, **kwargs)


def connected_correlation(state, L, op_name, r_max=None, state_type='mps'):
    """
    Connected correlation: ⟨O_j O_{j+r}⟩ - ⟨O_j⟩⟨O_{j+r}⟩.
    """
    distances, corr = correlation_function(state, L, op_name, r_max, state_type)

    if state_type == 'mps':
        exp_vals = state.expectation_value(op_name)
    else:
        op_matrix = _name_to_matrix(op_name)
        exp_vals = _local_expectations_ed(state, op_matrix, L)

    site_ref = L // 4
    for idx, r in enumerate(distances):
        j2 = site_ref + r
        if j2 < L:
            corr[idx] -= np.real(exp_vals[site_ref] * exp_vals[j2])

    return distances, corr


def correlation_length(distances, correlations):
    """
    Extract correlation length ξ by fitting |C(r)| ~ exp(-r/ξ).

    Parameters
    ----------
    distances : ndarray
        Distance values.
    correlations : ndarray
        Correlation values.

    Returns
    -------
    xi : float
        Correlation length. Returns np.inf if fit fails.
    """
    abs_corr = np.abs(correlations)
    mask = abs_corr > 1e-15
    if np.sum(mask) < 3:
        return np.inf

    log_corr = np.log(abs_corr[mask])
    r_vals = distances[mask]

    # Linear fit: log|C(r)| = -r/ξ + const
    coeffs = np.polyfit(r_vals, log_corr, 1)
    if coeffs[0] >= 0:
        return np.inf
    return -1.0 / coeffs[0]


# --- Internal helpers ---

def _name_to_matrix(op_name):
    """Convert operator name to Pauli matrix."""
    mapping = {
        'Sigmax': _SIGMA_X,
        'Sigmay': _SIGMA_Y,
        'Sigmaz': _SIGMA_Z,
    }
    return mapping[op_name]


def _correlation_mps(psi, op_name, site_ref, r_max):
    """Compute correlations from MPS."""
    L = psi.L
    corr_matrix = psi.correlation_function(op_name, op_name)
    # Extract row for site_ref
    corr = np.zeros(r_max)
    for r in range(r_max):
        j2 = site_ref + r + 1
        if j2 < L:
            corr[r] = np.real(corr_matrix[site_ref, j2])
    return corr


def _correlation_ed(psi, op, site_ref, r_max, N):
    """
    Compute correlations from state vector using fast reshape trick.

    Instead of building the full 2^N × 2^N operator via Kronecker products,
    apply the single-site operator using reshaping: O(N × 2^N) vs O(4^N).
    """
    dim = 2**N
    corr = np.zeros(r_max)

    # Apply op on site_ref: op_ref|ψ⟩
    psi_r = psi.reshape(2**site_ref, 2, 2**(N - site_ref - 1))
    op_ref_psi = np.einsum('ab,ibe->iae', op, psi_r).reshape(dim)

    for r in range(r_max):
        j2 = site_ref + r + 1
        if j2 >= N:
            break
        # Apply op on site j2 to op_ref|ψ⟩: ⟨ψ| op_ref op_j2 |ψ⟩
        v_r = op_ref_psi.reshape(2**j2, 2, 2**(N - j2 - 1))
        v_out = np.einsum('ab,ibe->iae', op, v_r).reshape(dim)
        corr[r] = np.real(psi.conj() @ v_out)

    return corr


def _local_expectations_ed(psi, op, N):
    """Compute ⟨ψ|op_j|ψ⟩ for all sites j using fast reshape trick."""
    dim = 2**N
    vals = np.zeros(N)
    for j in range(N):
        psi_r = psi.reshape(2**j, 2, 2**(N - j - 1))
        op_psi = np.einsum('ab,ibe->iae', op, psi_r).reshape(dim)
        vals[j] = np.real(psi.conj() @ op_psi)
    return vals
