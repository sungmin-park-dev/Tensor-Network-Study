# Quantum Tensor Networks: From Theory to Implementation

**Author**: Sung-Min Park  
**Description**: Learning tensor networks by implementing core algorithms in Python and comparing with ITensor (Julia) references.  
**Last Updated**: November 2025 (In progress)

---

## Goals

1. Master the mathematical foundations of tensor networks
2. Implement core TN algorithms (MPS, DMRG, TEBD, MERA) and validate against ITensor
3. Simulate representative 1D and 2D quantum systems
4. Compute physical observables from quantum states

---

## Implementation Topics

### 1D Systems
- Ising Model
- Heisenberg / XXZ Model
- Fermi-Hubbard Model
- Transverse Field Ising
- Free Fermion Systems

### 2D Systems
- Ladder Geometry
- Square Lattice Ising
- Square Lattice Heisenberg
- Toric Code

### Dynamics & Time Evolution
- Quantum Quench
- Periodic Driving (Floquet)
- Real-time vs Imaginary-time Evolution

### Thermal States & Open Systems
- Canonical Ensemble / Gibbs States
- Thermal vs Ground State
- Thermalization Dynamics
- Lindblad Master Equation
- Quantum Sensing with Thermal Background

### Observable Calculations
- **Entanglement**: Von Neumann entropy, Renyi entropy, entanglement spectrum, mutual information
- **Correlations**: Two-point correlators, correlation length, structure factor, order parameters
- **Thermodynamics**: Energy, heat capacity, susceptibility, free energy
- **Quantum Information**: Fisher information, squeezing, fidelity
- **Spectral**: Energy gaps, eigenvalues, density of states

---

## Learning Resources

| Resource | Link |
|----------|------|
| Glen Evenbly | https://www.glenebbly.com/tnotes |
| tensors.net | https://www.tensors.net |
| ITensor Docs | https://itensor.org/docs.cgi |

---

## Learning Philosophy

- Implement algorithms from scratch, don't just read tutorials
- Validate everything: compare with ITensor, analytical results, literature
- Build intuition through concrete examples
- Document your learning journey
- Calculate physical quantities: Theory → Implementation → Measurement

---

## Repository Structure
```
quantum-tensor-networks/
├── README.md
├── resources/
├── notebooks/
├── python/
├── itensor_reference/
└── benchmarks/
```

---

## Status

🚧 In Progress - Phase 1 (Foundations)
