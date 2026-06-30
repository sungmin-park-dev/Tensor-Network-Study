"""Project-local method-consumption probe for 1D spin systems."""

from .method_form import ED, NQS, TN, Method, MethodForm, QuadHam, change_form
from .exact_references import match_exact_reference
from .observables import connected_correlator_matrix, half_chain_entropy, site_expectations, spin_vectors
from .results import ExactReference, SolverResult
from .solvers.ed import hamiltonian_matrix_from_form, solve_ed
from .spin_models import build_spin_chain, build_xxz_chain
from .spin_system import (
    Bond,
    HamiltonianTerm,
    LocalHilbertSpace,
    OperatorOnSite,
    Site,
    SpinSystem,
    spin_half_space,
)

__all__ = [
    "Bond",
    "ED",
    "HamiltonianTerm",
    "ExactReference",
    "LocalHilbertSpace",
    "Method",
    "MethodForm",
    "NQS",
    "OperatorOnSite",
    "QuadHam",
    "Site",
    "SpinSystem",
    "SolverResult",
    "TN",
    "build_spin_chain",
    "build_xxz_chain",
    "change_form",
    "connected_correlator_matrix",
    "half_chain_entropy",
    "hamiltonian_matrix_from_form",
    "match_exact_reference",
    "site_expectations",
    "solve_ed",
    "spin_half_space",
    "spin_vectors",
]
