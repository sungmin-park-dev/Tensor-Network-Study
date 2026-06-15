"""Compare XXZ-chain ground-state energy across solvers (PBC).

Three methods on the same physical system:
  - ED    : exact diagonalization in the Sz=0 sector (small L only),
  - Bethe : momentum-form Bethe equations of xxz-chain.md (exact reference),
  - DMRG  : TeNPy tensor-network ground state (reaches larger L).

The default run sweeps the chain length L at the Heisenberg point (Delta=1) and
shows convergence of the per-site energy toward the thermodynamic anchor
e0 = 1/4 - ln 2. Where the methods overlap they agree to DMRG/ED tolerance; DMRG
extends the curve to sizes ED cannot reach.

Standalone exact-reference / TN comparison; numpy + tenpy + matplotlib.
"""

from __future__ import annotations

import logging
import warnings
from math import log

import numpy as np

from verify_xxz_bethe import bethe_ground_energy, ed_ground_energy

warnings.filterwarnings("ignore")
logging.getLogger("tenpy").setLevel(logging.ERROR)

HEISENBERG_ANCHOR = 0.25 - log(2)  # thermodynamic e0 at Delta=1


def dmrg_ground_energy(length, delta, jxy=1.0, chi=160, bc_x="periodic"):
    from tenpy.algorithms import dmrg
    from tenpy.models.spins import SpinModel
    from tenpy.networks.mps import MPS

    model = SpinModel(dict(
        L=length, S=0.5, Jx=jxy, Jy=jxy, Jz=jxy * delta, hz=0.0,
        lattice="Chain", bc_MPS="finite", bc_x=bc_x, conserve="Sz",
    ))
    psi = MPS.from_product_state(model.lat.mps_sites(), ["up", "down"] * (length // 2), bc="finite")
    info = dmrg.run(psi, model, dict(
        trunc_params=dict(chi_max=chi, svd_min=1e-12),
        max_E_err=1e-12, max_sweeps=80, mixer=True,
    ))
    return float(info["E"])


def collect(delta=1.0, ed_lengths=range(4, 15, 2), other_lengths=range(4, 21, 2)):
    rows = []
    for length in sorted(set(ed_lengths) | set(other_lengths)):
        e_ed = ed_ground_energy(length, delta) if length in ed_lengths else np.nan
        e_be = bethe_ground_energy(length, delta)
        e_tn = dmrg_ground_energy(length, delta)
        rows.append((length, e_ed, e_be, e_tn))
    return rows


def main():
    delta = 1.0
    rows = collect(delta)
    print(f"XXZ ground-state energy per site, Delta={delta} (PBC)")
    print(f"{'L':>3} {'ED/L':>12} {'Bethe/L':>12} {'DMRG/L':>12}")
    for L, e_ed, e_be, e_tn in rows:
        ed_s = f"{e_ed / L:12.6f}" if not np.isnan(e_ed) else f"{'--':>12}"
        print(f"{L:>3} {ed_s} {e_be / L:12.6f} {e_tn / L:12.6f}")
    print(f"thermodynamic anchor e0 = 1/4 - ln2 = {HEISENBERG_ANCHOR:.6f}")

    with open("xxz_solver_comparison.csv", "w") as fh:
        fh.write("L,E_ED,E_Bethe,E_DMRG\n")
        for L, e_ed, e_be, e_tn in rows:
            fh.write(f"{L},{e_ed},{e_be},{e_tn}\n")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    Ls = [r[0] for r in rows]
    plt.figure(figsize=(7, 4.5))
    ed = np.array([r[1] / r[0] for r in rows])
    plt.plot([L for L, e in zip(Ls, ed) if not np.isnan(e)],
             [e for e in ed if not np.isnan(e)], "o-", label="ED (exact)", ms=7)
    plt.plot(Ls, [r[2] / r[0] for r in rows], "s--", label="Bethe (exact ref)", ms=6)
    plt.plot(Ls, [r[3] / r[0] for r in rows], "x:", label="DMRG (TeNPy)", ms=8, mew=2)
    plt.axhline(HEISENBERG_ANCHOR, color="k", lw=1, ls="-",
                label=r"$e_0=\frac{1}{4}-\ln 2$ ($L\to\infty$)")
    plt.xlabel("chain length $L$")
    plt.ylabel("ground-state energy per site $E_0/L$")
    plt.title(r"XXZ Heisenberg point $\Delta=1$ (PBC): ED vs Bethe vs DMRG")
    plt.legend()
    plt.tight_layout()
    out = "xxz_solver_comparison.png"
    plt.savefig(out, dpi=130)
    print(f"saved figure -> {out}")


if __name__ == "__main__":
    main()
