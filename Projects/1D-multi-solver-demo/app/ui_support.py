"""Shared helpers for the Streamlit 1D solver app."""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from one_dimensional_multi_solver_demo import (  # noqa: E402
    ED,
    build_spin_chain,
    change_form,
    connected_correlator_matrix,
    half_chain_entropy,
    match_exact_reference,
    site_expectations,
    solve_ed,
    spin_vectors,
)

DEFAULT_PARAMS = {
    "length": 8,
    "bc": "periodic",
    "jxy": 1.0,
    "jz": 1.0,
    "k": 0.0,
    "hz": 0.0,
    "hx": 0.0,
}

TERM_LABELS = ("Full", "XXZ", "Cluster", "Zeeman")

TERM_COPY = {
    "Full": {
        "title": "Full Hamiltonian",
        "equation": r"H = H_{\mathrm{XXZ}} + H_{\mathrm{cluster}} + H_{\mathrm{Zeeman}}",
        "body": "The current system definition keeps all active terms from the selected parameter family.",
    },
    "XXZ": {
        "title": "XXZ Exchange",
        "equation": (
            r"H_{\mathrm{XXZ}}"
            r"= \sum_{(a,b)\in\mathcal{B}_{L}^{\mathrm{bc}}}"
            r"\left[J_{xy}\left(S_a^xS_b^x+S_a^yS_b^y\right)+J_zS_a^zS_b^z\right]"
        ),
        "body": "Nearest-neighbor two-site exchange terms over the active bond set.",
    },
    "Cluster": {
        "title": "Cluster Interaction",
        "equation": (
            r"H_{\mathrm{cluster}}"
            r"= -K\sum_{c\in\mathcal{C}_{L}^{\mathrm{bc}}}"
            r"S_{\ell(c)}^xS_c^zS_{r(c)}^x"
        ),
        "body": "Three-site stabilizer-type terms over the active cluster-center set.",
    },
    "Zeeman": {
        "title": "Zeeman Field",
        "equation": r"H_{\mathrm{Zeeman}}= -h_z\sum_{a\in\Lambda_L}S_a^z-h_x\sum_{a\in\Lambda_L}S_a^x",
        "body": "On-site longitudinal and transverse field terms over the chain sites.",
    },
}

TERM_LABEL_MAP = {
    "XXZ": {"xx_exchange", "yy_exchange", "zz_exchange"},
    "Cluster": {"cluster"},
    "Zeeman": {"longitudinal_field", "transverse_field"},
}


def ensure_defaults(st) -> None:
    st.session_state.setdefault("params", dict(DEFAULT_PARAMS))
    st.session_state.setdefault("system", build_system(st.session_state["params"]))


def build_system(params):
    return build_spin_chain(
        length=int(params["length"]),
        bc=params["bc"],
        jxy=float(params["jxy"]),
        jz=float(params["jz"]),
        k=float(params["k"]),
        hz=float(params["hz"]),
        hx=float(params["hx"]),
    )


def update_system(st, params) -> None:
    st.session_state["params"] = dict(params)
    st.session_state["system"] = build_system(params)
    st.session_state.pop("result", None)
    st.session_state.pop("observables", None)


def solve_current(st) -> None:
    result = solve_ed(st.session_state["system"])
    system = st.session_state["system"]
    st.session_state["result"] = result
    st.session_state["observables"] = {
        "spin_vectors": spin_vectors(result, system),
        "site_sz": site_expectations(result, system, "Sz"),
        "connected_sz": connected_correlator_matrix(result, system, "Sz"),
        "half_chain_entropy": half_chain_entropy(result),
        "exact": match_exact_reference(system),
    }


def apply_define_style(st) -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1.4rem;
            max-width: 1060px;
        }
        .tns-center {
            text-align: center;
        }
        .tns-eyebrow {
            color: #6c7480;
            font-size: 0.78rem;
            letter-spacing: 0;
            margin-bottom: 0.1rem;
        }
        .tns-title {
            color: #242832;
            font-size: 1.8rem;
            font-weight: 680;
            margin-bottom: 0.1rem;
        }
        .tns-subtle {
            color: #6c7480;
            font-size: 0.9rem;
        }
        .tns-rule {
            border-top: 1px solid rgba(49, 51, 63, 0.12);
            margin: 1.05rem 0 0.85rem;
        }
        .tns-section-heading {
            margin: 1.1rem 0 0.55rem;
        }
        .tns-section-heading h2 {
            color: #262b33;
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.25;
            margin: 0;
        }
        .tns-section-heading p {
            color: #69717d;
            font-size: 0.86rem;
            line-height: 1.45;
            margin: 0.16rem 0 0;
        }
        .tns-stat-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.65rem;
            margin: 1rem auto 0.75rem;
        }
        .tns-stat {
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 8px;
            background: #ffffff;
            padding: 0.65rem 0.8rem;
            text-align: center;
        }
        .tns-stat-label {
            color: #747b86;
            font-size: 0.72rem;
            margin-bottom: 0.12rem;
        }
        .tns-stat-value {
            color: #272b34;
            font-size: 1.15rem;
            font-weight: 650;
            line-height: 1.2;
        }
        .tns-pane {
            border: 1px solid rgba(49, 51, 63, 0.13);
            border-radius: 8px;
            background: #ffffff;
            padding: 0.95rem 1rem;
            min-height: 132px;
        }
        .tns-pane h3 {
            color: #2b3038;
            font-size: 1.05rem;
            line-height: 1.25;
            margin: 0 0 0.45rem;
        }
        .tns-pane p {
            color: #555d68;
            font-size: 0.92rem;
            line-height: 1.55;
            margin-bottom: 0;
        }
        .tns-param-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.45rem;
            margin-top: 0.65rem;
        }
        .tns-param {
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 999px;
            color: #3d4652;
            background: #f7f8fa;
            font-size: 0.78rem;
            line-height: 1;
            padding: 0.42rem 0.58rem;
        }
        .tns-section-label {
            text-align: center;
            color: #5f6673;
            font-size: 0.78rem;
            margin: 0.2rem 0 0.55rem;
        }
        .tns-radio-note {
            text-align: center;
            color: #747b86;
            font-size: 0.78rem;
            margin-bottom: -0.3rem;
        }
        div[role="radiogroup"] {
            justify-content: center;
            gap: 0.25rem;
        }
        div[role="radiogroup"] label {
            border: 1px solid rgba(49, 51, 63, 0.14);
            border-radius: 999px;
            background: #fff;
            padding: 0.28rem 0.72rem 0.28rem 0.45rem;
            margin-right: 0 !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stExpander"]) {
            margin-top: -0.35rem;
        }
        .stDataFrame {
            border-radius: 8px;
            overflow: hidden;
        }
        @media (max-width: 760px) {
            .tns-stat-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
            .tns-title {
                font-size: 1.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def term_rows(system, selected: str = "Full"):
    allowed = TERM_LABEL_MAP.get(selected)
    return [
        {
            "label": term.label,
            "coefficient": float(np.real_if_close(term.coefficient)),
            "support": "-".join(str(site) for site in term.support()),
            "operators": " ".join(f"{op.name}@{op.site}" for op in term.operators),
        }
        for term in system.terms
        if allowed is None or term.label in allowed
    ]


def term_detail(selected: str) -> dict[str, str]:
    return TERM_COPY[selected]


def _cluster_supports_for_plot(system):
    if system.bc == "periodic":
        return tuple(((center - 1) % system.length, center, (center + 1) % system.length) for center in range(system.length))
    return tuple((center - 1, center, center + 1) for center in range(1, system.length - 1))


def plot_chain(system, selected: str = "Full"):
    fig, ax = plt.subplots(figsize=(7.2, 1.85))
    x = np.arange(system.length)
    y = np.zeros(system.length)
    ax.scatter(x, y, s=285, color="#f7f3ec", edgecolor="#282b30", linewidth=1.25, zorder=3)
    for site in system.sites:
        ax.text(site.index, 0.0, str(site.index), ha="center", va="center", fontsize=9, zorder=4)

    show_xxz = selected in {"Full", "XXZ"}
    show_cluster = selected in {"Full", "Cluster"}
    show_zeeman = selected in {"Full", "Zeeman"}

    for bond in system.bonds:
        i, j = bond.as_tuple()
        color = "#2f6f91" if show_xxz else "#c8ced6"
        alpha = 1.0 if show_xxz else 0.45
        if bond.boundary:
            xs = np.linspace(i, system.length - 1 + 0.7, 30)
            ax.plot(xs, 0.22 * np.sin(np.linspace(0, np.pi, 30)), color=color, lw=1.8, ls="--", alpha=alpha)
            xs = np.linspace(-0.7, j, 30)
            ax.plot(xs, 0.22 * np.sin(np.linspace(np.pi, 0, 30)), color=color, lw=1.8, ls="--", alpha=alpha)
        else:
            ax.plot([i, j], [0, 0], color=color, lw=2.6, solid_capstyle="round", alpha=alpha, zorder=1)

    cluster_terms = [term.support() for term in system.terms if term.label == "cluster"]
    if selected == "Cluster" and not cluster_terms:
        cluster_terms = list(_cluster_supports_for_plot(system))
    for left, center, right in cluster_terms:
        if not show_cluster:
            continue
        if left < right:
            xs = np.linspace(left, right, 80)
            center_x = 0.5 * (left + right)
            width = max(right - left, 1)
            ys = 0.34 * (1 - ((xs - center_x) / (0.5 * width)) ** 2)
            ax.plot(xs, ys, color="#7b3f8c", lw=1.9, zorder=2)
        else:
            ax.text(center, 0.48, "cluster", color="#7b3f8c", ha="center", fontsize=8)

    hz = float(system.metadata.get("hz", 0.0))
    hx = float(system.metadata.get("hx", 0.0))
    if show_zeeman and (abs(hz) > 1e-12 or abs(hx) > 1e-12):
        for site in system.sites:
            dx = 0.0 if abs(hx) < 1e-12 else 0.18 * np.sign(hx)
            dy = 0.0 if abs(hz) < 1e-12 else 0.34 * np.sign(hz)
            ax.arrow(site.index, -0.42, dx, dy, head_width=0.07, head_length=0.07, color="#b45f06", length_includes_head=True)

    ax.set_xlim(-0.8, system.length - 0.2)
    ax.set_ylim(-0.52, 0.58)
    ax.set_axis_off()
    fig.tight_layout()
    return fig


def plot_spin_vectors(rows, eps=1e-3):
    fig, ax = plt.subplots(figsize=(8.0, 2.6))
    x = np.array([row["site"] for row in rows], dtype=float)
    ax.scatter(x, np.zeros_like(x), s=260, color="#f6f1e8", edgecolor="#222222", linewidth=1.2)
    for row in rows:
        if row["norm"] < eps:
            continue
        ax.arrow(
            row["site"],
            0.0,
            0.5 * row["Sx"],
            0.85 * row["Sz"],
            head_width=0.07,
            head_length=0.08,
            color="#2c7a57",
            length_includes_head=True,
        )
    ax.axhline(0, color="#9a9a9a", lw=0.8)
    ax.set_xlim(-0.8, len(rows) - 0.2)
    ax.set_ylim(-0.6, 0.6)
    ax.set_xlabel("site")
    ax.set_ylabel("spin")
    fig.tight_layout()
    return fig


def method_form_summary(system):
    form = change_form(system, ED)
    return {
        "status": form.status,
        "consumed": ", ".join(form.consumed),
        "required_extra": ", ".join(form.required_extra) if form.required_extra else "none",
        "payload_keys": ", ".join(form.payload.keys()),
        "matrix_terms": len(form.payload["matrix_terms"]),
        "hilbert_dim": form.payload["basis"]["dimension"],
    }
