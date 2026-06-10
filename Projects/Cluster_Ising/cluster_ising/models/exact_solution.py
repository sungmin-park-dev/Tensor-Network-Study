"""
Exact analytical solution of the Cluster-Ising Model via Jordan-Wigner transformation.

Reference: PhysRevA.84.022304, Sections III-IV

The CIM Hamiltonian H(λ) = -Σ σ^x_{j-1} σ^z_j σ^x_{j+1} + λ Σ σ^y_j σ^y_{j+1}
is exactly solvable via Jordan-Wigner → Fourier → Bogoliubov transformations,
yielding free fermions with dispersion Λ(p) = √(1 + λ² - 2λ cos(3p)).
"""

import numpy as np
from scipy import integrate
from scipy.linalg import toeplitz, det


# ---------------------------------------------------------------------------
# Dispersion relation
# ---------------------------------------------------------------------------

def dispersion(p, lam):
    """
    Energy dispersion of the CIM.

    Λ(p) = √(1 + λ² - 2λ cos(3p))     [Eq. (9)]

    Parameters
    ----------
    p : float or array
        Momentum (0 ≤ p ≤ π).
    lam : float
        Coupling parameter λ.

    Returns
    -------
    float or array
        Dispersion relation Λ(p).
    """
    return np.sqrt(1.0 + lam**2 - 2.0 * lam * np.cos(3.0 * p))


def dispersion_ising(p, lam):
    """
    Ising-equivalent dispersion (used for free energy equivalence).

    Λ_Ising(p) = √(1 + λ² - 2λ cos(p))    [Eq. (10)-(11)]

    The CIM free energy equals that of an Ising chain with this dispersion.
    """
    return np.sqrt(1.0 + lam**2 - 2.0 * lam * np.cos(p))


# ---------------------------------------------------------------------------
# Ground-state energy
# ---------------------------------------------------------------------------

def ground_state_energy_density(lam, N=None):
    """
    Ground-state energy per site.

    For N → ∞ (thermodynamic limit):
        e₀(λ) = -(1/π) ∫₀^π Λ(p) dp

    For finite N:
        e₀ = -(2/N) Σ_{k=1}^{N} Λ_k   with  Λ_k = Λ(2πk/N)
        (factor 2 from Eq.(6): H = 2 Σ Λ_k (γ†γ - 1/2))

    Parameters
    ----------
    lam : float
        Coupling parameter λ.
    N : int or None
        System size. None = thermodynamic limit.

    Returns
    -------
    float
        Ground-state energy per site.
    """
    if N is None:
        # Thermodynamic limit: integral
        result, _ = integrate.quad(lambda p: dispersion(p, lam), 0, np.pi)
        return -result / np.pi
    else:
        # Finite system: discrete sum
        ks = np.arange(1, N + 1)
        lambdas = dispersion(2.0 * np.pi * ks / N, lam)
        return -np.sum(lambdas) / N


def ground_state_energy_total(lam, N):
    """Total ground-state energy E₀ = N × e₀."""
    return N * ground_state_energy_density(lam, N)


# ---------------------------------------------------------------------------
# Energy spectrum (finite system)
# ---------------------------------------------------------------------------

def single_particle_energies(lam, N):
    """
    Single-particle energies Λ_k for a finite chain of N sites.

    Λ_k = √(1 + λ² - 2λ cos(6πk/N))    [Eq. (6)]

    Parameters
    ----------
    lam : float
        Coupling parameter λ.
    N : int
        System size.

    Returns
    -------
    ndarray of shape (N,)
        Single-particle energies, sorted.
    """
    ks = np.arange(1, N + 1)
    energies = dispersion(2.0 * np.pi * ks / N, lam)
    return np.sort(energies)


def energy_gap(lam, N=None):
    """
    Energy gap Δ = min_p Λ(p).

    At λ=1, the gap closes (Δ=0) at p=0, signaling the QPT.

    Parameters
    ----------
    lam : float
        Coupling parameter λ.
    N : int or None
        System size. None = thermodynamic limit.

    Returns
    -------
    float
        Energy gap.
    """
    if N is None:
        # Gap = |1 - λ| (minimum of Λ(p) at p=0 or p=π/3)
        return np.abs(1.0 - lam)
    else:
        return 2.0 * np.min(single_particle_energies(lam, N))


# ---------------------------------------------------------------------------
# Free energy (finite temperature)
# ---------------------------------------------------------------------------

def free_energy_density(lam, beta):
    """
    Free energy density at inverse temperature β.

    f(β,λ) = -(1/πβ) ∫₀^π ln[2 cosh(β Λ(p))] dp    [Eq. (8)]

    Parameters
    ----------
    lam : float
        Coupling parameter λ.
    beta : float
        Inverse temperature 1/(k_B T). Use np.inf for T=0.

    Returns
    -------
    float
        Free energy per site.
    """
    if np.isinf(beta):
        return ground_state_energy_density(lam)

    def integrand(p):
        return np.log(2.0 * np.cosh(beta * dispersion(p, lam)))

    result, _ = integrate.quad(integrand, 0, np.pi)
    return -result / (np.pi * beta)


# ---------------------------------------------------------------------------
# Correlation function kernel D(r, T)
# ---------------------------------------------------------------------------

def _D_kernel(r, lam, beta=np.inf):
    """
    Correlation kernel D(r, T) from Eq. (25).

    D(r, T) = (1/π) ∫₀^π dp [tanh(β Λ(p)) / Λ(p)]
              × {cos[(r+2)p] - λ cos[(r-1)p]}

    Parameters
    ----------
    r : int
        Relative distance.
    lam : float
        Coupling parameter λ.
    beta : float
        Inverse temperature (default: ∞ = T=0).

    Returns
    -------
    float
        D(r, T).
    """
    def integrand(p):
        lam_p = dispersion(p, lam)
        if np.isinf(beta):
            ratio = 1.0 / lam_p if lam_p > 1e-15 else 0.0
        else:
            ratio = np.tanh(beta * lam_p) / lam_p if lam_p > 1e-15 else 0.0
        return ratio * (np.cos((r + 2) * p) - lam * np.cos((r - 1) * p))

    result, _ = integrate.quad(integrand, 0, np.pi)
    return result / np.pi


def correlation_Rx(r, lam, beta=np.inf):
    """
    Two-point correlation R^x_r = ⟨σ^x_j σ^x_{j+r}⟩.

    Given as a Toeplitz determinant [Eq. (26)]:
    R^x_r = det[D(-1+i-j)]_{i,j=0..r-1}   (with shifted indices)

    Note: R^x_r is nonvanishing only when r is a multiple of 3.

    Parameters
    ----------
    r : int
        Distance (r ≥ 1).
    lam : float
        Coupling parameter λ.
    beta : float
        Inverse temperature.

    Returns
    -------
    float
        Correlation function R^x_r.
    """
    if r == 0:
        return 1.0

    # Build the Toeplitz matrix from Eq. (26)
    # First row: D(-1), D(-2), ..., D(-r)
    # First column: D(-1), D(0), ..., D(r-2)
    col = np.array([_D_kernel(-1 + i, lam, beta) for i in range(r)])
    row = np.array([_D_kernel(-1 - j, lam, beta) for j in range(r)])
    T = toeplitz(col, row)
    return det(T)


def correlation_Ry(r, lam, beta=np.inf):
    """
    Two-point correlation R^y_r = ⟨σ^y_j σ^y_{j+r}⟩.

    Given as a Toeplitz determinant [Eq. (27)]:
    R^y_r = det[D(1+i-j)]_{i,j=0..r-1}

    Parameters
    ----------
    r : int
        Distance (r ≥ 1).
    lam : float
        Coupling parameter λ.
    beta : float
        Inverse temperature.

    Returns
    -------
    float
        Correlation function R^y_r.
    """
    if r == 0:
        return 1.0

    col = np.array([_D_kernel(1 + i, lam, beta) for i in range(r)])
    row = np.array([_D_kernel(1 - j, lam, beta) for j in range(r)])
    T = toeplitz(col, row)
    return det(T)


# ---------------------------------------------------------------------------
# Order parameters (thermodynamic limit)
# ---------------------------------------------------------------------------

def staggered_magnetization(lam):
    """
    Staggered magnetization m_y (exact, thermodynamic limit).

    m_y = { (1 - λ⁻²)^{3/8}  if λ > 1
          { 0                  if λ ≤ 1       [Eq. (45)]

    Parameters
    ----------
    lam : float
        Coupling parameter λ.

    Returns
    -------
    float
        |m_y|
    """
    if lam <= 1.0:
        return 0.0
    return (1.0 - lam**(-2))**(3.0 / 8.0)


def string_order_parameter(lam):
    """
    String order parameter O_z (exact, thermodynamic limit).

    O_z = { (1 - λ²)^{3/4}  if λ < 1
          { 0                if λ ≥ 1       [Eq. (51)]

    Parameters
    ----------
    lam : float
        Coupling parameter λ.

    Returns
    -------
    float
        O_z
    """
    if lam >= 1.0:
        return 0.0
    return (1.0 - lam**2)**(3.0 / 4.0)


def residual_entanglement(lam):
    """
    Residual (multipartite) entanglement τ in the symmetry-breaking ground state.

    τ = { 1                          if λ < 1
        { 1 - (1 - λ⁻²)^{3/4}      if λ > 1    [Eq. (73)]

    Parameters
    ----------
    lam : float
        Coupling parameter λ.

    Returns
    -------
    float
        τ
    """
    if lam <= 1.0:
        return 1.0
    return 1.0 - (1.0 - lam**(-2))**(3.0 / 4.0)


# ---------------------------------------------------------------------------
# Full Hamiltonian matrix (for ED validation)
# ---------------------------------------------------------------------------

def _bit(state, j):
    """Extract bit j from integer state (0 or 1)."""
    return (state >> j) & 1


def _flip(state, j):
    """Flip bit j of integer state."""
    return state ^ (1 << j)


def _sz_val(state, j):
    """σ^z eigenvalue at site j: +1 (spin up, bit=0) or -1 (spin down, bit=1)."""
    return 1 - 2 * _bit(state, j)


def build_hamiltonian_matrix(lam, N, bc='periodic',
                             J_c=1.0, J_xxz=0.0, J_I=0.0,
                             Delta=0.0, hz=0.0):
    """
    Build the full 2^N × 2^N Hamiltonian matrix using bit operations.

    Constructs H directly by computing matrix elements from Pauli algebra,
    avoiding expensive Kronecker products. ~100× faster than the naive approach.

    For the basic CIM (default parameters):
        H = -J_c Σ σ^x_{j-1} σ^z_j σ^x_{j+1} + lam Σ σ^y_j σ^y_{j+1}

    Generalized:
        H = -J_c Σ σ^x σ^z σ^x (cluster)
          + J_xxz Σ (σ^x σ^x + σ^y σ^y + Δ σ^z σ^z) (XXZ)
          + J_I Σ σ^y σ^y (Ising, controlled by lam)
          + hz Σ σ^z (Zeeman)

    Parameters
    ----------
    lam : float
        Coupling λ for the Ising-like σ^y σ^y term.
    N : int
        Number of sites.
    bc : str
        'periodic' (PBC) or 'open' (OBC).
    J_c, J_xxz, J_I, Delta, hz : float
        Coupling constants for the generalized Hamiltonian.

    Returns
    -------
    ndarray (2^N, 2^N)
        Hamiltonian matrix (Hermitian).
    """
    dim = 2**N
    H = np.zeros((dim, dim), dtype=complex)

    def _bond_pairs():
        """Generate nearest-neighbor pairs (j, j+1) respecting BC."""
        for j in range(N - 1):
            yield j, j + 1
        if bc == 'periodic':
            yield N - 1, 0

    def _triplet_sites():
        """Generate triplets (j-1, j, j+1) for the cluster term."""
        for j in range(1, N - 1):
            yield j - 1, j, j + 1
        if bc == 'periodic':
            yield N - 2, N - 1, 0
            yield N - 1, 0, 1

    # Pauli algebra via bit operations:
    # σ^x|b⟩ = |1-b⟩                   (flip bit)
    # σ^y|b⟩ = i(-1)^b |1-b⟩           (flip + phase)
    # σ^z|b⟩ = (-1)^b |b⟩              (diagonal)

    for s in range(dim):
        # --- Diagonal terms ---
        diag = 0.0

        # Zeeman: hz Σ σ^z_j
        if hz != 0:
            for j in range(N):
                diag += hz * _sz_val(s, j)

        # XXZ zz-part: J_xxz Δ Σ σ^z_j σ^z_{j+1}
        if J_xxz != 0 and Delta != 0:
            for j1, j2 in _bond_pairs():
                diag += J_xxz * Delta * _sz_val(s, j1) * _sz_val(s, j2)

        H[s, s] += diag

        # --- Cluster term: -J_c σ^x_{jm1} σ^z_j σ^x_{jp1} ---
        # σ^x_{jm1} σ^z_j σ^x_{jp1} |s⟩ = (-1)^{bit_j(s)} |s ⊕ (1<<jm1) ⊕ (1<<jp1)⟩
        if J_c != 0:
            for jm1, j, jp1 in _triplet_sites():
                s_new = _flip(_flip(s, jm1), jp1)
                val = -J_c * _sz_val(s, j)
                H[s_new, s] += val

        # --- Ising term: λ σ^y_j σ^y_{j+1} ---
        # σ^y_j σ^y_{j+1} |s⟩ = i(-1)^{b_j} × i(-1)^{b_{j+1}} |flip j, flip j+1⟩
        #                      = -(-1)^{b_j + b_{j+1}} |flip j, flip j+1⟩
        if lam != 0:
            for j1, j2 in _bond_pairs():
                s_new = _flip(_flip(s, j1), j2)
                phase = -(-1)**(_bit(s, j1) + _bit(s, j2))
                H[s_new, s] += lam * phase

        # --- XXZ xx-part: J_xxz σ^x_j σ^x_{j+1} ---
        # σ^x_j σ^x_{j+1} |s⟩ = |flip j, flip j+1⟩
        if J_xxz != 0:
            for j1, j2 in _bond_pairs():
                s_new = _flip(_flip(s, j1), j2)
                H[s_new, s] += J_xxz

        # --- XXZ yy-part: J_xxz σ^y_j σ^y_{j+1} ---
        if J_xxz != 0:
            for j1, j2 in _bond_pairs():
                s_new = _flip(_flip(s, j1), j2)
                phase = -(-1)**(_bit(s, j1) + _bit(s, j2))
                H[s_new, s] += J_xxz * phase

        # --- Extra Ising: J_I σ^y_j σ^y_{j+1} ---
        if J_I != 0:
            for j1, j2 in _bond_pairs():
                s_new = _flip(_flip(s, j1), j2)
                phase = -(-1)**(_bit(s, j1) + _bit(s, j2))
                H[s_new, s] += J_I * phase

    return H


# Legacy Kronecker-product implementation (kept for testing)
def _kron_op(op, site, N):
    """Build N-site operator with `op` acting on `site` and identity elsewhere."""
    I2 = np.eye(2, dtype=complex)
    result = np.array([[1.0]], dtype=complex)
    for i in range(N):
        result = np.kron(result, op if i == site else I2)
    return result


def exact_diagonalization(lam, N, bc='periodic', n_states=4, **kwargs):
    """
    Exact diagonalization of the CIM for small N.

    Parameters
    ----------
    lam : float
        Coupling parameter.
    N : int
        Number of sites (keep N ≤ 16 for memory).
    bc : str
        Boundary conditions.
    n_states : int
        Number of lowest eigenvalues to compute.
    **kwargs
        Additional Hamiltonian parameters (J_c, J_xxz, etc.).

    Returns
    -------
    eigenvalues : ndarray
        Lowest n_states eigenvalues.
    eigenvectors : ndarray
        Corresponding eigenvectors (columns).
    """
    from scipy.sparse.linalg import eigsh
    from scipy.sparse import csr_matrix

    H = build_hamiltonian_matrix(lam, N, bc, **kwargs)
    H_sparse = csr_matrix(H)
    n_states = min(n_states, 2**N - 1)
    eigenvalues, eigenvectors = eigsh(H_sparse, k=n_states, which='SA')
    idx = np.argsort(eigenvalues)
    return eigenvalues[idx], eigenvectors[:, idx]


# ---------------------------------------------------------------------------
# Convenience: sweep over λ
# ---------------------------------------------------------------------------

def energy_vs_lambda(lam_range, N=None):
    """
    Compute ground-state energy per site for a range of λ values.

    Parameters
    ----------
    lam_range : array-like
        λ values.
    N : int or None
        System size (None = thermodynamic limit).

    Returns
    -------
    ndarray
        Energy per site for each λ.
    """
    return np.array([ground_state_energy_density(lam, N) for lam in lam_range])


def order_parameters_vs_lambda(lam_range):
    """
    Compute m_y, O_z, τ for a range of λ values (thermodynamic limit).

    Parameters
    ----------
    lam_range : array-like
        λ values.

    Returns
    -------
    dict with keys 'm_y', 'O_z', 'tau', each an ndarray.
    """
    lam_range = np.asarray(lam_range)
    m_y = np.array([staggered_magnetization(l) for l in lam_range])
    O_z = np.array([string_order_parameter(l) for l in lam_range])
    tau = np.array([residual_entanglement(l) for l in lam_range])
    return {'m_y': m_y, 'O_z': O_z, 'tau': tau}
