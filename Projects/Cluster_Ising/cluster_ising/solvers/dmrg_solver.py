"""
DMRG ground-state solver wrapping TeNPy's TwoSiteDMRGEngine.

Returns SolverResult with state_type='mps'.
"""

import numpy as np
from tenpy.algorithms.dmrg import TwoSiteDMRGEngine
from tenpy.networks.mps import MPS

from .base_solver import SolverResult, Timer
from ..models.cluster_ising_model import ClusterIsingModel


DEFAULT_DMRG_PARAMS = {
    'trunc_params': {
        'chi_max': 200,
        'svd_min': 1e-10,
    },
    'mixer': True,
    'mixer_params': {
        'amplitude': 1e-5,
        'decay': 1.5,
        'disable_after': 30,
    },
    'max_sweeps': 50,
    'max_E_err': 1e-10,
    'max_S_err': 1e-6,
}


def run_dmrg(model_params, dmrg_params=None, initial_state=None):
    """
    Run DMRG to find the ground state of the Cluster-Ising Model.

    Parameters
    ----------
    model_params : dict
        Model parameters passed to ClusterIsingModel:
        - L : int
        - lam : float
        - J_c : float (default 1.0)
        - bc_MPS : 'finite' or 'infinite'
        - bc : 'open' or 'periodic'
        - conserve : 'parity' or 'None'
    dmrg_params : dict or None
        DMRG algorithm parameters. None uses DEFAULT_DMRG_PARAMS.
    initial_state : str or list or None
        Initial MPS state:
        - None: random product state
        - 'up'/'down': all up/down
        - list: site-by-site spin configuration

    Returns
    -------
    SolverResult
        With state_type='mps', state=optimized MPS.
    """
    if dmrg_params is None:
        dmrg_params = dict(DEFAULT_DMRG_PARAMS)

    # Ensure required model params have defaults
    params = dict(model_params)
    params.setdefault('bc_MPS', 'finite')
    params.setdefault('conserve', 'parity')

    with Timer() as timer:
        model = ClusterIsingModel(params)
        L = model.lat.N_sites

        # Initialize MPS from product state
        if initial_state is None:
            # Alternate up/down — gives nonzero overlap with both phases
            init = ['up', 'down'] * (L // 2)
            if L % 2:
                init.append('up')
        elif isinstance(initial_state, str):
            init = [initial_state] * L
        else:
            init = initial_state

        psi = MPS.from_product_state(
            model.lat.mps_sites(),
            init,
            bc=model.lat.bc_MPS,
        )

        eng = TwoSiteDMRGEngine(psi, model, dmrg_params)
        E0, psi = eng.run()

    return SolverResult(
        solver_name='DMRG',
        energy=E0,
        energy_per_site=E0 / L,
        state=psi,
        state_type='mps',
        num_sites=L,
        model_params=params,
        metadata={
            'chi_max': dmrg_params['trunc_params']['chi_max'],
            'sweeps': eng.sweeps,
            'wall_time': timer.elapsed,
            'model': model,
            'engine': eng,
            'max_chi': max(psi.chi),
            'sweep_stats': eng.sweep_stats,
        }
    )


def run_dmrg_sweep(lam_values, model_params_base, dmrg_params=None):
    """
    Run DMRG for multiple λ values and collect results.

    Parameters
    ----------
    lam_values : array-like
        λ values to sweep.
    model_params_base : dict
        Base model parameters (L, bc, etc.). 'lam' will be overwritten.
    dmrg_params : dict or None
        DMRG parameters.

    Returns
    -------
    list of SolverResult
    """
    results = []
    for lam in lam_values:
        params = dict(model_params_base)
        params['lam'] = lam
        result = run_dmrg(params, dmrg_params)
        results.append(result)
    return results
