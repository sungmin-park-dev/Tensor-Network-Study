"""
Entanglement measures for the Cluster-Ising Model.

- Block (Von Neumann) entropy S_L
- Entanglement spectrum
- Central charge extraction from S_L scaling

At the critical point (λ=1), the CIM has central charge c = 3/2,
with S_L ~ (c/6) log(L) + const for OBC.
"""

import numpy as np


def block_entropies(state, L, state_type='mps'):
    """
    Compute Von Neumann entanglement entropy for all bipartitions.

    S(l) = -Tr[ρ_l log₂ ρ_l]  for blocks of length l = 1, ..., L-1

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
    ndarray of shape (L-1,)
        Entanglement entropy at each bond.
    """
    if state_type == 'mps':
        return np.array(state.entanglement_entropy())
    elif state_type == 'vector':
        return _block_entropies_ed(state, L)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")


def half_chain_entropy(state, L, state_type='mps'):
    """
    Entanglement entropy at the center bond (l = L/2).
    """
    entropies = block_entropies(state, L, state_type)
    return entropies[L // 2 - 1]


def entanglement_spectrum(state, bond=None, state_type='mps'):
    """
    Entanglement spectrum (Schmidt values) at a given bond.

    Parameters
    ----------
    state : MPS or ndarray
        Quantum state.
    bond : int or None
        Bond index. None = center bond.
    state_type : str
        'mps' or 'vector'.

    Returns
    -------
    ndarray
        Schmidt values (sorted descending).
    """
    if state_type == 'mps':
        L = state.L
        if bond is None:
            bond = L // 2
        return state.get_SL(bond)
    elif state_type == 'vector':
        N = int(np.log2(len(state)))
        if bond is None:
            bond = N // 2
        return _schmidt_values_ed(state, bond, N)
    else:
        raise ValueError(f"Unknown state_type: {state_type}")


def fit_central_charge(L_values, S_values, bc='open'):
    """
    Extract central charge c from entanglement entropy scaling.

    For OBC: S_L ~ (c/6) log₂(L) + const
    For PBC: S_L ~ (c/3) log₂(L) + const  (Calabrese-Cardy)

    Parameters
    ----------
    L_values : array-like
        System sizes.
    S_values : array-like
        Half-chain entanglement entropies.
    bc : str
        'open' or 'periodic'.

    Returns
    -------
    c : float
        Estimated central charge.
    const : float
        Constant offset.
    c_err : float
        Standard error on c.
    """
    L_values = np.asarray(L_values, dtype=float)
    S_values = np.asarray(S_values, dtype=float)

    log_L = np.log2(L_values)

    # Fit S = a * log₂(L) + b
    A = np.vstack([log_L, np.ones_like(log_L)]).T
    result = np.linalg.lstsq(A, S_values, rcond=None)
    a, b = result[0]

    # Residuals for error estimate
    residuals = S_values - (a * log_L + b)
    if len(L_values) > 2:
        mse = np.sum(residuals**2) / (len(L_values) - 2)
        cov = mse * np.linalg.inv(A.T @ A)
        a_err = np.sqrt(cov[0, 0])
    else:
        a_err = 0.0

    # c/6 = a (OBC) or c/3 = a (PBC)
    prefactor = 6.0 if bc == 'open' else 3.0
    c = prefactor * a
    c_err = prefactor * a_err

    return c, b, c_err


# --- Internal helpers ---

def _block_entropies_ed(psi, N):
    """Compute entanglement entropy for all bipartitions from state vector."""
    entropies = np.zeros(N - 1)
    for l in range(1, N):
        sv = _schmidt_values_ed(psi, l, N)
        # Von Neumann entropy: S = -Σ p log₂(p)  where p = sv²
        p = sv**2
        p = p[p > 1e-30]  # avoid log(0)
        entropies[l - 1] = -np.sum(p * np.log2(p))
    return entropies


def _schmidt_values_ed(psi, l, N):
    """
    Compute Schmidt values for bipartition at bond l.

    Splits system into [0..l-1] and [l..N-1].
    """
    dim_A = 2**l
    dim_B = 2**(N - l)
    psi_matrix = psi.reshape(dim_A, dim_B)
    sv = np.linalg.svd(psi_matrix, compute_uv=False)
    return sv / np.linalg.norm(sv)  # normalize


def calabrese_cardy_entropy(l, L, c, const=0.0, bc='open'):
    """
    Calabrese-Cardy prediction for block entropy.

    OBC: S(l) = (c/6) log₂[(2L/π) sin(πl/L)] + const
    PBC: S(l) = (c/3) log₂[(L/π) sin(πl/L)] + const

    Parameters
    ----------
    l : int or array
        Block size(s).
    L : int
        Total system size.
    c : float
        Central charge.
    const : float
        Non-universal constant.
    bc : str
        'open' or 'periodic'.

    Returns
    -------
    float or ndarray
        Predicted entropy.
    """
    l = np.asarray(l, dtype=float)
    L = float(L)

    if bc == 'open':
        prefactor = c / 6.0
        arg = (2.0 * L / np.pi) * np.sin(np.pi * l / L)
    else:
        prefactor = c / 3.0
        arg = (L / np.pi) * np.sin(np.pi * l / L)

    return prefactor * np.log2(np.maximum(arg, 1e-30)) + const
