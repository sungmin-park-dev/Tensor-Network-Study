"""(a) entanglement scaling and (b) correlation decay for the XXZ chain.

(a) Block entanglement entropy S(l) vs subsystem size at Delta=1, L=16, PBC:
    ED and DMRG match the c=1 Calabrese-Cardy form
        S(l) = (c/3) ln[(L/pi) sin(pi l / L)] + const,  c = 1.
    A linear fit recovers c ~ 1 (small finite-size excess at the SU(2) point).
    PBC is used here for weak boundary oscillation and a clean central charge,
    matching the boundary condition of the energy/gap/magnetization comparison.

(b) Longitudinal correlator |<Sz_i0 Sz_{i0+r}>| vs distance r, OBC: gapless
    Delta=1 decays algebraically (power law, exponent ~1 from Luttinger-liquid /
    Bethe), gapped Delta=2 decays exponentially. ED (L=16) cross-checks DMRG
    (L=48). OBC lets DMRG reach a long, clean decay range cheaply; the bulk decay
    is not boundary sensitive.
"""

from __future__ import annotations

import logging
import warnings

import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh

warnings.filterwarnings("ignore")
logging.getLogger("tenpy").setLevel(logging.ERROR)

SX = sp.csr_matrix(0.5 * np.array([[0, 1], [1, 0]], complex))
SY = sp.csr_matrix(0.5 * np.array([[0, -1j], [1j, 0]], complex))
SZ = sp.csr_matrix(0.5 * np.array([[1, 0], [0, -1]], complex))


def _op(o, i, L):
    return sp.kron(sp.kron(sp.identity(2 ** i), o), sp.identity(2 ** (L - 1 - i)), format="csr")


def ed_ground(L, delta, bc, jxy=1.0):
    bonds = range(L) if bc == "periodic" else range(L - 1)
    H = sp.csr_matrix((2 ** L, 2 ** L), dtype=complex)
    for i in bonds:
        j = (i + 1) % L
        H = H + jxy * (_op(SX, i, L) @ _op(SX, j, L)
                       + _op(SY, i, L) @ _op(SY, j, L)
                       + delta * _op(SZ, i, L) @ _op(SZ, j, L))
    _, v = eigsh(H, k=1, which="SA")
    return v[:, 0]


def ed_entropy(psi, L, ell):
    s = np.linalg.svd(psi.reshape(2 ** ell, 2 ** (L - ell)), compute_uv=False) ** 2
    s = s[s > 1e-14]
    return float(-np.sum(s * np.log(s)))


def ed_sxsx(psi, L, i, j):
    op = _op(SX, i, L) @ _op(SX, j, L)
    return float(np.real(psi.conj() @ (op @ psi)))


def dmrg_state(L, delta, bc, jxy=1.0, chi=128):
    from tenpy.algorithms import dmrg
    from tenpy.networks.mps import MPS

    params = dict(L=L, S=0.5, Jx=jxy, Jy=jxy, Jz=jxy * delta, hz=0.0,
                  bc_MPS="finite", bc_x=bc, conserve="Sz")
    if bc == "periodic":
        from tenpy.models.spins import SpinModel
        model = SpinModel(dict(params, lattice="Chain"))
    else:
        from tenpy.models.spins import SpinChain
        model = SpinChain(params)
    psi = MPS.from_product_state(model.lat.mps_sites(), ["up", "down"] * (L // 2), bc="finite")
    dmrg.run(psi, model, dict(trunc_params=dict(chi_max=chi, svd_min=1e-12),
                              max_E_err=1e-12, max_sweeps=60, mixer=True))
    return psi


def cft_entropy(ell, L, c=1.0):  # PBC, two boundary points
    return (c / 3.0) * np.log((L / np.pi) * np.sin(np.pi * ell / L))


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(11.5, 4.4))

    # ---- (a) entanglement scaling, Delta=1, L=16, PBC ----
    Le = 16
    ells = np.arange(1, Le)
    psi_ed = ed_ground(Le, 1.0, "periodic")
    s_ed = np.array([ed_entropy(psi_ed, Le, l) for l in ells])
    s_tn = np.array(dmrg_state(Le, 1.0, "periodic").entanglement_entropy())
    g = np.log((Le / np.pi) * np.sin(np.pi * ells / Le))
    slope, const = np.polyfit(g, s_ed, 1)
    c_fit = 3 * slope
    print(f"(a) entanglement L={Le}, Delta=1 (PBC): ED-DMRG max|diff|="
          f"{np.max(np.abs(s_ed - s_tn)):.1e}, fitted c={c_fit:.3f}")
    b1 = float(np.mean(s_ed - cft_entropy(ells, Le)))
    a1.plot(ells, s_ed, "o", ms=8, label="ED", color="#185FA5")
    a1.plot(ells, s_tn, "x", ms=9, mew=2, label="DMRG", color="#1D9E75")
    a1.plot(ells, cft_entropy(ells, Le) + b1, "-", lw=1.5, color="#993C1D",
            label=f"c=1 CFT (fit c={c_fit:.2f})")
    a1.set_xlabel("subsystem size $\\ell$"); a1.set_ylabel("entanglement entropy $S(\\ell)$")
    a1.set_title(f"(a) entanglement scaling, L={Le}, $\\Delta=1$ (PBC)")
    a1.legend()

    # ---- (b) transverse correlation decay, gapless vs gapped, OBC ----
    Lc_ed, Lc_tn = 16, 48
    rows = []
    for delta, color, name in [(1.0, "#534AB7", "gapless $\\Delta=1$"),
                               (2.0, "#BA7517", "gapped $\\Delta=2$")]:
        i0e = Lc_ed // 2
        pe = ed_ground(Lc_ed, delta, "open")
        re = np.arange(1, Lc_ed // 2)
        ce = np.array([abs(ed_sxsx(pe, Lc_ed, i0e, i0e + r)) for r in re])
        i0t = Lc_tn // 2
        pt = dmrg_state(Lc_tn, delta, "open")
        rt = np.arange(1, Lc_tn // 2)
        cols = (i0t + rt).tolist()
        spsm = pt.correlation_function("Sp", "Sm", [i0t], cols)[0]
        smsp = pt.correlation_function("Sm", "Sp", [i0t], cols)[0]
        ct = np.abs(0.25 * (spsm + smsp).real)
        a2.semilogy(rt, ct, "-", color=color, lw=2, label=f"{name} DMRG (L={Lc_tn})")
        a2.semilogy(re, ce, "o", color=color, ms=6, label=f"{name} ED (L={Lc_ed})")
        rows.append((delta, rt, ct))
    a2.set_xlabel("distance $r$"); a2.set_ylabel(r"$|\langle S^x_{i_0} S^x_{i_0+r}\rangle|$")
    a2.set_title("(b) transverse correlation decay (OBC)")
    a2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("xxz_entanglement_decay.png", dpi=130)
    print("saved figure -> xxz_entanglement_decay.png")

    with open("xxz_entanglement_decay.csv", "w") as fh:
        fh.write("# entanglement L=16 Delta=1 PBC: ell,S_ED,S_DMRG\n")
        for l, se, st in zip(ells, s_ed, s_tn):
            fh.write(f"ent,{l},{se},{st}\n")
        fh.write("# transverse decay DMRG L=48 OBC: Delta,r,|SxSx|\n")
        for delta, rt, ct in rows:
            for r, val in zip(rt, ct):
                fh.write(f"decay,{delta},{r},{val}\n")


if __name__ == "__main__":
    main()
