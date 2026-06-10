"""
Finite-size scaling analysis for extracting critical exponents.

Critical exponents of the CIM (Table I of the paper):
    ν = 1, z = 1, β = 3/8, α = 0

Methods:
- Energy gap scaling: Δ(L) ~ L^{-z}
- Order parameter scaling: m(λ_c, L) ~ L^{-β/ν}
- Data collapse for ν
- Second derivative of energy (log divergence, α=0)
"""

import numpy as np
from scipy.optimize import curve_fit


def fit_gap_scaling(L_values, gap_values):
    """
    Fit energy gap Δ(L) ~ a * L^{-z} at the critical point.

    Extracts dynamical critical exponent z.

    Parameters
    ----------
    L_values : array-like
        System sizes.
    gap_values : array-like
        Energy gaps at criticality.

    Returns
    -------
    z : float
        Dynamical critical exponent (expected z=1).
    a : float
        Prefactor.
    z_err : float
        Standard error on z.
    """
    L = np.asarray(L_values, dtype=float)
    gaps = np.asarray(gap_values, dtype=float)

    # Fit in log-log: log(Δ) = -z log(L) + log(a)
    log_L = np.log(L)
    log_gap = np.log(gaps)

    coeffs, cov = np.polyfit(log_L, log_gap, 1, cov=True)
    z = -coeffs[0]
    a = np.exp(coeffs[1])
    z_err = np.sqrt(cov[0, 0])

    return z, a, z_err


def fit_order_parameter_scaling(L_values, m_values, exponent_name='beta_over_nu'):
    """
    Fit order parameter m(L) ~ a * L^{-β/ν} at the critical point.

    Parameters
    ----------
    L_values : array-like
        System sizes.
    m_values : array-like
        Order parameter values at criticality.
    exponent_name : str
        Label for the exponent ratio.

    Returns
    -------
    beta_over_nu : float
        β/ν ratio (expected 3/8 for CIM).
    a : float
        Prefactor.
    err : float
        Standard error.
    """
    L = np.asarray(L_values, dtype=float)
    m = np.asarray(m_values, dtype=float)

    mask = m > 1e-15
    if np.sum(mask) < 3:
        return 0.0, 0.0, np.inf

    log_L = np.log(L[mask])
    log_m = np.log(m[mask])

    coeffs, cov = np.polyfit(log_L, log_m, 1, cov=True)
    ratio = -coeffs[0]
    a = np.exp(coeffs[1])
    err = np.sqrt(cov[0, 0])

    return ratio, a, err


def correlation_length_scaling(lam_values, xi_values, lam_c=1.0):
    """
    Fit correlation length ξ ~ |λ - λ_c|^{-ν}.

    Parameters
    ----------
    lam_values : array-like
        λ values (near but not at critical point).
    xi_values : array-like
        Correlation lengths.
    lam_c : float
        Critical point (default 1.0).

    Returns
    -------
    nu : float
        Correlation length exponent (expected ν=1).
    a : float
        Prefactor.
    nu_err : float
        Standard error on ν.
    """
    lam = np.asarray(lam_values, dtype=float)
    xi = np.asarray(xi_values, dtype=float)

    delta = np.abs(lam - lam_c)
    mask = (delta > 1e-10) & (xi > 0) & np.isfinite(xi)
    if np.sum(mask) < 3:
        return 1.0, 1.0, np.inf

    log_delta = np.log(delta[mask])
    log_xi = np.log(xi[mask])

    coeffs, cov = np.polyfit(log_delta, log_xi, 1, cov=True)
    nu = -coeffs[0]
    a = np.exp(coeffs[1])
    nu_err = np.sqrt(cov[0, 0])

    return nu, a, nu_err


def order_parameter_exponent(lam_values, m_values, lam_c=1.0, side='right'):
    """
    Fit order parameter m ~ |λ - λ_c|^β near the critical point.

    Parameters
    ----------
    lam_values : array-like
        λ values.
    m_values : array-like
        Order parameter values.
    lam_c : float
        Critical point.
    side : str
        'right' (λ > λ_c) or 'left' (λ < λ_c).

    Returns
    -------
    beta : float
        Order parameter exponent (expected β=3/8 for m_y).
    a : float
        Prefactor.
    beta_err : float
        Standard error on β.
    """
    lam = np.asarray(lam_values, dtype=float)
    m = np.asarray(m_values, dtype=float)

    if side == 'right':
        mask = (lam > lam_c + 1e-6) & (m > 1e-15)
    else:
        mask = (lam < lam_c - 1e-6) & (m > 1e-15)

    if np.sum(mask) < 3:
        return 0.0, 0.0, np.inf

    delta = np.abs(lam[mask] - lam_c)
    log_delta = np.log(delta)
    log_m = np.log(m[mask])

    coeffs, cov = np.polyfit(log_delta, log_m, 1, cov=True)
    beta = coeffs[0]
    a = np.exp(coeffs[1])
    beta_err = np.sqrt(cov[0, 0])

    return beta, a, beta_err


def data_collapse(lam_values, observable_values, L_values,
                  lam_c=1.0, nu=1.0, beta_over_nu=0.375):
    """
    Perform data collapse for finite-size scaling verification.

    Scaling ansatz: m(λ, L) = L^{-β/ν} f[(λ - λ_c) L^{1/ν}]

    Parameters
    ----------
    lam_values : array-like
        λ values for each data point.
    observable_values : array-like
        Observable m(λ, L).
    L_values : array-like
        System sizes for each data point.
    lam_c, nu, beta_over_nu : float
        Critical parameters.

    Returns
    -------
    x_scaled : ndarray
        Scaled variable (λ - λ_c) * L^{1/ν}.
    y_scaled : ndarray
        Scaled observable m * L^{β/ν}.
    """
    lam = np.asarray(lam_values, dtype=float)
    m = np.asarray(observable_values, dtype=float)
    L = np.asarray(L_values, dtype=float)

    x_scaled = (lam - lam_c) * L**(1.0 / nu)
    y_scaled = m * L**beta_over_nu

    return x_scaled, y_scaled
