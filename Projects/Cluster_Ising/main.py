#!/usr/bin/env python
"""
Unified ground-state energy benchmark for the Cluster-Ising Model.

Compares Exact (analytical), ED, DMRG, and NQS solvers for
H(λ) = -J_c Σ σ^x_{j-1} σ^z_j σ^x_{j+1} + λ Σ σ^y_j σ^y_{j+1}

Usage examples:
    # Single point
    python main.py --lam 0.5 --L 10 --solvers exact ed

    # Multiple lambda values with plot
    python main.py --lam 0.5 1.0 1.5 2.0 --L 12 --solvers exact ed dmrg --plot

    # Lambda sweep with plot
    python main.py --lam-sweep 0.0 2.0 21 --L 10 --solvers exact ed --plot

    # Multiple system sizes
    python main.py --lam 1.0 --L 8 10 12 14 --solvers exact ed --plot

    # All solvers including NQS (OBC recommended)
    python main.py --lam 0.5 --L 6 --bc open --solvers ed nqs --plot

    # Save figure to file
    python main.py --lam-sweep 0.0 2.0 21 --L 10 --solvers exact ed --save-fig benchmark.png
"""

import argparse
import sys
import time
import warnings
import numpy as np

# Suppress TeNPy and JAX warnings for cleaner output
warnings.filterwarnings('ignore', category=UserWarning)


# ---------------------------------------------------------------------------
# Solver styles for plotting
# ---------------------------------------------------------------------------

SOLVER_STYLES = {
    'Exact': dict(color='black', linestyle='-', marker=None, linewidth=2,
                  markersize=0, label='Exact (JW)'),
    'ED':    dict(color='#1f77b4', linestyle='none', marker='s', linewidth=0,
                  markersize=5, label='ED', alpha=0.8),
    'DMRG':  dict(color='#d62728', linestyle='none', marker='^', linewidth=0,
                  markersize=6, label='DMRG', alpha=0.8),
    'NQS':   dict(color='#2ca02c', linestyle='none', marker='D', linewidth=0,
                  markersize=5, label='NQS (VMC)', alpha=0.8),
}


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Cluster-Ising Model: ground-state energy benchmark.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    # Model parameters
    parser.add_argument('--L', type=int, nargs='+', default=[8],
                        help='System size(s). Default: 8')
    parser.add_argument('--lam', type=float, nargs='+', default=None,
                        help='Lambda value(s). Default: 0.5')
    parser.add_argument('--lam-sweep', type=float, nargs=3, default=None,
                        metavar=('START', 'STOP', 'NPOINTS'),
                        help='Lambda sweep: start stop npoints')
    parser.add_argument('--bc', type=str, default='periodic',
                        choices=['periodic', 'open'],
                        help='Boundary conditions. Default: periodic')
    parser.add_argument('--J-c', type=float, default=1.0,
                        help='Cluster coupling J_c. Default: 1.0')

    # Solver selection
    parser.add_argument('--solvers', type=str, nargs='+',
                        default=['exact', 'ed', 'dmrg', 'nqs'],
                        choices=['exact', 'ed', 'dmrg', 'nqs'],
                        help='Solvers to run. Default: exact ed dmrg nqs')

    # DMRG-specific
    parser.add_argument('--chi-max', type=int, default=200,
                        help='DMRG max bond dimension. Default: 200')

    # NQS-specific
    parser.add_argument('--nqs-ansatz', type=str, default='RBM',
                        choices=['RBM', 'RBMSymm'],
                        help='NQS ansatz. Default: RBM')
    parser.add_argument('--nqs-alpha', type=int, default=1,
                        help='NQS hidden unit density. Default: 1')
    parser.add_argument('--nqs-samples', type=int, default=1024,
                        help='NQS MC samples. Default: 1024')
    parser.add_argument('--nqs-iter', type=int, default=300,
                        help='NQS optimization iterations. Default: 300')
    parser.add_argument('--nqs-lr', type=float, default=0.01,
                        help='NQS learning rate. Default: 0.01')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random seed for NQS.')

    # Output
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output with solver details.')
    parser.add_argument('--no-plot', action='store_true',
                        help='Suppress matplotlib plot (shown by default).')
    parser.add_argument('--save-fig', type=str, default=None,
                        metavar='PATH',
                        help='Save figure to file (e.g. benchmark.png).')

    return parser.parse_args()


def get_lambda_values(args):
    """Resolve lambda values from --lam or --lam-sweep."""
    if args.lam_sweep is not None:
        start, stop, npoints = args.lam_sweep
        return np.linspace(start, stop, int(npoints))
    elif args.lam is not None:
        return np.array(args.lam)
    else:
        # Default: λ sweep 0→2 (11 points) for a quick overview plot
        return np.linspace(0.0, 2.0, 11)


# ---------------------------------------------------------------------------
# Solver dispatch
# ---------------------------------------------------------------------------

def run_exact(model_params):
    """Run the analytical exact solution (Jordan-Wigner)."""
    from cluster_ising.models.exact_solution import (
        ground_state_energy_density, ground_state_energy_total,
    )
    from cluster_ising.solvers.base_solver import SolverResult, Timer

    L = model_params['L']
    lam = model_params['lam']
    bc = model_params.get('bc', 'periodic')

    with Timer() as timer:
        if bc == 'periodic':
            E_per_site = ground_state_energy_density(lam, N=L)
            E_total = E_per_site * L
        else:
            # OBC: use thermodynamic limit as reference
            E_per_site = ground_state_energy_density(lam, N=None)
            E_total = E_per_site * L

    return SolverResult(
        solver_name='Exact',
        energy=E_total,
        energy_per_site=E_per_site,
        state=None,
        state_type='analytical',
        num_sites=L,
        model_params=dict(model_params),
        metadata={
            'wall_time': timer.elapsed,
            'note': ('finite-N PBC formula' if bc == 'periodic'
                     else 'thermodynamic limit (N→∞)'),
        },
    )


def run_solver(solver_name, model_params, args):
    """Dispatch to the appropriate solver."""
    if solver_name == 'exact':
        return run_exact(model_params)

    elif solver_name == 'ed':
        from cluster_ising.solvers.ed_solver import run_ed
        return run_ed(model_params, n_states=2)

    elif solver_name == 'dmrg':
        from cluster_ising.solvers.dmrg_solver import run_dmrg
        dmrg_params = {
            'trunc_params': {'chi_max': args.chi_max, 'svd_min': 1e-10},
            'mixer': True,
            'mixer_params': {
                'amplitude': 1e-5, 'decay': 1.5, 'disable_after': 30,
            },
            'max_sweeps': 50,
            'max_E_err': 1e-10,
            'max_S_err': 1e-6,
        }
        mp = dict(model_params)
        mp.setdefault('bc_MPS', 'finite')
        mp.setdefault('conserve', 'parity')
        return run_dmrg(mp, dmrg_params)

    elif solver_name == 'nqs':
        from cluster_ising.solvers.nqs_solver import run_nqs
        nqs_params = {
            'ansatz': args.nqs_ansatz,
            'alpha': args.nqs_alpha,
            'n_samples': args.nqs_samples,
            'n_iter': args.nqs_iter,
            'learning_rate': args.nqs_lr,
            'seed': args.seed,
        }
        return run_nqs(model_params, nqs_params)

    else:
        raise ValueError(f"Unknown solver: {solver_name}")


# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

def print_results_table(results, exact_result=None):
    """Print a formatted comparison table."""
    ref_E = exact_result.energy if exact_result else None

    header = (f"  {'Solver':<10} {'E_total':>16} {'E/L':>14} "
              f"{'|dE/L|':>12} {'Time(s)':>10}")
    sep = "  " + "-" * 66

    print(header)
    print(sep)

    for r in results:
        E_str = f"{r.energy:16.10f}"
        eps_str = f"{r.energy_per_site:14.10f}"
        if ref_E is not None and r.solver_name != 'Exact':
            err_ps = abs(r.energy - ref_E) / r.num_sites
            err_str = f"{err_ps:12.2e}"
        else:
            err_str = f"{'---':>12}"
        t = r.metadata.get('wall_time', 0)
        t_str = f"{t:10.3f}"
        print(f"  {r.solver_name:<10} {E_str} {eps_str} {err_str} {t_str}")


def print_solver_details(result, args):
    """Print verbose solver-specific details."""
    meta = result.metadata
    if result.solver_name == 'Exact':
        print(f"    Note: {meta.get('note', '')}")
    elif result.solver_name == 'ED':
        dim = meta.get('hilbert_dim', '?')
        print(f"    Hilbert dim: {dim}, eigenvalues: {meta.get('n_states', '?')}")
    elif result.solver_name == 'DMRG':
        chi = meta.get('chi_max', '?')
        sweeps = meta.get('sweeps', '?')
        max_chi = meta.get('max_chi', '?')
        print(f"    chi_max={chi}, sweeps={sweeps}, actual_chi={max_chi}")
    elif result.solver_name == 'NQS':
        ansatz = meta.get('ansatz', '?')
        alpha = meta.get('alpha', '?')
        var = meta.get('energy_variance', 0)
        conv = meta.get('converged', '?')
        print(f"    ansatz={ansatz}, alpha={alpha}, "
              f"E_var={var:.4f}, converged={conv}")


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

def plot_results(all_results, lam_values, L_values, args):
    """
    Generate benchmark comparison plots.

    Parameters
    ----------
    all_results : dict
        {L: {solver_name: {'lam': [...], 'E_per_site': [...], 'metadata': [...]}}}
    lam_values : array
        Lambda values used in the sweep.
    L_values : list
        System sizes.
    args : argparse.Namespace
        CLI arguments.
    """
    import matplotlib.pyplot as plt
    from cluster_ising.visualization.paper_figures import setup_style
    setup_style()

    n_lam = len(lam_values)
    n_L = len(L_values)
    has_nqs = any(
        'NQS' in all_results.get(L, {})
        for L in L_values
    )

    if n_lam > 1:
        _plot_lambda_sweep(all_results, lam_values, L_values, has_nqs, args)
    elif n_L > 1:
        _plot_size_sweep(all_results, lam_values[0], L_values, has_nqs, args)
    else:
        _plot_single_point(all_results, lam_values[0], L_values[0], args)

    if args.save_fig:
        plt.savefig(args.save_fig, dpi=150, bbox_inches='tight')
        print(f"\n  Figure saved: {args.save_fig}")
    if not args.no_plot:
        plt.show()


def _plot_lambda_sweep(all_results, lam_values, L_values, has_nqs, args):
    """Plot E/L vs λ for one or more system sizes."""
    import matplotlib.pyplot as plt

    n_L = len(L_values)

    # Determine subplot layout
    if has_nqs:
        n_cols = 3  # E/L | |ΔE/L| | NQS convergence
    else:
        n_cols = 2  # E/L | |ΔE/L|

    fig, axes = plt.subplots(n_L, n_cols, figsize=(5 * n_cols, 4 * n_L),
                             squeeze=False)

    for row, L in enumerate(L_values):
        data = all_results.get(L, {})
        ax_e = axes[row, 0]
        ax_err = axes[row, 1]

        # Find reference solver for error (prefer Exact, fallback to ED)
        ref_name = 'Exact' if 'Exact' in data else ('ED' if 'ED' in data else None)

        # Marker fallback for error plot (Exact has no marker by default)
        _err_markers = {'Exact': 'o', 'ED': 's', 'DMRG': '^', 'NQS': 'D'}

        for solver_name, sdata in data.items():
            style = SOLVER_STYLES.get(solver_name, {})
            lams = np.array(sdata['lam'])
            eps = np.array(sdata['E_per_site'])

            ax_e.plot(lams, eps, **style)

            # Error subplot
            if ref_name and solver_name != ref_name:
                ref_eps = np.array(data[ref_name]['E_per_site'])
                err = np.abs(eps - ref_eps)
                mask = err > 1e-16
                if np.any(mask):
                    ax_err.semilogy(lams[mask], err[mask],
                                   color=style.get('color', 'gray'),
                                   marker=_err_markers.get(solver_name, 'o'),
                                   linestyle='-', linewidth=1,
                                   markersize=style.get('markersize', 5),
                                   label=solver_name, alpha=0.8)

        ax_e.axvline(x=1.0, color='gray', linestyle='--', alpha=0.4)
        ax_e.set_xlabel(r'$\lambda$')
        ax_e.set_ylabel(r'$E_0/L$')
        ax_e.set_title(f'L = {L}, bc = {args.bc}')
        ax_e.legend(fontsize=10)

        ax_err.axvline(x=1.0, color='gray', linestyle='--', alpha=0.4)
        ax_err.set_xlabel(r'$\lambda$')
        ax_err.set_ylabel(rf'$|\Delta E/L|$ (vs {ref_name})')
        ax_err.set_title(f'Energy error, L = {L}')
        if ax_err.has_data():
            ax_err.legend(fontsize=10)

        # NQS convergence panel
        if has_nqs and 'NQS' in data:
            ax_nqs = axes[row, 2]
            _plot_nqs_convergence_multi(ax_nqs, data, L)

    fig.suptitle(r'Cluster-Ising Model: $E_0/L$ vs $\lambda$', fontsize=16, y=1.02)
    fig.tight_layout()


def _plot_size_sweep(all_results, lam, L_values, has_nqs, args):
    """Plot E/L vs L for a single λ value."""
    import matplotlib.pyplot as plt

    n_cols = 3 if has_nqs else 2
    fig, axes = plt.subplots(1, n_cols, figsize=(5 * n_cols, 5))
    if n_cols == 1:
        axes = [axes]
    ax_e = axes[0]
    ax_err = axes[1]

    # Collect solver data across L values
    solver_data = {}  # {solver_name: {'L': [], 'E_per_site': []}}
    for L in L_values:
        data = all_results.get(L, {})
        for solver_name, sdata in data.items():
            if solver_name not in solver_data:
                solver_data[solver_name] = {'L': [], 'E_per_site': []}
            # Single λ: take the first (only) entry
            solver_data[solver_name]['L'].append(L)
            solver_data[solver_name]['E_per_site'].append(sdata['E_per_site'][0])

    ref_name = 'Exact' if 'Exact' in solver_data else (
        'ED' if 'ED' in solver_data else None)
    _err_markers = {'Exact': 'o', 'ED': 's', 'DMRG': '^', 'NQS': 'D'}

    for solver_name, sd in solver_data.items():
        style = SOLVER_STYLES.get(solver_name, {})
        Ls = np.array(sd['L'])
        eps = np.array(sd['E_per_site'])

        plot_style = dict(style)
        if plot_style.get('linestyle') == 'none':
            plot_style['linestyle'] = '-'
            plot_style['linewidth'] = 1
        ax_e.plot(Ls, eps, **plot_style)

        if ref_name and solver_name != ref_name:
            ref_eps = np.array(solver_data[ref_name]['E_per_site'])
            err = np.abs(eps - ref_eps)
            mask = err > 1e-16
            if np.any(mask):
                ax_err.semilogy(Ls[mask], err[mask],
                                color=style.get('color', 'gray'),
                                marker=_err_markers.get(solver_name, 'o'),
                                linestyle='-', linewidth=1,
                                markersize=style.get('markersize', 5),
                                label=solver_name, alpha=0.8)

    ax_e.set_xlabel(r'$L$')
    ax_e.set_ylabel(r'$E_0/L$')
    ax_e.set_title(rf'$\lambda = {lam:.2f}$, bc = {args.bc}')
    ax_e.legend(fontsize=10)

    ax_err.set_xlabel(r'$L$')
    ax_err.set_ylabel(rf'$|\Delta E/L|$ (vs {ref_name})')
    ax_err.set_title('Energy error vs system size')
    if ax_err.has_data():
        ax_err.legend(fontsize=10)

    # NQS convergence for the largest L
    if has_nqs:
        ax_nqs = axes[2]
        largest_L = max(L for L in L_values if 'NQS' in all_results.get(L, {}))
        data = all_results[largest_L]
        _plot_nqs_convergence_single(ax_nqs, data, largest_L, lam)

    fig.suptitle(r'Cluster-Ising Model: $E_0/L$ vs $L$', fontsize=16, y=1.02)
    fig.tight_layout()


def _plot_single_point(all_results, lam, L, args):
    """Plot bar chart + NQS convergence for a single (L, λ) point."""
    import matplotlib.pyplot as plt

    data = all_results.get(L, {})
    has_nqs = 'NQS' in data

    n_cols = 2 if has_nqs else 1
    fig, axes = plt.subplots(1, n_cols, figsize=(6 * n_cols, 5))
    if n_cols == 1:
        axes = [axes]

    # Bar chart of E/L
    ax_bar = axes[0]
    names = []
    energies = []
    colors = []
    for solver_name, sdata in data.items():
        names.append(solver_name)
        energies.append(sdata['E_per_site'][0])
        colors.append(SOLVER_STYLES.get(solver_name, {}).get('color', 'gray'))

    bars = ax_bar.bar(names, energies, color=colors, alpha=0.8, edgecolor='black')
    ax_bar.set_ylabel(r'$E_0/L$')
    ax_bar.set_title(rf'$L = {L}$, $\lambda = {lam:.2f}$, bc = {args.bc}')

    # Add value labels on bars
    for bar, e in zip(bars, energies):
        ax_bar.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    f'{e:.6f}', ha='center', va='bottom', fontsize=9)

    # NQS convergence
    if has_nqs:
        _plot_nqs_convergence_single(axes[1], data, L, lam)

    fig.suptitle('Cluster-Ising Model: Solver Comparison', fontsize=16, y=1.02)
    fig.tight_layout()


def _plot_nqs_convergence_single(ax, data, L, lam):
    """Plot NQS energy vs iteration for a single run."""
    nqs_data = data.get('NQS', {})
    if not nqs_data or not nqs_data.get('metadata'):
        ax.text(0.5, 0.5, 'No NQS data', ha='center', va='center',
                transform=ax.transAxes)
        return

    # Take the first (or only) run's metadata
    meta = nqs_data['metadata'][0]
    E_hist = meta.get('energy_history', [])
    if not E_hist:
        return

    iters = np.arange(1, len(E_hist) + 1)
    ax.plot(iters, E_hist, color='#2ca02c', linewidth=1.5, alpha=0.8,
            label='NQS')

    # Show ED reference if available
    if 'ED' in data:
        E_ed = data['ED']['E_per_site'][0] * L
        ax.axhline(y=E_ed, color='#1f77b4', linestyle='--', linewidth=1.5,
                    label=f'ED ($E = {E_ed:.4f}$)')

    # Show Exact reference if available
    if 'Exact' in data:
        E_ex = data['Exact']['E_per_site'][0] * L
        ax.axhline(y=E_ex, color='black', linestyle=':', linewidth=1.5,
                    label=f'Exact ($E = {E_ex:.4f}$)')

    ax.set_xlabel('VMC iteration')
    ax.set_ylabel(r'$E_0$')
    ax.set_title(rf'NQS convergence ($L={L}$, $\lambda={lam:.2f}$)')
    ax.legend(fontsize=9)


def _plot_nqs_convergence_multi(ax, data, L):
    """Plot NQS convergence overview for λ sweep: final E and variance."""
    nqs_data = data.get('NQS', {})
    if not nqs_data:
        ax.text(0.5, 0.5, 'No NQS data', ha='center', va='center',
                transform=ax.transAxes)
        return

    lams = np.array(nqs_data['lam'])
    final_vars = []
    for meta in nqs_data['metadata']:
        final_vars.append(meta.get('energy_variance', 0))
    final_vars = np.array(final_vars)

    ax.semilogy(lams, final_vars, 'D-', color='#2ca02c', markersize=4,
                linewidth=1.5, label=r'$\mathrm{Var}(E)$')
    ax.axvline(x=1.0, color='gray', linestyle='--', alpha=0.4)
    ax.set_xlabel(r'$\lambda$')
    ax.set_ylabel(r'$\mathrm{Var}(E)$ (final)')
    ax.set_title(f'NQS variance, L = {L}')
    ax.legend(fontsize=10)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    lam_values = get_lambda_values(args)
    L_values = args.L
    solvers = args.solvers

    # Print configuration
    print(f"\nCluster-Ising Model: Ground-State Energy Benchmark")
    print(f"  H(λ) = -J_c Σ σ^x σ^z σ^x + λ Σ σ^y σ^y")
    print(f"  J_c = {args.J_c}, bc = {args.bc}")
    print(f"  System sizes: {L_values}")
    print(f"  Lambda values: ", end='')
    if len(lam_values) <= 10:
        print([round(l, 4) for l in lam_values])
    else:
        print(f"{len(lam_values)} points in [{lam_values[0]:.4f}, {lam_values[-1]:.4f}]")
    print(f"  Solvers: {solvers}")

    total_t0 = time.perf_counter()

    # Collect results for plotting
    # Structure: {L: {solver_name: {'lam': [], 'E_per_site': [], 'metadata': []}}}
    all_results = {}

    for L in L_values:
        if L not in all_results:
            all_results[L] = {}

        for lam in lam_values:
            print(f"\n{'='*70}")
            print(f"  L = {L}, λ = {lam:.4f}, bc = {args.bc}")
            print(f"{'='*70}")

            model_params = {
                'L': L,
                'lam': lam,
                'bc': args.bc,
                'J_c': args.J_c,
            }

            results = []
            exact_result = None

            for solver_name in solvers:
                if args.verbose:
                    print(f"  Running {solver_name}...", end='', flush=True)
                try:
                    result = run_solver(solver_name, model_params, args)
                    results.append(result)
                    if solver_name == 'exact':
                        exact_result = result
                    if args.verbose:
                        wt = result.metadata.get('wall_time', 0)
                        print(f" E/L = {result.energy_per_site:.10f} "
                              f"({wt:.2f}s)")

                    # Store for plotting
                    sname = result.solver_name
                    if sname not in all_results[L]:
                        all_results[L][sname] = {
                            'lam': [], 'E_per_site': [], 'metadata': [],
                        }
                    all_results[L][sname]['lam'].append(lam)
                    all_results[L][sname]['E_per_site'].append(
                        result.energy_per_site)
                    all_results[L][sname]['metadata'].append(result.metadata)

                except ImportError as e:
                    print(f"  SKIP {solver_name}: {e}")
                except Exception as e:
                    print(f"  FAIL {solver_name}: {e}")
                    if args.verbose:
                        import traceback
                        traceback.print_exc()

            if results:
                print()
                print_results_table(results, exact_result)

                if args.verbose:
                    print()
                    for r in results:
                        print_solver_details(r, args)

    total_time = time.perf_counter() - total_t0
    print(f"\nTotal wall time: {total_time:.2f}s")

    # Generate plots (shown by default; use --no-plot to suppress)
    if not args.no_plot or args.save_fig:
        plot_results(all_results, lam_values, L_values, args)


if __name__ == '__main__':
    main()
