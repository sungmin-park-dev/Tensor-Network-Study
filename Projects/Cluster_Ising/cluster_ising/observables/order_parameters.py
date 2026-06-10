"""
Order parameters for the Cluster-Ising Model.

- Staggered magnetization m_y: detects Ising phase (λ > 1)
- String order parameter O_z: detects cluster phase (λ < 1)
- Residual multipartite entanglement τ

Supports both MPS (DMRG) and state vector (ED) representations.

Note on parity conservation:
    With conserve='parity', the MPS ground state is a Z₂ eigenstate.
    Since σ^y is parity-odd, ⟨σ^y_j⟩ = 0 identically.
    We therefore compute m_y from the σ^y−σ^y correlation function:
        m_y² = (1/L²) Σ_{i,j} (-1)^{i+j} ⟨σ^y_i σ^y_j⟩
    The string order parameter uses the paper's Eq.(47) with odd string length
    to preserve parity symmetry.
"""

import numpy as np


# Pauli matrices for ED computations
_SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
_SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def staggered_magnetization_y(state, L, state_type='mps'):
    """
    Staggered magnetization along y.

    Computed from the two-point correlator:
        m_y² = (1/L²) Σ_{i,j} (-1)^{i+j} ⟨σ^y_i σ^y_j⟩

    This works correctly with parity conservation.

    In the thermodynamic limit:
        m_y = 0 for λ ≤ 1 (cluster phase)
        m_y = (1 - λ⁻²)^{3/8} for λ > 1 (Ising phase)

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
    float
        |m_y|
    """
    if state_type == 'mps':
        corr = state.correlation_function('Sigmay', 'Sigmay')
    elif state_type == 'vector':
        corr = _two_point_correlation_matrix_ed(state, _SIGMA_Y, L)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")

    # m_y² = (1/L²) Σ_{i,j} (-1)^{i+j} C(i,j)
    signs = np.array([(-1)**j for j in range(L)])
    sign_matrix = np.outer(signs, signs)
    m_y_sq = np.sum(sign_matrix * np.real(corr)) / L**2
    return np.sqrt(max(0.0, m_y_sq))


def string_order_z(state, L, state_type='mps', i=None, j=None):
    """
    String order parameter O_z for the cluster (SPT) phase.

    Uses the paper's definition [Eq. (47)]:
        Ω_z(r) = ⟨σ^x_i σ^y_{i+1} (∏_{k=i+2}^{j-2} σ^z_k) σ^y_{j-1} σ^x_j⟩

    where r = j - i must be odd (≥ 5) to be parity-even under Z₂.

    O_z² = lim_{r→∞} |Ω_z(r)|, so O_z = √|Ω_z(r_max)|.

    In the thermodynamic limit:
        O_z = (1 - λ²)^{3/4} for λ < 1 (cluster phase)
        O_z = 0 for λ ≥ 1

    Parameters
    ----------
    state : MPS or ndarray
        Quantum state.
    L : int
        Number of sites.
    state_type : str
        'mps' or 'vector'.
    i, j : int or None
        Endpoints. None = auto-select to maximise string length.
        If specified, j - i must be odd and ≥ 5.

    Returns
    -------
    float
        String order parameter |O_z|.
    """
    if i is None or j is None:
        # Auto-select: use central region, odd r, as long as possible
        margin = max(L // 8, 2)
        i = margin
        r_max = L - 2 * margin
        # Ensure r is odd and >= 5
        if r_max % 2 == 0:
            r_max -= 1
        r_max = max(r_max, 5)
        j = i + r_max
        if j >= L:
            j = L - margin
            r = j - i
            if r % 2 == 0:
                j -= 1
            if j - i < 5:
                # System too small
                return 0.0

    r = j - i
    if r < 5:
        return 0.0

    if state_type == 'mps':
        val = _omega_z_mps(state, i, j)
    elif state_type == 'vector':
        val = _omega_z_ed(state, i, j, L)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")

    # O_z = sqrt(|Omega_z|)
    return np.sqrt(max(0.0, abs(val)))


def residual_entanglement_tau(state, L, state_type='mps'):
    """
    Residual multipartite entanglement τ.

    For the symmetric (parity-conserving) ground state, τ is computed
    from the correlation-based m_y via the relation τ = 1 - m_y²,
    which is valid in the thermodynamic limit.

    τ = 1 for λ ≤ 1 (cluster phase, maximally entangled)
    τ = 1 - (1 - λ⁻²)^{3/4} for λ > 1 (Ising phase)

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
    float
        τ value (0 ≤ τ ≤ 1).
    """
    m_y = staggered_magnetization_y(state, L, state_type)
    return 1.0 - m_y**2


# ---------------------------------------------------------------------------
# String order helpers
# ---------------------------------------------------------------------------

def _omega_z_mps(psi, i, j):
    """
    Compute Ω_z(i,j) via MPS [Eq. (47)].

    Ω_z = ⟨σ^x_i σ^y_{i+1} (∏_{k=i+2}^{j-2} σ^z_k) σ^y_{j-1} σ^x_j⟩
    """
    ops = [('Sigmax', i), ('Sigmay', i + 1)]
    for k in range(i + 2, j - 1):
        ops.append(('Sigmaz', k))
    ops.append(('Sigmay', j - 1))
    ops.append(('Sigmax', j))
    return np.real(psi.expectation_value_term(ops))


def _omega_z_ed(psi, i, j, N):
    """Compute Ω_z(i,j) from full state vector."""
    I2 = np.eye(2, dtype=complex)
    full_op = np.array([[1.0]], dtype=complex)
    for k in range(N):
        if k == i or k == j:
            full_op = np.kron(full_op, _SIGMA_X)
        elif k == i + 1 or k == j - 1:
            full_op = np.kron(full_op, _SIGMA_Y)
        elif i + 1 < k < j - 1:
            full_op = np.kron(full_op, _SIGMA_Z)
        else:
            full_op = np.kron(full_op, I2)
    return np.real(psi.conj() @ full_op @ psi)


# ---------------------------------------------------------------------------
# ED helpers
# ---------------------------------------------------------------------------

def _two_point_correlation_matrix_ed(psi, op, N):
    """
    Compute full correlation matrix C(i,j) = ⟨ψ|op_i op_j|ψ⟩.

    Uses reshape trick: apply op on site j by reshaping psi to (2^j, 2, 2^{N-j-1}),
    then contracting with the 2×2 operator. O(N² × 2^N) instead of O(N² × 4^N).
    """
    dim = 2**N
    corr = np.zeros((N, N))

    # Precompute op|ψ⟩ for each site j
    op_psi = np.zeros((N, dim), dtype=complex)
    for j in range(N):
        # Reshape: (2^j, 2, 2^{N-j-1})
        psi_r = psi.reshape(2**j, 2, 2**(N - j - 1))
        # Apply op on the middle axis
        result = np.einsum('ab,ibe->iae', op, psi_r)
        op_psi[j] = result.reshape(dim)

    for i in range(N):
        corr[i, i] = 1.0  # ⟨op²⟩ = 1 for Pauli matrices
        for j in range(i + 1, N):
            # ⟨ψ| op_i op_j |ψ⟩ = (op_i|ψ⟩)† (op_j|ψ⟩) when ops commute on different sites
            # Actually: ⟨ψ| op_i op_j |ψ⟩ = ⟨op_i ψ | op_j ψ⟩ since op is Hermitian
            # But op_i and op_j act on different sites, so op_i op_j |ψ⟩ can be computed as
            # applying op_j to op_i|ψ⟩.
            v = op_psi[i]
            v_r = v.reshape(2**j, 2, 2**(N - j - 1))
            v_out = np.einsum('ab,ibe->iae', op, v_r).reshape(dim)
            val = np.real(psi.conj() @ v_out)
            corr[i, j] = val
            corr[j, i] = val

    return corr


def _local_expectations_ed(psi, op, N):
    """Compute ⟨ψ|op_j|ψ⟩ for all sites j."""
    I2 = np.eye(2, dtype=complex)
    vals = np.zeros(N)
    for j in range(N):
        full_op = np.array([[1.0]], dtype=complex)
        for k in range(N):
            full_op = np.kron(full_op, op if k == j else I2)
        vals[j] = np.real(psi.conj() @ full_op @ psi)
    return vals


def _single_site_rdm_ed(psi, site, N):
    """
    Compute reduced density matrix for a single site from state vector.

    ρ_site = Tr_{rest}(|ψ⟩⟨ψ|)
    """
    psi_reshaped = psi.reshape([2] * N)
    psi_r = np.moveaxis(psi_reshaped, site, 0)
    psi_r = psi_r.reshape(2, -1)
    rho = psi_r @ psi_r.conj().T
    return rho
