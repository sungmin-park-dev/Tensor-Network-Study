"""
Unified solver result interface for cross-method benchmarking.

All solvers (ED, DMRG, TDVP, NQS) return SolverResult objects
with a common interface for measuring observables.
"""

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class SolverResult:
    """
    Unified result container for all solvers.

    Attributes
    ----------
    solver_name : str
        Solver identifier ('ED', 'DMRG', 'Exact', 'NQS', etc.).
    energy : float
        Ground-state energy (total).
    energy_per_site : float
        Energy per site.
    state : Any
        Quantum state in solver-native format:
        - ED: ndarray (state vector)
        - DMRG: tenpy MPS object
        - NQS: variational parameters (future)
    state_type : str
        'vector' (ED), 'mps' (DMRG/TDVP), 'nqs' (future).
    num_sites : int
        System size L.
    model_params : dict
        Parameters used for reproducibility.
    metadata : dict
        Solver-specific info (chi, sweeps, wall_time, etc.).
    """
    solver_name: str
    energy: float
    energy_per_site: float
    state: Any
    state_type: str
    num_sites: int
    model_params: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)


class Timer:
    """Simple context manager for timing solver runs."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.elapsed = time.perf_counter() - self.start
