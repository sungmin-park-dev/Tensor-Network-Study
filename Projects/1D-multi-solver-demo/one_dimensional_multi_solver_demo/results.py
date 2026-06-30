"""Project-local result records for solver and observable output."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True)
class SolverResult:
    """Common result container for the project-local ED slice."""

    solver_name: str
    energy: float
    energy_per_site: float
    state: np.ndarray
    state_type: str
    num_sites: int
    model_params: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ExactReference:
    """An exact or analytical reference matched to the current parameter limit."""

    label: str
    energy: float
    energy_per_site: float
    source: str
    notes: tuple[str, ...] = ()

    def deviation(self, result: SolverResult) -> float:
        return float(result.energy - self.energy)
