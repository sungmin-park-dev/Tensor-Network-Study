from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

APP_ROOT = Path(__file__).resolve().parents[1]
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ui_support import ensure_defaults, method_form_summary

st.set_page_config(page_title="MethodForm", layout="wide")
ensure_defaults(st)

system = st.session_state["system"]
summary = method_form_summary(system)

st.header("ED MethodForm")

cols = st.columns(4)
cols[0].metric("Status", summary["status"])
cols[1].metric("Hilbert dim", summary["hilbert_dim"])
cols[2].metric("Matrix terms", summary["matrix_terms"])
cols[3].metric("Extra", summary["required_extra"])

st.dataframe(
    pd.DataFrame(
        [
            {"field": "consumed", "value": summary["consumed"]},
            {"field": "payload_keys", "value": summary["payload_keys"]},
        ]
    ),
    width="stretch",
    hide_index=True,
)
