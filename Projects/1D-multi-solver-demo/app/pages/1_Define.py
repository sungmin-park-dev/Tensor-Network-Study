from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ui_support import (
    TERM_LABELS,
    apply_define_style,
    ensure_defaults,
    plot_chain,
    term_detail,
    term_rows,
    update_system,
)

st.set_page_config(page_title="Define", layout="wide")
ensure_defaults(st)
apply_define_style(st)

params = dict(st.session_state["params"])

def _format_number(value: float) -> str:
    if abs(value) < 1e-12:
        return "0"
    if float(value).is_integer():
        return str(int(value))
    return f"{value:.3g}"


def _active_count(rows: list[dict[str, object]]) -> str:
    return f"{len(rows)} active terms" if rows else "0 active terms"


def _section_heading(title: str, body: str) -> None:
    st.markdown(
        f"""
        <div class="tns-section-heading">
          <h2>{title}</h2>
          <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <div class="tns-center">
      <div class="tns-eyebrow">Spin-chain source definition</div>
      <div class="tns-title">System Definition</div>
      <div class="tns-subtle">Define the lattice, choose active terms, then pass the same system to ED.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

_section_heading(
    "Geometry",
    "Defines the one-dimensional chain. The local Hilbert space is fixed to spin-1/2 in this demo.",
)
geom_inputs, geom_preview = st.columns([0.42, 0.58], gap="medium")

with geom_inputs:
    with st.container(border=True):
        st.markdown("#### Chain")
        length = st.slider(
            "Sites (L)",
            min_value=2,
            max_value=14,
            value=int(params["length"]),
            step=1,
            help="Number of spin-1/2 sites in the chain.",
        )
        bc = st.radio(
            "Boundary condition",
            ["open", "periodic"],
            index=["open", "periodic"].index(params["bc"]),
            horizontal=True,
            help="Open uses nearest-neighbor bonds inside the chain. Periodic also connects the last site back to the first.",
        )
        st.markdown('<div class="tns-param-row"><span class="tns-param">local spin=1/2</span><span class="tns-param">local dim=2</span></div>', unsafe_allow_html=True)

with geom_preview:
    with st.container(border=True):
        st.markdown("#### Lattice preview")
        preview_slot = st.empty()
        preview_caption_slot = st.empty()
        notation_slot = st.empty()

st.markdown('<div class="tns-rule"></div>', unsafe_allow_html=True)
_section_heading(
    "Hamiltonian",
    "Chooses the active term family and the coupling constants used to build the matrix terms.",
)
ham_inputs, ham_support = st.columns([0.6, 0.4], gap="medium")

with ham_inputs:
    with st.container(border=True):
        st.markdown("#### Terms and parameters")
        selected = st.radio("Hamiltonian term", TERM_LABELS, horizontal=True, key="define_term")
        detail = term_detail(selected)

        coupling_cols = st.columns(3, gap="small")
        with coupling_cols[0]:
            jxy = st.number_input("Jxy", value=float(params["jxy"]), step=0.25, format="%.3f")
        with coupling_cols[1]:
            jz = st.number_input("Jz", value=float(params["jz"]), step=0.25, format="%.3f")
        with coupling_cols[2]:
            k = st.number_input("K", value=float(params["k"]), step=0.25, format="%.3f")

        field_cols = st.columns(2, gap="small")
        with field_cols[0]:
            hz = st.number_input("hz", value=float(params["hz"]), step=0.25, format="%.3f")
        with field_cols[1]:
            hx = st.number_input("hx", value=float(params["hx"]), step=0.25, format="%.3f")

with ham_support:
    with st.container(border=True):
        st.markdown("#### Term support")
        st.write("The selected Hamiltonian determines which supports are highlighted below.")
        if selected == "Cluster":
            st.latex(r"\ell(c)=c-1,\quad r(c)=c+1")
            st.caption("Open boundaries use adjacent sites. Periodic boundaries read neighbors modulo L.")
        elif selected == "Full":
            st.latex(r"H = H_{\mathrm{XXZ}} + H_{\mathrm{cluster}} + H_{\mathrm{Zeeman}}")
        else:
            st.latex(detail["equation"])

new_params = {"length": int(length), "bc": bc, "jxy": jxy, "jz": jz, "k": k, "hz": hz, "hx": hx}
if new_params != params:
    update_system(st, new_params)

system = st.session_state["system"]
rows = term_rows(system, selected)

with preview_slot.container():
    st.pyplot(plot_chain(system, selected), clear_figure=True, width="stretch")
preview_caption_slot.caption(
    "For a 1D chain, geometry is just L plus the boundary condition: open removes the wrap-around bond, periodic adds it."
)
with notation_slot.container():
    with st.expander("Lattice notation", expanded=False):
        st.latex(r"\Lambda_L = \{0,1,\ldots,L-1\}")
        st.latex(r"\mathcal{B}_{L}^{\mathrm{bc}} = \text{nearest-neighbor bond set}")
        if system.bc == "periodic":
            st.latex(r"\mathcal{C}_{L}^{\mathrm{periodic}}=\Lambda_L")
            st.caption("Periodic cluster neighbors are read modulo L.")
        else:
            st.latex(r"\mathcal{C}_{L}^{\mathrm{open}}=\{1,\ldots,L-2\}")

st.markdown('<div class="tns-rule"></div>', unsafe_allow_html=True)
formula_col, detail_col = st.columns([1.22, 0.78], gap="medium")

with formula_col:
    with st.container(border=True):
        st.markdown(f"#### {detail['title']}")
        st.caption("Selected Hamiltonian")
        st.latex(detail["equation"])

with detail_col:
    with st.container(border=True):
        st.markdown(f"#### {_active_count(rows)}")
        st.write(detail["body"])
        st.markdown(
            f"""
            <div class="tns-param-row">
              <span class="tns-param">Jxy={_format_number(float(new_params["jxy"]))}</span>
              <span class="tns-param">Jz={_format_number(float(new_params["jz"]))}</span>
              <span class="tns-param">K={_format_number(float(new_params["k"]))}</span>
              <span class="tns-param">hz={_format_number(float(new_params["hz"]))}</span>
              <span class="tns-param">hx={_format_number(float(new_params["hx"]))}</span>
              <span class="tns-param">dim={2 ** system.length}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

with st.expander(f"Matrix terms ({len(rows)})", expanded=False):
    if rows:
        st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)
    else:
        st.info("No active matrix terms for this Hamiltonian under the current parameter values.")
