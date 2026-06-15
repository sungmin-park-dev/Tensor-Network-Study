"""Method-specific forms exported from a shared SpinSystem."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np

from .spin_system import HamiltonianTerm, SpinSystem


@dataclass(frozen=True)
class Method:
    """Selector for a solver-family input form."""

    name: str
    label: str


ED = Method("ed", "ED")
TN = Method("tn", "TN")
NQS = Method("nqs", "NQS")
QuadHam = Method("quad_ham", "QuadHam")


@dataclass(frozen=True)
class MethodForm:
    """A method-facing form plus the trace of what it consumed."""

    method: str
    status: str
    payload: dict[str, Any]
    consumed: tuple[str, ...]
    required_extra: tuple[str, ...] = ()
    dropped: tuple[str, ...] = ()
    notes: tuple[str, ...] = field(default_factory=tuple)


def change_form(system: SpinSystem, method: Method) -> MethodForm:
    """Export one SpinSystem into the requested method-specific form."""

    if method == ED:
        return _ed_form(system)
    if method == TN:
        return _tn_form(system)
    if method == NQS:
        return _nqs_form(system)
    if method == QuadHam:
        return _quad_ham_form(system)
    raise ValueError(f"Unknown method selector: {method!r}")


def _coefficient(value: complex) -> float | complex:
    if abs(value.imag) < 1e-15:
        return float(value.real)
    return value


def _term_record(term: HamiltonianTerm) -> dict[str, Any]:
    return {
        "label": term.label,
        "coefficient": _coefficient(term.coefficient),
        "support": term.support(),
        "operators": tuple(
            {"name": operator.name, "site": operator.site} for operator in term.operators
        ),
    }


def _ed_form(system: SpinSystem) -> MethodForm:
    return MethodForm(
        method=ED.name,
        status="ready",
        payload={
            "basis": {
                "type": "product",
                "local_dimension": system.local_space.dimension,
                "n_sites": system.length,
                "dimension": system.local_space.dimension ** system.length,
                "ordering": "binary_site_order",
            },
            "local_operator_matrices": dict(system.local_space.operators),
            "matrix_terms": tuple(_term_record(term) for term in system.terms),
            "bc": system.bc,
        },
        consumed=(
            "local_space.dimension",
            "local_space.operators",
            "sites",
            "terms",
            "bc",
        ),
        notes=("ED consumes explicit local matrices and a many-body basis ordering.",),
    )


def _tn_form(system: SpinSystem) -> MethodForm:
    return MethodForm(
        method=TN.name,
        status="ready",
        payload={
            "site_type": system.local_space.name,
            "operator_names": system.local_space.operator_names(),
            "bonds": tuple(
                {
                    "sites": bond.as_tuple(),
                    "kind": bond.kind,
                    "boundary": bond.boundary,
                }
                for bond in system.bonds
            ),
            "mpo_terms": tuple(_term_record(term) for term in system.terms),
            "bc": system.bc,
        },
        consumed=(
            "local_space.name",
            "local_space.operator_names",
            "bonds",
            "terms",
            "bc",
        ),
        required_extra=("backend_site_class", "mpo_builder_policy"),
        notes=(
            "TN/DMRG prefers named local operators and MPO-friendly local terms.",
            "PBC is a solver-cost seam, not just a geometry flag.",
        ),
    )


def _nqs_form(system: SpinSystem) -> MethodForm:
    return MethodForm(
        method=NQS.name,
        status="ready",
        payload={
            "graph": {
                "nodes": tuple(site.index for site in system.sites),
                "edges": system.bond_tuples(),
                "bc": system.bc,
            },
            "hilbert": {
                "local_states": system.local_space.basis,
                "n_sites": system.length,
            },
            "local_operator_terms": tuple(_term_record(term) for term in system.terms),
        },
        consumed=(
            "local_space.basis",
            "sites",
            "bonds",
            "terms",
            "bc",
        ),
        required_extra=("ansatz", "sampler", "random_seed"),
        notes=("NQS consumes a graph/Hilbert/operator split plus stochastic run metadata.",),
    )


def _quad_ham_form(system: SpinSystem) -> MethodForm:
    jxy = float(system.metadata.get("jxy", 0.0))
    jz = float(system.metadata.get("jz", 0.0))
    hz = float(system.metadata.get("hz", 0.0))
    hx = float(system.metadata.get("hx", 0.0))

    unsupported = []
    if system.metadata.get("model_family") != "xxz":
        unsupported.append("model_family")
    if abs(jz) > 1e-15:
        unsupported.append("jz_interaction")
    if abs(hz) > 1e-15:
        unsupported.append("longitudinal_field")
    if abs(hx) > 1e-15:
        unsupported.append("transverse_field")

    if unsupported:
        return MethodForm(
            method=QuadHam.name,
            status="not_applicable",
            payload={
                "kind": "quadratic_hamiltonian",
                "reason": "The current probe only exports the XX free-fermion limit.",
                "unsupported_features": tuple(unsupported),
            },
            consumed=("metadata", "terms"),
            required_extra=("noninteracting_or_jw_quadratic_mapping",),
            notes=("Interacting spin terms cannot be exported as a quadratic Hamiltonian.",),
        )

    hopping = np.zeros((system.length, system.length), dtype=complex)
    boundary_terms = []
    for bond in system.bonds:
        i, j = bond.as_tuple()
        amplitude = 0.5 * jxy
        if bond.boundary and system.bc == "periodic":
            boundary_terms.append(
                {
                    "sites": bond.as_tuple(),
                    "spin_amplitude": amplitude,
                    "fermion_amplitude": "-Pi * Jxy / 2 after JW sector choice",
                }
            )
            continue
        hopping[i, j] += amplitude
        hopping[j, i] += amplitude

    required_extra = ()
    status = "ready"
    notes = ["QuadHam consumes the free-fermion hopping form, not the full spin basis."]
    if boundary_terms:
        required_extra = ("fermion_parity_sector",)
        status = "partial"
        notes.append("Periodic spin boundary requires a JW fermion-parity sector.")

    return MethodForm(
        method=QuadHam.name,
        status=status,
        payload={
            "kind": "number_conserving_quadratic",
            "hopping_matrix": hopping,
            "pairing_matrix": None,
            "constant": 0.0,
            "boundary_terms": tuple(boundary_terms),
            "bc": system.bc,
        },
        consumed=("bonds", "metadata.jxy", "metadata.jz", "metadata.hz", "metadata.hx", "bc"),
        required_extra=required_extra,
        dropped=("many_body_basis", "named_spin_operator_mpo_terms"),
        notes=tuple(notes),
    )

