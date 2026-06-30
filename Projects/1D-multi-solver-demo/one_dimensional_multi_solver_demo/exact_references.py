"""Exact-reference overlays for the first ED UI slice."""

from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np

from .results import ExactReference
from .spin_system import SpinSystem


def _near_zero(value: float, tol: float = 1e-12) -> bool:
    return abs(float(value)) < tol


def _load_bethe_ground_energy():
    project_root = Path(__file__).resolve().parents[1]
    module_path = project_root / "verify_xxz_bethe.py"
    spec = importlib.util.spec_from_file_location("_tns_verify_xxz_bethe", module_path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.bethe_ground_energy


def _cluster_term_count(system: SpinSystem) -> int:
    return sum(1 for term in system.terms if term.label == "cluster")


def match_exact_reference(system: SpinSystem) -> ExactReference | None:
    """Return an exact reference when the current parameters hit a known limit."""

    params = system.metadata
    jxy = float(params.get("jxy", 0.0))
    jz = float(params.get("jz", 0.0))
    k = float(params.get("cluster_coupling", 0.0))
    hz = float(params.get("hz", 0.0))
    hx = float(params.get("hx", 0.0))

    if not _near_zero(k) and all(_near_zero(value) for value in (jxy, jz, hz, hx)):
        n_terms = _cluster_term_count(system)
        energy = -abs(k) * n_terms / 8.0
        return ExactReference(
            label="Pure cluster stabilizer limit",
            energy=energy,
            energy_per_site=energy / system.length,
            source="Models/1d-spin-chains/model-hamiltonian.md",
            notes=("Spin convention S=sigma/2, so each three-site stabilizer has magnitude 1/8.",),
        )

    if system.bc == "periodic" and system.length % 2 == 0 and _near_zero(k) and _near_zero(hz) and _near_zero(hx) and not _near_zero(jxy):
        delta = jz / jxy
        if -1e-12 <= delta <= 1.0 + 1e-12:
            bethe_ground_energy = _load_bethe_ground_energy()
            if bethe_ground_energy is None:
                return None
            energy = float(bethe_ground_energy(system.length, float(np.clip(delta, 0.0, 1.0)), jxy=jxy))
            if np.isnan(energy):
                return None
            return ExactReference(
                label="Finite PBC XXZ Bethe reference",
                energy=energy,
                energy_per_site=energy / system.length,
                source="Projects/1D-multi-solver-demo/verify_xxz_bethe.py",
                notes=("Matched for K=0, hx=hz=0, even L, and 0 <= Delta <= 1.",),
            )

    return None
