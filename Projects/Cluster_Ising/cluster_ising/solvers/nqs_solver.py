"""
Neural Quantum States solver using NetKet VMC.

Uses NetKet >= 3.0 with JAX backend for variational Monte Carlo
optimization of the Cluster-Ising Model ground state.

Ansatz options:
- RBM (Restricted Boltzmann Machine) via nk.models.RBM
- RBMSymm (translation-invariant RBM)

Returns SolverResult with state_type='nqs'.
"""

import numpy as np
import warnings
from .base_solver import SolverResult, Timer

try:
    import netket as nk
    import jax
    HAS_NETKET = True
except ImportError:
    HAS_NETKET = False


# Pauli matrices (eigenvalues ±1)
_SX = np.array([[0, 1], [1, 0]], dtype=complex)
_SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
_SZ = np.array([[1, 0], [0, -1]], dtype=complex)

# Pre-computed multi-site operators
_XZX = np.kron(np.kron(_SX, _SZ), _SX)  # 8×8: cluster term
_YY = np.kron(_SY, _SY)                  # 4×4: Ising term


DEFAULT_NQS_PARAMS = {
    'ansatz': 'RBM',           # 'RBM' or 'RBMSymm'
    'alpha': 2,                # hidden unit density (n_hidden = alpha * L)
    'n_samples': 2048,         # MC samples per iteration
    'n_iter': 500,             # VMC optimization iterations
    'learning_rate': 0.02,     # SGD learning rate (with SR)
    'diag_shift': 0.01,        # SR diagonal regularization
    'seed': None,              # RNG seed (None = random)
    'n_discard_per_chain': 16, # MC thermalization steps
    'use_sr': True,            # Use Stochastic Reconfiguration
}


def build_netket_hamiltonian(model_params):
    """
    Build the CIM Hamiltonian as a NetKet LocalOperator.

    H(λ) = -J_c Σ_j σ^x_{j-1} σ^z_j σ^x_{j+1} + λ Σ_j σ^y_j σ^y_{j+1}

    Parameters
    ----------
    model_params : dict
        Must contain 'L' and 'lam'.
        Optional: 'bc' ('periodic'|'open', default 'periodic'),
                  'J_c' (default 1.0).

    Returns
    -------
    hi : nk.hilbert.Spin
        Hilbert space.
    H : nk.operator.LocalOperator
        Hamiltonian operator.
    graph : nk.graph.Chain
        Lattice graph (for symmetric ansatz).
    """
    if not HAS_NETKET:
        raise ImportError(
            "NetKet is required for the NQS solver. "
            "Install with: pip install 'cluster-ising[nqs]' "
            "or: pip install netket"
        )

    L = model_params['L']
    lam = model_params.get('lam', 1.0)
    bc = model_params.get('bc', 'periodic')
    J_c = model_params.get('J_c', 1.0)

    if L < 3:
        raise ValueError(f"L must be >= 3 for the cluster term, got L={L}")

    pbc = (bc == 'periodic')
    hi = nk.hilbert.Spin(s=1 / 2, N=L)
    graph = nk.graph.Chain(length=L, pbc=pbc)

    H = nk.operator.LocalOperator(hi, dtype=complex)

    # --- Cluster term: -J_c Σ σ^x_{j-1} σ^z_j σ^x_{j+1} ---
    if pbc:
        triplets = [(j, (j + 1) % L, (j + 2) % L) for j in range(L)]
    else:
        triplets = [(j, j + 1, j + 2) for j in range(L - 2)]

    for jm1, j, jp1 in triplets:
        H += nk.operator.LocalOperator(
            hi, -J_c * _XZX, [jm1, j, jp1]
        )

    # --- Ising term: λ Σ σ^y_j σ^y_{j+1} ---
    if pbc:
        bonds = [(j, (j + 1) % L) for j in range(L)]
    else:
        bonds = [(j, j + 1) for j in range(L - 1)]

    for j1, j2 in bonds:
        H += nk.operator.LocalOperator(
            hi, lam * _YY, [j1, j2]
        )

    return hi, H, graph


def run_nqs(model_params, nqs_params=None):
    """
    Run NQS variational optimization using NetKet VMC.

    Parameters
    ----------
    model_params : dict
        Must contain:
        - 'L' : int, number of sites
        - 'lam' : float, coupling λ
        Optional:
        - 'bc' : str, 'periodic' or 'open' (default 'periodic')
        - 'J_c' : float, cluster coupling (default 1.0)
    nqs_params : dict or None
        NQS-specific parameters (merged with DEFAULT_NQS_PARAMS):
        - ansatz : str, 'RBM' or 'RBMSymm'
        - alpha : int, hidden unit density
        - n_samples : int, MC samples per step
        - n_iter : int, optimization iterations
        - learning_rate : float, SGD learning rate
        - diag_shift : float, SR regularization
        - seed : int or None, random seed
        - n_discard_per_chain : int, MC thermalization
        - use_sr : bool, use Stochastic Reconfiguration

    Returns
    -------
    SolverResult
        With state_type='nqs', state=variational_state.
    """
    if not HAS_NETKET:
        raise ImportError(
            "NetKet is required for the NQS solver. "
            "Install with: pip install 'cluster-ising[nqs]' "
            "or: pip install netket"
        )

    # Merge parameters
    params = {**DEFAULT_NQS_PARAMS, **(nqs_params or {})}
    L = model_params['L']
    ansatz = params['ansatz']
    alpha = params['alpha']
    n_samples = params['n_samples']
    n_iter = params['n_iter']
    learning_rate = params['learning_rate']
    diag_shift = params['diag_shift']
    seed = params['seed']
    n_discard = params['n_discard_per_chain']
    use_sr = params['use_sr']

    # Build Hamiltonian
    hi, H, graph = build_netket_hamiltonian(model_params)

    # Sampler: single-spin flip Metropolis
    sampler = nk.sampler.MetropolisLocal(hilbert=hi, n_chains=16)

    # Ansatz (param_dtype=complex for σ^y σ^y Hamiltonian)
    if ansatz == 'RBM':
        model = nk.models.RBM(
            alpha=alpha,
            use_visible_bias=True,
            use_hidden_bias=True,
            param_dtype=complex,
        )
    elif ansatz == 'RBMSymm':
        model = nk.models.RBMSymm(
            symmetries=graph.translation_group(),
            alpha=alpha,
            param_dtype=complex,
        )
    else:
        raise ValueError(f"Unknown ansatz: {ansatz}. Use 'RBM' or 'RBMSymm'.")

    # Variational state
    vs = nk.vqs.MCState(
        sampler=sampler,
        model=model,
        n_samples=n_samples,
        n_discard_per_chain=n_discard,
        seed=seed,
    )

    # Optimizer: use SGD + SR when possible, fallback to Adam without SR
    if use_sr:
        try:
            optimizer = nk.optimizer.Sgd(learning_rate=learning_rate)
            # Explicit cholesky solver avoids plum-dispatch AmbiguousLookupError
            # that occurs with the default solver in NetKet 3.x + plum-dispatch 2.x
            preconditioner = nk.optimizer.SR(
                diag_shift=diag_shift,
                holomorphic=True,
                solver=nk.optimizer.solver.cholesky,
            )
        except Exception:
            # Fallback if SR has compatibility issues
            warnings.warn(
                "SR preconditioner unavailable, falling back to Adam optimizer.",
                RuntimeWarning,
            )
            optimizer = nk.optimizer.Adam(learning_rate=learning_rate)
            preconditioner = None
    else:
        optimizer = nk.optimizer.Sgd(learning_rate=learning_rate)
        preconditioner = None

    # VMC driver
    gs = nk.driver.VMC(
        hamiltonian=H,
        optimizer=optimizer,
        variational_state=vs,
        preconditioner=preconditioner,
    )

    # Run optimization (with fallback if SR fails at runtime)
    with Timer() as timer:
        log = nk.logging.RuntimeLog()
        try:
            gs.run(n_iter=n_iter, out=log)
        except Exception as e:
            if preconditioner is not None:
                warnings.warn(
                    f"SR failed at runtime ({e}), retrying with Adam optimizer.",
                    RuntimeWarning,
                )
                optimizer = nk.optimizer.Adam(learning_rate=learning_rate)
                gs = nk.driver.VMC(
                    hamiltonian=H,
                    optimizer=optimizer,
                    variational_state=vs,
                    preconditioner=None,
                )
                log = nk.logging.RuntimeLog()
                gs.run(n_iter=n_iter, out=log)
            else:
                raise

    # Extract energy from log
    # NetKet >= 3.12: log.data['Energy']['Mean'] is a numpy array directly
    energy_data = log.data['Energy']
    E_history = np.real(np.array(energy_data['Mean']))
    var_history = np.real(np.array(energy_data['Variance']))

    # Final energy: average over last 10% of iterations
    tail = max(1, n_iter // 10)
    E_mean = float(np.mean(E_history[-tail:]))
    E_var = float(np.mean(var_history[-tail:]))

    # Convergence check
    converged = True
    if E_var > 0.1 * abs(E_mean) and abs(E_mean) > 1e-6:
        warnings.warn(
            f"NQS may not have converged: E={E_mean:.6f}, "
            f"Var={E_var:.4f} ({E_var/abs(E_mean)*100:.1f}% of |E|). "
            f"Consider increasing n_iter or n_samples.",
            RuntimeWarning,
        )
        converged = False

    return SolverResult(
        solver_name='NQS',
        energy=E_mean,
        energy_per_site=E_mean / L,
        state=vs,
        state_type='nqs',
        num_sites=L,
        model_params=dict(model_params),
        metadata={
            'ansatz': ansatz,
            'alpha': alpha,
            'n_samples': n_samples,
            'n_iter': n_iter,
            'learning_rate': learning_rate,
            'diag_shift': diag_shift,
            'energy_variance': E_var,
            'energy_history': E_history.tolist(),
            'variance_history': var_history.tolist(),
            'wall_time': timer.elapsed,
            'converged': converged,
            'nqs_params': params,
        },
    )


def run_nqs_sweep(lam_values, model_params_base, nqs_params=None):
    """
    Run NQS for multiple λ values and collect results.

    Parameters
    ----------
    lam_values : array-like
        λ values to sweep.
    model_params_base : dict
        Base model parameters (L, bc, etc.). 'lam' will be overwritten.
    nqs_params : dict or None
        NQS parameters.

    Returns
    -------
    list of SolverResult
    """
    results = []
    for lam in lam_values:
        params = dict(model_params_base)
        params['lam'] = lam
        result = run_nqs(params, nqs_params)
        results.append(result)
    return results
