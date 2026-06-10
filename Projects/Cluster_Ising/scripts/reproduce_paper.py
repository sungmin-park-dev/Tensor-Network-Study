#!/usr/bin/env python
"""
Generate lightweight reproduction outputs for Phys. Rev. A 84, 022304.
"""

import argparse
import json
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

os.environ.setdefault("MPLCONFIGDIR", str(PROJECT_ROOT / ".mplconfig"))

import matplotlib.pyplot as plt
import numpy as np

from cluster_ising.analysis.central_charge import extract_central_charge
from cluster_ising.analysis.thermodynamics import free_energy_equivalence_grid
from cluster_ising.models.exact_solution import (
    correlation_Rx,
    correlation_Ry,
    energy_vs_lambda,
    order_parameters_vs_lambda,
)
from cluster_ising.observables.pairwise_entanglement import (
    exact_pairwise_concurrence_profile,
)
from cluster_ising.solvers.dmrg_solver import run_dmrg
from cluster_ising.solvers.ed_solver import run_ed
from cluster_ising.visualization.paper_figures import (
    plot_block_entropy_scaling,
    plot_correlations_Rx,
    plot_correlations_Ry,
    plot_free_energy_equivalence,
    plot_order_parameters,
    plot_pairwise_concurrence,
    plot_residual_entanglement,
    setup_style,
)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Reproduce the main numerical claims of the Cluster-Ising paper."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=PROJECT_ROOT / "data" / "figures" / "paper_reproduction",
        help="Directory where figures and summaries will be written.",
    )
    parser.add_argument("--lam-min", type=float, default=0.05)
    parser.add_argument("--lam-max", type=float, default=3.0)
    parser.add_argument("--n-lam", type=int, default=80)
    parser.add_argument(
        "--ed-sizes",
        type=int,
        nargs="+",
        default=[6, 8, 10, 12, 14],
        help="Open-chain sizes used for ED central-charge extraction.",
    )
    parser.add_argument(
        "--r-max",
        type=int,
        default=16,
        help="Maximum distance used in concurrence profiles.",
    )
    parser.add_argument(
        "--with-dmrg",
        action="store_true",
        help="Add larger DMRG systems to the central-charge fit.",
    )
    parser.add_argument(
        "--dmrg-sizes",
        type=int,
        nargs="+",
        default=[20, 40, 60],
        help="Finite sizes used for the optional DMRG central-charge fit.",
    )
    parser.add_argument(
        "--chi-max",
        type=int,
        default=120,
        help="Maximum bond dimension used in the optional DMRG fit.",
    )
    return parser.parse_args()


def save_current_figure(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()


def build_phase_diagram_outputs(lam_values, output_dir, summary):
    energies = energy_vs_lambda(lam_values)
    order_params = order_parameters_vs_lambda(lam_values)

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_order_parameters(lam_values, order_params["m_y"], order_params["O_z"], ax=ax)
    save_current_figure(output_dir / "figure_01_order_parameters.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_residual_entanglement(lam_values, order_params["tau"], ax=ax)
    save_current_figure(output_dir / "figure_02_residual_entanglement.png")

    summary["phase_diagram"] = {
        "lambda_range": [float(lam_values[0]), float(lam_values[-1])],
        "n_points": int(len(lam_values)),
        "energy_min": float(np.min(energies)),
        "energy_max": float(np.max(energies)),
    }


def build_correlation_outputs(lam_values, output_dir, summary):
    rx_distances = [3, 6, 9, 12]
    ry_distances = [1, 2, 6, 14]
    rx_data = {
        r: np.array([correlation_Rx(r, lam) for lam in lam_values])
        for r in rx_distances
    }
    ry_data = {
        r: np.array([correlation_Ry(r, lam) for lam in lam_values])
        for r in ry_distances
    }

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_correlations_Rx(lam_values, rx_data, ax=ax)
    save_current_figure(output_dir / "figure_04_rx_vs_lambda.png")

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_correlations_Ry(lam_values, ry_data, ax=ax)
    save_current_figure(output_dir / "figure_05_ry_vs_lambda.png")

    summary["correlations"] = {
        "rx_distances": rx_distances,
        "ry_distances": ry_distances,
    }


def build_free_energy_outputs(lam_values, output_dir, summary):
    beta_values = [np.inf, 5.0, 2.0, 1.0]
    data = free_energy_equivalence_grid(lam_values, beta_values)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    zero_temp = data[float(np.inf)]
    plot_free_energy_equivalence(
        lam_values,
        zero_temp["f_cim"],
        zero_temp["f_ising"],
        ax=axes[0],
        title="Ground-state energy density",
    )

    for beta in beta_values:
        entry = data[float(beta)]
        label = "T=0" if np.isinf(beta) else f"beta={beta:g}"
        axes[1].semilogy(
            lam_values,
            np.maximum(entry["errors"], 1e-18),
            label=label,
        )
    axes[1].set_xlabel(r'$\lambda$')
    axes[1].set_ylabel("Absolute error")
    axes[1].set_title("CIM vs effective Ising free-energy density")
    axes[1].legend()
    save_current_figure(output_dir / "free_energy_equivalence.png")

    summary["free_energy_equivalence"] = {
        ("inf" if np.isinf(beta) else str(beta)): {
            "max_error": float(data[float(beta)]["max_error"])
        }
        for beta in beta_values
    }


def build_concurrence_outputs(r_max, output_dir, summary):
    r_values = np.arange(1, r_max + 1)

    ground_profiles = {
        f"lambda={lam:g}, T=0": exact_pairwise_concurrence_profile(lam, r_values)
        for lam in (0.5, 1.0, 1.5)
    }
    thermal_profiles = {
        f"beta={beta:g}": exact_pairwise_concurrence_profile(0.5, r_values, beta)
        for beta in (5.0, 2.0, 1.0)
    }

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    plot_pairwise_concurrence(
        r_values,
        ground_profiles,
        ax=axes[0],
        title="Ground-state pairwise concurrence",
    )
    plot_pairwise_concurrence(
        r_values,
        thermal_profiles,
        ax=axes[1],
        title="Thermal pairwise concurrence (lambda=0.5)",
    )
    save_current_figure(output_dir / "pairwise_concurrence.png")

    all_values = []
    for values in list(ground_profiles.values()) + list(thermal_profiles.values()):
        all_values.extend(np.asarray(values).tolist())

    summary["pairwise_entanglement"] = {
        "r_max": int(r_max),
        "max_concurrence": float(np.max(np.abs(all_values))) if all_values else 0.0,
    }


def build_central_charge_outputs(ed_sizes, output_dir, summary, with_dmrg=False,
                                 dmrg_sizes=None, chi_max=120):
    results = {}
    for L in ed_sizes:
        result = run_ed({"L": L, "lam": 1.0, "bc": "open"}, n_states=1)
        results[L] = result

    if with_dmrg:
        import warnings

        warnings.filterwarnings("ignore", category=UserWarning)
        dmrg_params = {
            "trunc_params": {"chi_max": chi_max, "svd_min": 1e-10},
            "mixer": True,
            "mixer_params": {
                "amplitude": 1e-5,
                "decay": 1.5,
                "disable_after": 30,
            },
            "max_sweeps": 60,
            "max_E_err": 1e-12,
            "max_S_err": 1e-8,
        }
        for L in dmrg_sizes or []:
            result = run_dmrg(
                {
                    "L": L,
                    "lam": 1.0,
                    "bc_MPS": "finite",
                    "conserve": "parity",
                },
                dmrg_params,
            )
            results[L] = result

    c_fit = extract_central_charge(results, bc="open")

    fig, ax = plt.subplots(figsize=(8, 5))
    plot_block_entropy_scaling(
        c_fit["L_values"],
        c_fit["S_values"],
        c_fit,
        ax=ax,
        title="Half-chain entropy at lambda=1",
    )
    save_current_figure(output_dir / "figure_11_central_charge.png")

    summary["central_charge"] = {
        "ed_sizes": [int(L) for L in sorted(ed_sizes)],
        "dmrg_sizes": [int(L) for L in sorted(dmrg_sizes or [])] if with_dmrg else [],
        "method": "ED + DMRG" if with_dmrg else "ED only",
        "c": float(c_fit["c"]),
        "c_err": float(c_fit["c_err"]),
    }


def write_summary(summary, output_dir):
    json_path = output_dir / "paper_reproduction_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True))

    md_lines = [
        "# Paper Reproduction Summary",
        "",
        "Generated by `scripts/reproduce_paper.py`.",
        "",
        "## Numerical checks",
        "",
        f"- Central-charge fit method: {summary['central_charge']['method']}",
        f"- Central charge estimate: c = {summary['central_charge']['c']:.6f}",
        f"- Max pairwise concurrence: {summary['pairwise_entanglement']['max_concurrence']:.3e}",
    ]
    if summary["central_charge"]["method"] == "ED only":
        md_lines.append(
            "- Note: the ED-only central-charge fit is a coarse finite-size estimate; "
            "use `--with-dmrg` for a stronger reproduction of the c = 3/2 claim."
        )
    for beta, entry in summary["free_energy_equivalence"].items():
        md_lines.append(
            f"- Free-energy max error (beta={beta}): {entry['max_error']:.3e}"
        )
    (output_dir / "paper_reproduction_summary.md").write_text("\n".join(md_lines) + "\n")


def main():
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    setup_style()

    lam_values = np.linspace(args.lam_min, args.lam_max, args.n_lam)
    summary = {
        "paper": {
            "title": "Statistical mechanics of the cluster Ising model",
            "doi": "10.1103/PhysRevA.84.022304",
        }
    }

    build_phase_diagram_outputs(lam_values, args.output_dir, summary)
    build_correlation_outputs(lam_values, args.output_dir, summary)
    build_free_energy_outputs(lam_values, args.output_dir, summary)
    build_concurrence_outputs(args.r_max, args.output_dir, summary)
    build_central_charge_outputs(
        args.ed_sizes,
        args.output_dir,
        summary,
        with_dmrg=args.with_dmrg,
        dmrg_sizes=args.dmrg_sizes,
        chi_max=args.chi_max,
    )
    write_summary(summary, args.output_dir)

    print(f"Saved reproduction outputs to: {args.output_dir}")


if __name__ == "__main__":
    main()
