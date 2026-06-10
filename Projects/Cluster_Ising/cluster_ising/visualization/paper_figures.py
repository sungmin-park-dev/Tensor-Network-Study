"""
Reproduce key figures from PhysRevA.84.022304.

Fig 1:  O_z and m_y vs λ (order parameters, QPT)
Fig 2:  τ (residual entanglement) vs λ
Fig 4:  R^x_r vs λ for r = 3, 6, 9, 12
Fig 5:  R^y_r vs λ for r = 1, 2, 6, 14
Fig 11: S_L vs L at critical point (c = 3/2)
"""

import numpy as np
import matplotlib.pyplot as plt


def setup_style():
    """Set publication-quality plot style."""
    plt.rcParams.update({
        'figure.figsize': (8, 6),
        'font.size': 14,
        'axes.labelsize': 16,
        'axes.titlesize': 16,
        'legend.fontsize': 12,
        'xtick.labelsize': 12,
        'ytick.labelsize': 12,
        'lines.linewidth': 2,
        'figure.dpi': 100,
    })


def plot_order_parameters(lam_range, m_y, O_z, ax=None, title=None):
    """
    Reproduce Fig. 1: O_z and m_y vs λ.

    Parameters
    ----------
    lam_range : array
        λ values.
    m_y : array
        Staggered magnetization.
    O_z : array
        String order parameter.
    ax : matplotlib axis or None
    title : str or None
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(lam_range, O_z, 'b-', label=r'$\mathcal{O}_z$ (string order)', linewidth=2)
    ax.plot(lam_range, m_y, 'r-', label=r'$m_y$ (stag. magnetization)', linewidth=2)

    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5, label=r'QPT ($\lambda=1$)')
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel('Order parameter')
    ax.set_title(title or r'Fig. 1: Order parameters vs $\lambda$')
    ax.legend()

    # Phase labels
    ax.text(0.5, 0.15, 'Cluster\nphase', transform=ax.transAxes,
            ha='left', fontsize=11, style='italic', alpha=0.6)
    ax.text(0.75, 0.15, 'AF\nphase', transform=ax.transAxes,
            ha='left', fontsize=11, style='italic', alpha=0.6)

    ax.set_xlim([lam_range[0], lam_range[-1]])
    ax.set_ylim([-0.05, 1.05])

    return ax


def plot_residual_entanglement(lam_range, tau, ax=None, title=None):
    """
    Reproduce Fig. 2: τ (residual multipartite entanglement) vs λ.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(lam_range, tau, 'k-', linewidth=2)
    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)

    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$\tau$ (multipartite entanglement)')
    ax.set_title(title or r'Fig. 2: Residual entanglement $\tau$ vs $\lambda$')
    ax.set_xlim([lam_range[0], lam_range[-1]])
    ax.set_ylim([-0.05, 1.05])

    return ax


def plot_correlations_Rx(lam_range, Rx_dict, ax=None, title=None):
    """
    Reproduce Fig. 4: |R^x_r| vs λ for multiple r values.

    Parameters
    ----------
    lam_range : array
        λ values.
    Rx_dict : dict
        {r: array of R^x_r values}. r should be multiples of 3.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(Rx_dict)))
    for (r, vals), color in zip(sorted(Rx_dict.items()), colors):
        sign = (-1)**(r // 3)
        label = rf'$R^x_{{{r}}}$'
        ax.plot(lam_range, np.abs(vals), color=color, label=label)

    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$|R^x_r|$')
    ax.set_title(title or r'Fig. 4: $|R^x_r(0)|$ vs $\lambda$')
    ax.legend()

    return ax


def plot_correlations_Ry(lam_range, Ry_dict, ax=None, title=None):
    """
    Reproduce Fig. 5: |R^y_r| vs λ for multiple r values.

    Parameters
    ----------
    lam_range : array
        λ values.
    Ry_dict : dict
        {r: array of R^y_r values}.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    colors = plt.cm.plasma(np.linspace(0.2, 0.8, len(Ry_dict)))
    for (r, vals), color in zip(sorted(Ry_dict.items()), colors):
        ax.plot(lam_range, np.abs(vals), color=color, label=rf'$R^y_{{{r}}}$')

    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$|R^y_r|$')
    ax.set_title(title or r'Fig. 5: $|R^y_r(0)|$ vs $\lambda$')
    ax.legend()

    return ax


def plot_block_entropy_scaling(L_values, S_values, c_fit=None, ax=None, title=None):
    """
    Reproduce Fig. 11: S_L vs L at the critical point.

    Parameters
    ----------
    L_values : array
        System sizes.
    S_values : array
        Half-chain entanglement entropies.
    c_fit : dict or None
        Fit results from fit_central_charge.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(L_values, S_values, 'rx', markersize=8, label='Data')

    if c_fit is not None:
        L_fit = np.linspace(min(L_values), max(L_values), 100)
        a = c_fit['c'] / 6.0  # coefficient of log₂(L) for OBC
        S_fit = a * np.log2(L_fit) + c_fit['const']
        label = rf'Fit: $S_L = {a:.3f} \log_2 L + {c_fit["const"]:.3f}$, $c={c_fit["c"]:.3f}$'
        ax.plot(L_fit, S_fit, 'b-', label=label)

    ax.set_xlabel(r'Block length $L$')
    ax.set_ylabel(r'$S_L$')
    ax.set_title(title or r'Fig. 11: Block entropy at $\lambda=1$ (critical)')
    ax.legend()

    return ax


def plot_energy_comparison(lam_range, energies_exact, energies_dmrg=None,
                           energies_ed=None, ax=None, title=None):
    """
    Plot ground-state energy per site: exact vs numerical methods.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(lam_range, energies_exact, 'k-', label='Exact (JW)', linewidth=2)

    if energies_dmrg is not None:
        ax.plot(lam_range, energies_dmrg, 'ro', markersize=5,
                label='DMRG', alpha=0.7)

    if energies_ed is not None:
        ax.plot(lam_range, energies_ed, 'bs', markersize=4,
                label='ED', alpha=0.7)

    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5, label=r'$\lambda_c=1$')
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$E_0 / L$')
    ax.set_title(title or r'Ground-state energy per site vs $\lambda$')
    ax.legend()

    return ax


def plot_free_energy_equivalence(lam_range, f_cim, f_ising, ax=None, title=None):
    """
    Plot the free-energy density of the CIM and its effective Ising chain.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(lam_range, f_cim, 'k-', linewidth=2, label='CIM')
    ax.plot(lam_range, f_ising, 'C1--', linewidth=2, label='Effective Ising')
    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$f(\beta, \lambda)$')
    ax.set_title(title or 'Free-energy density equivalence')
    ax.legend()
    return ax


def plot_pairwise_concurrence(r_values, concurrence_dict, ax=None, title=None):
    """
    Plot pairwise concurrence profiles for one or more parameter choices.

    Parameters
    ----------
    r_values : array
        Distances between spins.
    concurrence_dict : dict
        Mapping from label to concurrence values.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 5))

    for label, values in concurrence_dict.items():
        ax.plot(r_values, values, 'o-', ms=4, label=label)

    ax.set_xlabel(r'Distance $r$')
    ax.set_ylabel(r'Concurrence $C(r)$')
    ax.set_title(title or 'Pairwise concurrence')
    ax.legend()
    return ax


def plot_phase_diagram_summary(lam_range, data, figsize=(14, 10)):
    """
    Create a multi-panel summary figure of the CIM phase diagram.

    Parameters
    ----------
    lam_range : array
        λ values.
    data : dict
        Must contain 'E0', 'O_z', 'm_y', 'tau'.
        Optionally 'Rx', 'Ry', 'S_L', 'S_fit'.
    """
    setup_style()

    n_panels = 4
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    axes = axes.flatten()

    # Panel 1: Energy
    axes[0].plot(lam_range, data['E0'], 'k-', linewidth=2)
    axes[0].axvline(x=1.0, color='gray', linestyle='--', alpha=0.5)
    axes[0].set_xlabel(r'$\lambda$')
    axes[0].set_ylabel(r'$E_0/L$')
    axes[0].set_title(r'(a) Ground-state energy')

    # Panel 2: Order parameters
    plot_order_parameters(lam_range, data['m_y'], data['O_z'], ax=axes[1],
                          title=r'(b) Order parameters')

    # Panel 3: Residual entanglement
    plot_residual_entanglement(lam_range, data['tau'], ax=axes[2],
                               title=r'(c) Multipartite entanglement')

    # Panel 4: Entanglement entropy (if available)
    if 'S_L' in data and 'L_values' in data:
        plot_block_entropy_scaling(data['L_values'], data['S_L'],
                                  data.get('S_fit'), ax=axes[3],
                                  title=r'(d) Block entropy at $\lambda_c$')
    else:
        axes[3].text(0.5, 0.5, 'Entropy scaling\n(requires DMRG data)',
                     ha='center', va='center', transform=axes[3].transAxes)
        axes[3].set_title(r'(d) Block entropy')

    fig.tight_layout()
    return fig, axes
