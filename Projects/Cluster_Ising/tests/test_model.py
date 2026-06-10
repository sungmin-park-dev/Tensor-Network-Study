"""Tests for the TeNPy Cluster-Ising Model."""

import numpy as np
import pytest

# Only run if TeNPy is installed
tenpy = pytest.importorskip("tenpy")

from cluster_ising.models.cluster_ising_model import ClusterIsingModel
from cluster_ising.models.generalized_model import GeneralizedClusterModel
from cluster_ising.models.exact_solution import (
    build_hamiltonian_matrix,
    ground_state_energy_density,
)


def mpo_to_matrix(H_mpo):
    """Contract a finite MPO into a dense 2^N x 2^N matrix."""
    N = H_mpo.L
    Ws = [H_mpo.get_W(i).to_ndarray() for i in range(N)]

    # Contract W tensors over bond indices: (wL, wR, p, p*)
    T = Ws[0]
    for i in range(1, N):
        T = np.tensordot(T, Ws[i], axes=([1], [0]))
        # Move new wR (at ndim-3) to position 1
        ndim = T.ndim
        ax_order = [0, ndim - 3] + list(range(1, ndim - 3)) + [ndim - 2, ndim - 1]
        T = T.transpose(ax_order)

    # Apply finite boundary: IdL selects row, IdR selects column
    IdL = H_mpo.get_IdL(0)
    IdR = H_mpo.get_IdR(N - 1)
    H_full = T[IdL, IdR]

    # Rearrange from (p0, p0*, p1, p1*, ...) to matrix (p0 p1 ..., p0* p1* ...)
    d = 2
    dim = d ** N
    bra_indices = list(range(0, 2 * N, 2))
    ket_indices = list(range(1, 2 * N, 2))
    H_full = H_full.transpose(bra_indices + ket_indices)
    return H_full.reshape(dim, dim)


class TestClusterIsingModel:
    """Test the TeNPy model construction."""

    def test_model_creation(self):
        """Model can be created without errors."""
        params = {
            'L': 8,
            'lam': 1.0,
            'J_c': 1.0,
            'bc_MPS': 'finite',
            'conserve': 'None',
        }
        model = ClusterIsingModel(params)
        assert model is not None
        assert model.lat.N_sites == 8

    def test_model_parity_conserve(self):
        """Model works with parity conservation."""
        params = {
            'L': 6,
            'lam': 1.0,
            'bc_MPS': 'finite',
            'conserve': 'parity',
        }
        model = ClusterIsingModel(params)
        assert model is not None

    @pytest.mark.parametrize("lam", [0.5, 1.0, 2.0])
    def test_mpo_vs_ed_energy(self, lam):
        """TeNPy MPO Hamiltonian matches ED for small systems."""
        N = 6
        params = {
            'L': N,
            'lam': lam,
            'J_c': 1.0,
            'bc_MPS': 'finite',
            'conserve': 'None',
        }
        model = ClusterIsingModel(params)

        H_matrix = mpo_to_matrix(model.calc_H_MPO())
        H_ed = build_hamiltonian_matrix(lam, N, bc='open')

        diff = np.max(np.abs(H_matrix - H_ed))
        assert diff < 1e-10, f"MPO vs ED Hamiltonian diff: {diff}"


class TestGeneralizedModel:
    """Test the generalized Hamiltonian model."""

    def test_reduces_to_cim(self):
        """With J_xxz=J_I=hz=0, reduces to standard CIM."""
        N = 6
        lam = 1.5
        params_cim = {
            'L': N,
            'lam': lam,
            'bc_MPS': 'finite',
            'conserve': 'None',
        }
        params_gen = {
            'L': N,
            'lam': lam,
            'J_c': 1.0,
            'J_xxz': 0.0,
            'J_I': 0.0,
            'hz': 0.0,
            'bc_MPS': 'finite',
            'conserve': 'None',
        }

        H_cim = mpo_to_matrix(ClusterIsingModel(params_cim).calc_H_MPO())
        H_gen = mpo_to_matrix(GeneralizedClusterModel(params_gen).calc_H_MPO())

        diff = np.max(np.abs(H_cim - H_gen))
        assert diff < 1e-10, f"Generalized model differs from CIM: {diff}"

    def test_zeeman_field(self):
        """Zeeman field adds diagonal terms."""
        N = 4
        params = {
            'L': N,
            'lam': 0.0,
            'J_c': 0.0,
            'hz': 1.0,
            'bc_MPS': 'finite',
            'conserve': 'None',
        }
        model = GeneralizedClusterModel(params)
        H = mpo_to_matrix(model.calc_H_MPO())

        # Pure Zeeman: H = Σ σ^z_j, eigenvalues are ±N, ±(N-2), ...
        evals = np.sort(np.linalg.eigvalsh(H))
        expected = []
        for bits in range(2**N):
            val = sum(1 - 2 * ((bits >> i) & 1) for i in range(N))
            expected.append(val)
        expected = np.sort(expected)

        assert np.allclose(evals, expected, atol=1e-10)
