"""
Tests for the NQS solver (NetKet-based).

Requires: pip install netket
Tests are skipped automatically if NetKet is not installed.
"""

import numpy as np
import pytest

# Skip entire module if NetKet is not installed
nk = pytest.importorskip("netket")

from cluster_ising.solvers.nqs_solver import (
    build_netket_hamiltonian, run_nqs, HAS_NETKET,
)
from cluster_ising.models.exact_solution import build_hamiltonian_matrix


class TestBuildHamiltonian:
    """Test NetKet Hamiltonian construction against ED."""

    @pytest.mark.parametrize("lam", [0.5, 1.0, 2.0])
    def test_eigenvalues_match_ed_obc(self, lam):
        """NetKet Hamiltonian eigenvalues match ED for L=6 OBC."""
        L = 6
        model_params = {'L': L, 'lam': lam, 'bc': 'open'}

        hi, H_nk, graph = build_netket_hamiltonian(model_params)
        H_nk_dense = H_nk.to_dense()

        H_ed = build_hamiltonian_matrix(lam, L, bc='open')

        # Compare eigenvalue spectra (basis ordering may differ)
        evals_nk = np.sort(np.linalg.eigvalsh(H_nk_dense.real))
        evals_ed = np.sort(np.linalg.eigvalsh(H_ed.real))
        np.testing.assert_allclose(evals_nk, evals_ed, atol=1e-10)

    @pytest.mark.parametrize("lam", [0.5, 1.0, 2.0])
    def test_eigenvalues_match_ed_pbc(self, lam):
        """NetKet Hamiltonian eigenvalues match ED for L=6 PBC."""
        L = 6
        model_params = {'L': L, 'lam': lam, 'bc': 'periodic'}

        hi, H_nk, graph = build_netket_hamiltonian(model_params)
        H_nk_dense = H_nk.to_dense()

        H_ed = build_hamiltonian_matrix(lam, L, bc='periodic')

        evals_nk = np.sort(np.linalg.eigvalsh(H_nk_dense.real))
        evals_ed = np.sort(np.linalg.eigvalsh(H_ed.real))
        np.testing.assert_allclose(evals_nk, evals_ed, atol=1e-10)

    @pytest.mark.parametrize("bc", ['open', 'periodic'])
    def test_hamiltonian_hermitian(self, bc):
        """NetKet Hamiltonian is Hermitian."""
        model_params = {'L': 6, 'lam': 1.0, 'bc': bc}
        hi, H_nk, graph = build_netket_hamiltonian(model_params)
        H_dense = H_nk.to_dense()
        assert np.allclose(H_dense, H_dense.conj().T, atol=1e-12)

    def test_ground_energy_lambda_zero(self):
        """At λ=0, E₀/L = -1 (pure cluster state)."""
        L = 6
        model_params = {'L': L, 'lam': 0.0, 'bc': 'periodic'}
        hi, H_nk, graph = build_netket_hamiltonian(model_params)
        H_dense = H_nk.to_dense()
        evals = np.sort(np.linalg.eigvalsh(H_dense.real))
        E0_per_site = evals[0] / L
        assert abs(E0_per_site - (-1.0)) < 1e-10

    def test_dimension(self):
        """Hamiltonian has correct dimension 2^L."""
        L = 8
        model_params = {'L': L, 'lam': 1.0, 'bc': 'open'}
        hi, H_nk, graph = build_netket_hamiltonian(model_params)
        H_dense = H_nk.to_dense()
        assert H_dense.shape == (2**L, 2**L)

    def test_min_system_size(self):
        """Raise ValueError for L < 3."""
        with pytest.raises(ValueError, match="L must be >= 3"):
            build_netket_hamiltonian({'L': 2, 'lam': 1.0})


class TestRunNQS:
    """Test the full NQS VMC optimization."""

    @pytest.mark.slow
    def test_nqs_energy_small_system(self):
        """NQS energy matches ED within tolerance for L=6 OBC."""
        model_params = {'L': 6, 'lam': 0.5, 'bc': 'open'}
        nqs_params = {
            'ansatz': 'RBM',
            'alpha': 2,
            'n_samples': 2048,
            'n_iter': 500,
            'learning_rate': 0.02,
            'diag_shift': 0.01,
            'seed': 42,
        }
        result = run_nqs(model_params, nqs_params)

        # Compare with ED
        H_ed = build_hamiltonian_matrix(0.5, 6, bc='open')
        evals = np.sort(np.linalg.eigvalsh(H_ed.real))
        E_exact = evals[0]

        assert result.solver_name == 'NQS'
        assert result.state_type == 'nqs'
        assert result.num_sites == 6
        # VMC with SGD+SR should get within 2% of exact for this small system
        rel_err = abs(result.energy - E_exact) / abs(E_exact)
        assert rel_err < 0.02, (
            f"NQS energy {result.energy:.6f} too far from exact {E_exact:.6f} "
            f"(rel_err={rel_err:.4f})"
        )

    @pytest.mark.slow
    def test_nqs_metadata(self):
        """SolverResult metadata has expected fields."""
        model_params = {'L': 4, 'lam': 0.5, 'bc': 'open'}
        nqs_params = {
            'ansatz': 'RBM', 'alpha': 1,
            'n_samples': 256, 'n_iter': 50,
            'seed': 0,
        }
        result = run_nqs(model_params, nqs_params)

        assert 'wall_time' in result.metadata
        assert 'energy_history' in result.metadata
        assert 'variance_history' in result.metadata
        assert 'ansatz' in result.metadata
        assert len(result.metadata['energy_history']) == 50
