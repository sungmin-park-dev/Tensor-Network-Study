"""
TeNPy Model for the Cluster-Ising Hamiltonian.

Reference: PhysRevA.84.022304

H(λ) = -J_c Σ σ^x_{j-1} σ^z_j σ^x_{j+1} + λ Σ σ^y_j σ^y_{j+1}

Uses CouplingMPOModel with SpinHalfSite(conserve='parity').
The three-body cluster term is added via add_multi_coupling().
TEBD is NOT compatible (3-body term); use DMRG or TDVP.
"""

import numpy as np
from tenpy.models.model import CouplingMPOModel
from tenpy.networks.site import SpinHalfSite


class ClusterIsingModel(CouplingMPOModel):
    r"""
    Cluster-Ising Model on a 1D chain.

    H = -J_c Σ_j σ^x_{j-1} σ^z_j σ^x_{j+1}  +  λ Σ_j σ^y_j σ^y_{j+1}

    Parameters
    ----------
    model_params : dict | tenpy.tools.params.Config
        Model parameters:
        - L : int
            Number of sites.
        - J_c : float
            Cluster interaction strength (default 1.0).
        - lam : float
            Ising coupling λ (default 1.0).
        - bc_MPS : str
            MPS boundary condition: 'finite' or 'infinite'.
        - bc : str
            Lattice boundary condition: 'open' or 'periodic'.
        - conserve : str
            Conserved quantity: 'parity', 'None', or None.
    """

    default_lattice = 'Chain'
    force_default_lattice = True

    def init_sites(self, model_params):
        conserve = model_params.get('conserve', 'parity', str)
        if conserve == 'None':
            conserve = None
        site = SpinHalfSite(conserve=conserve)
        return site

    def init_terms(self, model_params):
        J_c = model_params.get('J_c', 1.0, 'real_or_array')
        lam = model_params.get('lam', 1.0, 'real_or_array')

        # --- Three-body cluster term: -J_c σ^x_{j} σ^z_{j+1} σ^x_{j+2} ---
        # add_multi_coupling sums over all j, with operators at relative
        # positions [0], [1], [2] from the reference site.
        self.add_multi_coupling(-J_c, [
            ('Sigmax', [0], 0),
            ('Sigmaz', [1], 0),
            ('Sigmax', [2], 0),
        ])

        # --- Two-body Ising term: λ σ^y_j σ^y_{j+1} ---
        for u1, u2, dx in self.lat.pairs['nearest_neighbors']:
            self.add_coupling(lam, u1, 'Sigmay', u2, 'Sigmay', dx)
