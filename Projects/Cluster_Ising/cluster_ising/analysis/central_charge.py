"""
Central charge extraction from entanglement entropy scaling.

The CIM has central charge c = 3/2, corresponding to three
decoupled Ising chains (3 × c_Ising = 3 × 1/2 = 3/2).

The Calabrese-Cardy formula:
    S_L = (c/6) log₂(L) + const     (OBC, half-chain)
    S_L = (c/3) log₂(L) + const     (PBC, half-chain)
"""

import numpy as np
from ..observables.entanglement import fit_central_charge, calabrese_cardy_entropy


def extract_central_charge(results_dict, bc='open'):
    """
    Extract central charge from a set of DMRG/ED results at different L.

    Parameters
    ----------
    results_dict : dict
        {L: SolverResult} mapping system size to result at λ_c.
    bc : str
        Boundary conditions.

    Returns
    -------
    dict with keys:
        'c': central charge estimate
        'c_err': error on c
        'const': non-universal constant
        'L_values': system sizes used
        'S_values': entropy values
    """
    L_values = sorted(results_dict.keys())
    S_values = []

    for L in L_values:
        result = results_dict[L]
        if result.state_type == 'mps':
            entropies = result.state.entanglement_entropy()
            S_half = entropies[L // 2 - 1]
        elif result.state_type == 'vector':
            from ..observables.entanglement import half_chain_entropy
            S_half = half_chain_entropy(result.state, L, 'vector')
        S_values.append(S_half)

    L_arr = np.array(L_values, dtype=float)
    S_arr = np.array(S_values)

    c, const, c_err = fit_central_charge(L_arr, S_arr, bc)

    return {
        'c': c,
        'c_err': c_err,
        'const': const,
        'L_values': L_arr,
        'S_values': S_arr,
    }


def verify_three_ising_decomposition(lam_values, energies_cim, energies_ising):
    """
    Verify the effective three-Ising decomposition at the level of density.

    The Cluster-Ising Hamiltonian decomposes into three decoupled Ising chains
    living on the three sublattices. Since each Ising chain has length N/3, the
    free-energy density per physical site matches the free-energy density of a
    single effective Ising chain.

    Parameters
    ----------
    lam_values : array-like
        λ values.
    energies_cim : array-like
        CIM ground-state energies per site.
    energies_ising : array-like
        Ising chain ground-state energies per site (for the same λ).

    Returns
    -------
    dict with:
        'max_error': maximum discrepancy
        'errors': array of discrepancies
    """
    e_cim = np.asarray(energies_cim)
    e_ising = np.asarray(energies_ising)

    # After normalizing by the total number of physical sites, the densities
    # coincide even though the model factorizes into three sublattice chains.
    errors = np.abs(e_cim - e_ising)

    return {
        'max_error': np.max(errors),
        'errors': errors,
    }
