"""
Pairwise entanglement observables for reproducing the Cluster-Ising paper.

For the exact thermodynamic solution, symmetry forces all one-point functions
and mixed-axis correlators to vanish. The two-spin reduced state is therefore
Bell diagonal and can be reconstructed from R^x_r and R^y_r alone.
"""

import numpy as np

from ..models.exact_solution import correlation_Rx, correlation_Ry


_I2 = np.eye(2, dtype=complex)
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)
_YY = np.kron(_SY, _SY)


def concurrence_from_density_matrix(rho):
    """
    Compute Wootters concurrence for a two-qubit density matrix.

    Parameters
    ----------
    rho : ndarray
        4 x 4 two-qubit density matrix.

    Returns
    -------
    float
        Concurrence in [0, 1].
    """
    rho = np.asarray(rho, dtype=complex).reshape(4, 4)
    rho = 0.5 * (rho + rho.conj().T)

    tr = np.trace(rho)
    if abs(tr) < 1e-15:
        raise ValueError("Density matrix trace is zero.")
    rho = rho / tr

    rho_tilde = _YY @ rho.conj() @ _YY
    eigenvalues = np.linalg.eigvals(rho @ rho_tilde)
    lambdas = np.sqrt(np.maximum(np.real_if_close(eigenvalues), 0.0))
    lambdas = np.sort(np.real(lambdas))[::-1]
    return float(max(0.0, lambdas[0] - lambdas[1] - lambdas[2] - lambdas[3]))


def two_site_reduced_density_matrix(state, L, i, j, state_type="vector"):
    """
    Reduced density matrix for two sites of a pure many-body state.

    Parameters
    ----------
    state : ndarray or MPS
        State vector or TeNPy MPS.
    L : int
        Number of sites.
    i, j : int
        Site indices.
    state_type : str
        "vector" or "mps".

    Returns
    -------
    ndarray
        4 x 4 reduced density matrix.
    """
    if i == j:
        raise ValueError("Two-site reduced density matrix requires i != j.")
    if i > j:
        i, j = j, i

    if state_type == "vector":
        psi = np.asarray(state, dtype=complex).reshape([2] * L)
        perm = [i, j] + [k for k in range(L) if k not in (i, j)]
        psi_perm = np.transpose(psi, axes=perm).reshape(4, -1)
        rho = psi_perm @ psi_perm.conj().T
        return rho / np.trace(rho)

    if state_type == "mps":
        rho = state.get_rho_segment([i, j]).to_ndarray()
        rho = np.asarray(rho, dtype=complex).reshape(4, 4)
        return rho / np.trace(rho)

    raise ValueError(f"Unknown state_type: {state_type}")


def pairwise_concurrence(state, L, i, j, state_type="vector"):
    """
    Pairwise concurrence between sites i and j.

    Parameters
    ----------
    state : ndarray or MPS
        State vector or TeNPy MPS.
    L : int
        Number of sites.
    i, j : int
        Site indices.
    state_type : str
        "vector" or "mps".

    Returns
    -------
    float
        Pairwise concurrence.
    """
    rho = two_site_reduced_density_matrix(state, L, i, j, state_type)
    return concurrence_from_density_matrix(rho)


def concurrence_profile(state, L, state_type="vector", reference_site=None,
                        max_distance=None):
    """
    Pairwise concurrence as a function of distance from a reference site.

    Parameters
    ----------
    state : ndarray or MPS
        State vector or TeNPy MPS.
    L : int
        Number of sites.
    state_type : str
        "vector" or "mps".
    reference_site : int or None
        Starting site. Defaults to the middle bond.
    max_distance : int or None
        Maximum separation. Defaults to all sites to the right.

    Returns
    -------
    distances : ndarray
        Separations 1, 2, ...
    concurrences : ndarray
        Pairwise concurrence at each separation.
    """
    if reference_site is None:
        reference_site = max(0, L // 2 - 1)
    if max_distance is None:
        max_distance = L - 1 - reference_site
    max_distance = min(max_distance, L - 1 - reference_site)

    distances = np.arange(1, max_distance + 1)
    values = np.array([
        pairwise_concurrence(
            state, L, reference_site, reference_site + distance, state_type
        )
        for distance in distances
    ])
    return distances, values


def exact_two_spin_density_matrix(r, lam, beta=np.inf):
    """
    Exact thermodynamic two-spin density matrix at distance r.

    The reduced state is Bell diagonal:
        rho = 1/4 [I + R^x_r XX + R^y_r YY]
    because z magnetization and mixed-axis correlators vanish by symmetry.

    Parameters
    ----------
    r : int
        Spin separation.
    lam : float
        Cluster-Ising coupling.
    beta : float
        Inverse temperature. Use np.inf for the ground-state limit.

    Returns
    -------
    ndarray
        4 x 4 exact reduced density matrix.
    """
    rx = correlation_Rx(r, lam, beta)
    ry = correlation_Ry(r, lam, beta)
    rho = 0.25 * (
        np.kron(_I2, _I2) +
        rx * np.kron(_SX, _SX) +
        ry * np.kron(_SY, _SY)
    )
    return 0.5 * (rho + rho.conj().T)


def exact_pairwise_concurrence(r, lam, beta=np.inf):
    """
    Exact thermodynamic pairwise concurrence at distance r.

    Parameters
    ----------
    r : int
        Spin separation.
    lam : float
        Cluster-Ising coupling.
    beta : float
        Inverse temperature.

    Returns
    -------
    float
        Pairwise concurrence.
    """
    rho = exact_two_spin_density_matrix(r, lam, beta)
    return concurrence_from_density_matrix(rho)


def exact_pairwise_concurrence_profile(lam, r_values, beta=np.inf):
    """
    Exact thermodynamic concurrence evaluated on several distances.

    Parameters
    ----------
    lam : float
        Cluster-Ising coupling.
    r_values : array-like
        Distances to evaluate.
    beta : float
        Inverse temperature.

    Returns
    -------
    ndarray
        Pairwise concurrence for each distance.
    """
    r_values = np.asarray(r_values, dtype=int)
    return np.array([
        exact_pairwise_concurrence(int(r), lam, beta) for r in r_values
    ])
