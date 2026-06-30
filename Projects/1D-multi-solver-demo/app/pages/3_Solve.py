from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ui_support import ensure_defaults, plot_spin_vectors, solve_current

st.set_page_config(page_title="Solve", layout="wide")
ensure_defaults(st)

st.header("Solve")

if st.button("Run ED", type="primary"):
    solve_current(st)

result = st.session_state.get("result")
if result:
    cols = st.columns(4)
    cols[0].metric("E0", f"{result.energy:.12g}")
    cols[1].metric("E0 / L", f"{result.energy_per_site:.12g}")
    cols[2].metric("Wall time", f"{result.metadata['wall_time']:.4f}s")
    cols[3].metric("Hilbert dim", result.metadata["hilbert_dim"])

    vectors = st.session_state["observables"]["spin_vectors"]
    st.pyplot(plot_spin_vectors(vectors), clear_figure=True)
    st.dataframe(pd.DataFrame(vectors), width="stretch", hide_index=True)
else:
    st.info("ED result is not available yet.")
