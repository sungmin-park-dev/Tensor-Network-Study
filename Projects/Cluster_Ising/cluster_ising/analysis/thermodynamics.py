"""
Thermodynamic checks for reproducing the Cluster-Ising paper.

The exact solution maps the Cluster-Ising model to three decoupled Ising
chains living on the three lattice sublattices. After normalizing by the
total number of physical sites, the free-energy density matches that of a
single effective Ising chain with dispersion_ising().
"""

import numpy as np
from scipy import integrate

from ..models.exact_solution import dispersion_ising, free_energy_density


def ising_free_energy_density(lam, beta):
    """
    Free-energy density of the effective Ising chain.

    Parameters
    ----------
    lam : float
        Ising coupling.
    beta : float
        Inverse temperature. Use np.inf for the ground-state limit.

    Returns
    -------
    float
        Free energy per physical site.
    """
    if np.isinf(beta):
        result, _ = integrate.quad(lambda p: dispersion_ising(p, lam), 0, np.pi)
        return -result / np.pi

    def integrand(p):
        return np.log(2.0 * np.cosh(beta * dispersion_ising(p, lam)))

    result, _ = integrate.quad(integrand, 0, np.pi)
    return -result / (np.pi * beta)


def free_energy_equivalence(lam_values, beta):
    """
    Compare the Cluster-Ising free energy density with its Ising equivalent.

    Parameters
    ----------
    lam_values : array-like
        Coupling values to evaluate.
    beta : float
        Inverse temperature.

    Returns
    -------
    dict
        Arrays for the CIM and Ising free energies plus absolute errors.
    """
    lam_values = np.asarray(lam_values, dtype=float)
    f_cim = np.array([free_energy_density(lam, beta) for lam in lam_values])
    f_ising = np.array([ising_free_energy_density(lam, beta) for lam in lam_values])
    errors = np.abs(f_cim - f_ising)
    return {
        "lam_values": lam_values,
        "f_cim": f_cim,
        "f_ising": f_ising,
        "errors": errors,
        "max_error": float(np.max(errors)) if len(errors) else 0.0,
    }


def free_energy_equivalence_grid(lam_values, beta_values):
    """
    Evaluate the free-energy equivalence for multiple temperatures.

    Parameters
    ----------
    lam_values : array-like
        Coupling values to evaluate.
    beta_values : array-like
        Inverse temperatures.

    Returns
    -------
    dict
        Maps each beta to the output of free_energy_equivalence().
    """
    return {
        float(beta): free_energy_equivalence(lam_values, beta)
        for beta in beta_values
    }
