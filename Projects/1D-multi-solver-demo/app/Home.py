from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_ROOT = Path(__file__).resolve().parent
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from ui_support import ensure_defaults

st.set_page_config(page_title="1D Solver", layout="wide")
ensure_defaults(st)

st.title("1D Multi-Solver Demo")

left, right = st.columns([1.05, 1.0])

with left:
    st.subheader("Project")
    st.markdown(
        """
        Project-local ED app for the 1D spin-chain family used in the TNS
        multi-method seam probe.

        The source definition stays as `SpinSystem`; method-specific payloads
        are generated through `change_form(system, method)`.
        """
    )

    st.subheader("Scope")
    st.markdown(
        """
        - System family: configurable 1D spin-chain model
        - Current backend: ED ground-state solve
        - Current UI surface: Define, MethodForm, Solve, Observables
        - Project boundary: no `code-space/` promotion in this slice
        """
    )

with right:
    st.subheader("Current Implementation")
    st.markdown(
        """
        - General spin-chain builder with open and periodic boundaries
        - Cluster OBC convention: bulk-center terms only
        - Sparse Hamiltonian assembly from the ED `MethodForm`
        - Energy, site magnetization, connected correlator, and half-chain entropy
        - Exact overlay for finite PBC XXZ and pure cluster stabilizer limits
        """
    )

    st.subheader("Planned Implementation")
    st.markdown(
        """
        - TN/DMRG backend connection
        - NQS backend connection
        - Method comparison report layer
        - Time-evolution and dynamics visualizations
        - Reusable toolbox extraction after project-local validation
        """
    )
