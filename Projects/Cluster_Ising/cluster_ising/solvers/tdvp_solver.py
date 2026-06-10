"""
TDVP time evolution solver for the Cluster-Ising Model.

Uses TeNPy's TwoSiteTDVPEngine for real-time evolution.
TEBD is NOT usable due to the 3-body cluster term.

Supports time-dependent Hamiltonian h(t) via model rebuilding.
"""

import numpy as np
from tqdm import tqdm

from .base_solver import Timer


DEFAULT_TDVP_PARAMS = {
    'N_steps': 200,
    'dt': 0.05,
    'trunc_params': {
        'chi_max': 100,
        'svd_min': 1e-10,
    },
}


def run_tdvp(initial_psi, model, tdvp_params=None, measurements=None,
             h_func=None, model_class=None, model_params_base=None,
             progress=True):
    """
    Run TDVP time evolution.

    Parameters
    ----------
    initial_psi : MPS
        Initial state (will be modified in-place).
    model : CouplingMPOModel
        Hamiltonian model (used if h_func is None).
    tdvp_params : dict or None
        TDVP parameters. None uses DEFAULT_TDVP_PARAMS.
    measurements : dict or None
        {name: callable(psi, t)} measurement functions.
        Called at each time step.
    h_func : callable or None
        Time-dependent field h(t). If provided, the model is rebuilt
        at each time step with updated hz parameter.
    model_class : class or None
        Model class to instantiate (needed with h_func).
    model_params_base : dict or None
        Base model parameters (needed with h_func).
    progress : bool
        Show progress bar.

    Returns
    -------
    dict
        'times': array of time values
        'observables': {name: list of measured values}
        'final_psi': final MPS state
    """
    from tenpy.algorithms.tdvp import TwoSiteTDVPEngine

    if tdvp_params is None:
        tdvp_params = dict(DEFAULT_TDVP_PARAMS)

    N_steps = tdvp_params.pop('N_steps', 200)
    dt = tdvp_params.get('dt', 0.05)

    results = {
        'times': [],
        'observables': {},
    }

    if measurements:
        for name in measurements:
            results['observables'][name] = []

    psi = initial_psi

    with Timer() as timer:
        iterator = range(N_steps)
        if progress:
            iterator = tqdm(iterator, desc='TDVP', unit='step')

        for step in iterator:
            t = step * dt

            # Update model for time-dependent h(t)
            if h_func is not None and model_class is not None:
                params = dict(model_params_base)
                params['hz'] = h_func(t)
                model = model_class(params)

            # Create engine for this step
            if step == 0:
                eng = TwoSiteTDVPEngine(psi, model, tdvp_params)
            else:
                eng.init_env(model)

            eng.run_evolution(1, dt)

            # Measure observables
            if measurements:
                results['times'].append(t + dt)
                for name, func in measurements.items():
                    results['observables'][name].append(func(psi, t + dt))

    results['times'] = np.array(results['times'])
    for name in results['observables']:
        results['observables'][name] = np.array(results['observables'][name])

    results['final_psi'] = psi
    results['wall_time'] = timer.elapsed

    return results


# ---------------------------------------------------------------------------
# Standard measurement functions for use with run_tdvp
# ---------------------------------------------------------------------------

def measure_energy(psi, t, model=None):
    """Measure total energy ⟨H⟩."""
    if model is not None:
        return model.bond_energies(psi).sum()
    return None


def measure_magnetization_z(psi, t):
    """Measure average σ^z."""
    return np.mean(psi.expectation_value('Sigmaz'))


def measure_staggered_mag_y(psi, t):
    """Measure staggered magnetization m_y."""
    vals = psi.expectation_value('Sigmay')
    L = len(vals)
    signs = np.array([(-1)**j for j in range(L)])
    return np.abs(np.mean(signs * vals))


def measure_half_chain_entropy(psi, t):
    """Measure half-chain entanglement entropy."""
    entropies = psi.entanglement_entropy()
    return entropies[len(entropies) // 2]


def measure_max_chi(psi, t):
    """Measure maximum bond dimension."""
    return max(psi.chi)
