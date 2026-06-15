"""Source-of-truth data structures for a spin system."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

import numpy as np


@dataclass(frozen=True)
class LocalHilbertSpace:
    """Local spin space and operator matrices before method-specific export."""

    name: str
    dimension: int
    basis: tuple[str, ...]
    operators: Mapping[str, np.ndarray]
    convention: str = "spin"

    def operator_names(self) -> tuple[str, ...]:
        return tuple(self.operators.keys())


@dataclass(frozen=True)
class Site:
    """A physical site in the system geometry."""

    index: int
    coordinate: tuple[float, ...]
    label: str = ""


@dataclass(frozen=True)
class Bond:
    """A geometry edge used by Hamiltonian terms and graph-based methods."""

    site_i: int
    site_j: int
    kind: str = "nearest_neighbor"
    boundary: bool = False

    def as_tuple(self) -> tuple[int, int]:
        return (self.site_i, self.site_j)


@dataclass(frozen=True)
class OperatorOnSite:
    """A named local operator acting on one site."""

    name: str
    site: int


@dataclass(frozen=True)
class HamiltonianTerm:
    """One product-operator term in the spin Hamiltonian."""

    label: str
    coefficient: complex
    operators: tuple[OperatorOnSite, ...]
    source: str = "model"

    def support(self) -> tuple[int, ...]:
        return tuple(operator.site for operator in self.operators)

    def operator_names(self) -> tuple[str, ...]:
        return tuple(operator.name for operator in self.operators)


@dataclass(frozen=True)
class SpinSystem:
    """Method-independent definition of a spin model on a fixed geometry."""

    name: str
    local_space: LocalHilbertSpace
    sites: tuple[Site, ...]
    bonds: tuple[Bond, ...]
    terms: tuple[HamiltonianTerm, ...]
    bc: str
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @property
    def length(self) -> int:
        return len(self.sites)

    def bond_tuples(self) -> tuple[tuple[int, int], ...]:
        return tuple(bond.as_tuple() for bond in self.bonds)


def spin_half_space() -> LocalHilbertSpace:
    """Return the default spin-1/2 local Hilbert space with spin operators."""

    sx = 0.5 * np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
    sy = 0.5 * np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
    sz = 0.5 * np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
    sp = np.array([[0.0, 1.0], [0.0, 0.0]], dtype=complex)
    sm = np.array([[0.0, 0.0], [1.0, 0.0]], dtype=complex)
    identity = np.eye(2, dtype=complex)
    return LocalHilbertSpace(
        name="spin_half",
        dimension=2,
        basis=("up", "down"),
        operators={
            "I": identity,
            "Sx": sx,
            "Sy": sy,
            "Sz": sz,
            "Sp": sp,
            "Sm": sm,
        },
        convention="spin",
    )

