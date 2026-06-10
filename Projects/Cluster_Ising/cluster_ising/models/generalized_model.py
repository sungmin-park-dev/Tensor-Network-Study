"""
Generalized Cluster-Ising-XXZ-Zeeman Model for TeNPy.

H = -J_c Σ σ^x_{j-1} σ^z_j σ^x_{j+1}              (Cluster, 3-body)
  + J_xxz Σ (σ^x σ^x + σ^y σ^y + Δ σ^z σ^z)        (XXZ)
  + J_I Σ σ^y_j σ^y_{j+1}                            (Ising-like)
  + hz Σ σ^z_j                                        (Zeeman)

Supports time-dependent hz(t) for dynamics (Phase 2).
"""

import numpy as np
from tenpy.models.model import CouplingMPOModel
from tenpy.networks.site import SpinHalfSite


class GeneralizedClusterModel(CouplingMPOModel):
    r"""
    Generalized Cluster + XXZ + Ising + Zeeman model on a 1D chain.

    Parameters
    ----------
    model_params : dict
        - L : int, number of sites
        - J_c : float, cluster interaction (default 1.0)
        - J_xxz : float, XXZ exchange (default 0.0)
        - Delta : float, XXZ anisotropy (default 0.0)
        - J_I : float or 'lam', Ising σ^y σ^y coupling
        - lam : float, alternative name for Ising coupling (default 1.0)
        - hz : float, Zeeman field (default 0.0)
        - bc_MPS : 'finite' or 'infinite'
        - bc : 'open' or 'periodic'
        - conserve : 'parity' or 'None'
    """

    default_lattice = 'Chain'
    force_default_lattice = True

    def init_sites(self, model_params):
        conserve = model_params.get('conserve', 'parity', str)
        if conserve == 'None':
            conserve = None
        return SpinHalfSite(conserve=conserve)

    def init_terms(self, model_params):
        J_c = model_params.get('J_c', 1.0, 'real_or_array')
        J_xxz = model_params.get('J_xxz', 0.0, 'real_or_array')
        Delta = model_params.get('Delta', 0.0, 'real_or_array')
        lam = model_params.get('lam', 1.0, 'real_or_array')
        J_I = model_params.get('J_I', 0.0, 'real_or_array')
        hz = model_params.get('hz', 0.0, 'real_or_array')

        # --- Three-body cluster term: -J_c σ^x σ^z σ^x ---
        if J_c != 0:
            self.add_multi_coupling(-J_c, [
                ('Sigmax', [0], 0),
                ('Sigmaz', [1], 0),
                ('Sigmax', [2], 0),
            ])

        # --- Ising term: λ σ^y σ^y (from paper) ---
        if lam != 0:
            for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
                self.add_coupling(lam, u1, 'Sigmay', u2, 'Sigmay', dx)

        # --- XXZ: J_xxz (σ^x σ^x + σ^y σ^y + Δ σ^z σ^z) ---
        if J_xxz != 0:
            for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
                self.add_coupling(J_xxz, u1, 'Sigmax', u2, 'Sigmax', dx)
                self.add_coupling(J_xxz, u1, 'Sigmay', u2, 'Sigmay', dx)
                self.add_coupling(J_xxz * Delta, u1, 'Sigmaz', u2, 'Sigmaz', dx)

        # --- Extra Ising: J_I σ^y σ^y ---
        if J_I != 0:
            for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
                self.add_coupling(J_I, u1, 'Sigmay', u2, 'Sigmay', dx)

        # --- Zeeman: hz σ^z ---
        if hz != 0:
            for u in range(len(self.lat.unit_cell)):
                self.add_onsite(hz, u, 'Sigmaz')


# ---------------------------------------------------------------------------
# Time-dependent magnetic field profiles
# ---------------------------------------------------------------------------

def quench_field(t, h0, t_quench=0.0):
    """Step function quench: h(t) = h0 for t ≥ t_quench."""
    return h0 if t >= t_quench else 0.0


def ramp_field(t, h0, tau):
    """Linear ramp: h(t) = h0 * min(t/tau, 1)."""
    return h0 * min(t / tau, 1.0)


def periodic_field(t, h0, omega, phase=0.0):
    """Periodic driving: h(t) = h0 * cos(ωt + φ)."""
    return h0 * np.cos(omega * t + phase)


def gaussian_pulse(t, h0, t0, sigma):
    """Gaussian pulse: h(t) = h0 * exp(-(t-t0)²/(2σ²))."""
    return h0 * np.exp(-0.5 * ((t - t0) / sigma)**2)
