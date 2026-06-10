"""
Cluster-Ising Model: Tensor Network Simulation
================================================
Based on PhysRevA.84.022304 (Smacchia et al., 2011)

H(λ) = -Σ σ^x_{j-1} σ^z_j σ^x_{j+1} + λ Σ σ^y_j σ^y_{j+1}

Generalized:
H = -J_c Σ σ^x σ^z σ^x + J_xxz Σ (σ^x σ^x + σ^y σ^y + Δ σ^z σ^z)
  + J_I Σ σ^y σ^y + h(t) Σ σ^z
"""

__version__ = "0.1.0"
