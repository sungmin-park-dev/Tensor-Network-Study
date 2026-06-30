from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ui_support import ensure_defaults, solve_current

st.set_page_config(page_title="Observables", layout="wide")
ensure_defaults(st)

if "result" not in st.session_state:
    if st.button("Run ED", type="primary"):
        solve_current(st)

result = st.session_state.get("result")
if not result:
    st.info("ED result is not available yet.")
    st.stop()

observables = st.session_state["observables"]

st.header("Observables")

exact = observables["exact"]
cols = st.columns(3)
cols[0].metric("E0", f"{result.energy:.12g}")
cols[1].metric("S half", f"{observables['half_chain_entropy']:.8g}")
if exact:
    cols[2].metric("Exact diff", f"{exact.deviation(result):.3e}", help=exact.label)
else:
    cols[2].metric("Exact", "none")

st.subheader("Site Sz")
st.bar_chart(pd.DataFrame(observables["site_sz"]).set_index("site"))

st.subheader("Connected Sz Correlator")
corr = observables["connected_sz"]
st.dataframe(
    pd.DataFrame(corr, index=[f"i={i}" for i in range(corr.shape[0])], columns=[f"j={j}" for j in range(corr.shape[1])]),
    width="stretch",
)

if exact:
    st.subheader("Exact Reference")
    st.dataframe(
        pd.DataFrame(
            [
                {"field": "label", "value": exact.label},
                {"field": "source", "value": exact.source},
                {"field": "energy", "value": exact.energy},
                {"field": "energy_per_site", "value": exact.energy_per_site},
                {"field": "notes", "value": " ".join(exact.notes)},
            ]
        ),
        width="stretch",
        hide_index=True,
    )
