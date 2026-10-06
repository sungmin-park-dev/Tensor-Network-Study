# Neural Quantum States (NetKet)

Variational ground-state search for the 1D transverse-field Ising model (TFIM)
with a neural-network ansatz, using [NetKet](https://www.netket.org/).

| File | Content |
| --- | --- |
| `NQS_Tutorial01_1D_TFIM.ipynb` | Tutorial 1: variational search for the TFIM ground state |
| `output.png` | Figure produced by the notebook |

The notebook follows NetKet Tutorial 1 by Filippo Vicentini (EPFL-CQSL),
presented at the Lemanic Quantum Science School (Geneva, 2021). Credit for the
original material belongs to its author; see the notebook header for links.

## Running it

NetKet is not in the top-level `requirements.txt`. Use a separate environment:

```bash
uv venv netket && source netket/bin/activate
uv pip install netket jupyter matplotlib
```

`netket/` is git-ignored.
