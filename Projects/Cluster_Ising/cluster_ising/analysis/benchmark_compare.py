"""
Cross-benchmark comparison between different solvers.

Compares ED, DMRG, NQS (future), and exact analytical results
on common metrics: energy, order parameters, entanglement, timing.
"""

import numpy as np
from ..observables.order_parameters import staggered_magnetization_y, string_order_z
from ..observables.entanglement import half_chain_entropy


def compare_energies(results, exact_energy=None):
    """
    Compare ground-state energies across solvers.

    Parameters
    ----------
    results : list of SolverResult
        Results from different solvers.
    exact_energy : float or None
        Exact analytical energy for reference.

    Returns
    -------
    dict
        Comparison table with solver names, energies, errors, and timings.
    """
    table = {
        'solver': [],
        'energy': [],
        'energy_per_site': [],
        'error': [],
        'relative_error': [],
        'wall_time': [],
    }

    ref_energy = exact_energy
    if ref_energy is None and results:
        # Use the most accurate solver as reference
        ref_energy = min(r.energy for r in results)

    for r in results:
        table['solver'].append(r.solver_name)
        table['energy'].append(r.energy)
        table['energy_per_site'].append(r.energy_per_site)
        err = abs(r.energy - ref_energy) if ref_energy is not None else None
        table['error'].append(err)
        rel_err = err / abs(ref_energy) if (ref_energy and ref_energy != 0) else None
        table['relative_error'].append(rel_err)
        table['wall_time'].append(r.metadata.get('wall_time', None))

    if exact_energy is not None:
        table['solver'].append('Exact')
        table['energy'].append(exact_energy)
        table['energy_per_site'].append(exact_energy / results[0].num_sites if results else None)
        table['error'].append(0.0)
        table['relative_error'].append(0.0)
        table['wall_time'].append(None)

    return table


def compare_observables(results, observables=None):
    """
    Compare observables across solvers.

    Parameters
    ----------
    results : list of SolverResult
        Results from different solvers.
    observables : list of str or None
        Which observables to compare. Default: ['m_y', 'O_z', 'S_half'].

    Returns
    -------
    dict
        {observable_name: {solver_name: value}}
    """
    if observables is None:
        observables = ['m_y', 'O_z', 'S_half']

    comparison = {obs: {} for obs in observables}

    for r in results:
        L = r.num_sites

        if 'm_y' in observables:
            try:
                m_y = staggered_magnetization_y(r.state, L, r.state_type)
                comparison['m_y'][r.solver_name] = m_y
            except Exception:
                comparison['m_y'][r.solver_name] = None

        if 'O_z' in observables:
            try:
                O_z = string_order_z(r.state, L, r.state_type)
                comparison['O_z'][r.solver_name] = O_z
            except Exception:
                comparison['O_z'][r.solver_name] = None

        if 'S_half' in observables:
            try:
                S = half_chain_entropy(r.state, L, r.state_type)
                comparison['S_half'][r.solver_name] = S
            except Exception:
                comparison['S_half'][r.solver_name] = None

    return comparison


def print_comparison_table(energy_table):
    """Pretty-print the energy comparison table."""
    header = f"{'Solver':<10} {'E₀':>14} {'E₀/L':>14} {'|ΔE|':>12} {'Time(s)':>10}"
    print(header)
    print("-" * len(header))

    for i in range(len(energy_table['solver'])):
        solver = energy_table['solver'][i]
        E = energy_table['energy'][i]
        eps = energy_table['energy_per_site'][i]
        err = energy_table['error'][i]
        t = energy_table['wall_time'][i]

        E_str = f"{E:14.10f}" if E is not None else f"{'N/A':>14}"
        eps_str = f"{eps:14.10f}" if eps is not None else f"{'N/A':>14}"
        err_str = f"{err:12.2e}" if err is not None else f"{'N/A':>12}"
        t_str = f"{t:10.3f}" if t is not None else f"{'N/A':>10}"

        print(f"{solver:<10} {E_str} {eps_str} {err_str} {t_str}")
