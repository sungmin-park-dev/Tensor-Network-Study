"""Compare XXZ ground-state observables across ED, Bethe, and DMRG (PBC).

Beyond the ground-state energy, three quantities are compared, all reducing to
sector ground-state energies E0(L, Delta, Sz) (plus an energy derivative):

  1. spin gap   E0(Sz=1) - E0(Sz=0)            vs chain length L,
  2. magnetization curve  <Sz_tot> vs field h  from {E0(Sz)} (Maxwell stair),
  3. nearest-neighbour correlators <Sz Sz>, <Sx Sx>  vs Delta
       - ED/DMRG : measured directly on the ground state,
       - Bethe   : Hellmann-Feynman, <SzSz>=(1/(L*Jxy)) dE/dDelta and
                   <SxSx>=(1/(2L)) dE/dJxy at fixed Jz.

The Bethe solver of verify_xxz_bethe.py is generalised to an arbitrary magnon
number M = L/2 - Sz by seeding the M lowest free-fermion momenta and continuing
in Delta. numpy + tenpy + matplotlib.
"""

from __future__ import annotations

import logging
import warnings

import numpy as np

from verify_xxz_bethe import _newton, _scattering_phase

warnings.filterwarnings("ignore")
logging.getLogger("tenpy").setLevel(logging.ERROR)


# ---------- Bethe: ground energy in the M-magnon sector ----------
def _seed_M(length, m):
    cand = []
    for n in range(length):
        k = np.pi * (2 * n + (m - 1)) / length
        k = (k + np.pi) % (2 * np.pi) - np.pi
        cand.append((np.cos(k), k))
    cand.sort()
    ks = np.sort(np.array([c[1] for c in cand[:m]]))
    numbers = np.empty(m)
    for j in range(m):
        s = sum(_scattering_phase(ks[j], ks[l], 0.0) for l in range(m) if l != j)
        numbers[j] = (length * ks[j] - s) / (2 * np.pi)
    return ks, numbers


def bethe_sector_energy(length, delta, m, jxy=1.0, nstep=80):
    if m == 0 or m == length:
        return jxy * delta * length / 4.0
    ks, numbers = _seed_M(length, m)
    try:
        for d in np.linspace(0.0, delta, nstep + 1)[1:]:
            ks = _newton(ks, numbers, length, d)
    except (np.linalg.LinAlgError, RuntimeError):
        return float("nan")
    return float(jxy * (delta * length / 4.0 + np.sum(np.cos(ks)) - delta * m))


# ---------- ED: sector ground energy and ground-state correlators ----------
def _ed_sector(length, delta, n_up, jxy=1.0):
    states = [s for s in range(1 << length) if bin(s).count("1") == n_up]
    index = {s: i for i, s in enumerate(states)}
    dim = len(states)
    ham = np.zeros((dim, dim))
    for a, s in enumerate(states):
        for i in range(length):
            j = (i + 1) % length
            bi, bj = (s >> i) & 1, (s >> j) & 1
            ham[a, a] += jxy * delta * (bi - 0.5) * (bj - 0.5)
            if bi != bj:
                t = s ^ (1 << i) ^ (1 << j)
                ham[index[t], a] += jxy * 0.5
    w, v = np.linalg.eigh(ham)
    return w[0], v[:, 0], states, index


def ed_sector_energy(length, delta, n_up, jxy=1.0):
    if n_up in (0, length):
        return jxy * delta * length / 4.0
    return _ed_sector(length, delta, n_up, jxy)[0]


# TODO: this returns the unconnected correlator <Sz_i Sz_j>. scope-and-design.md 9.2 names the
# connected correlator <Sz_i Sz_j> - <Sz_i><Sz_j> as the primary convention; add that as a
# follow-up once a benchmark/report slice needs it.
def ed_nn_correlators(length, delta, jxy=1.0):
    _, v, states, index = _ed_sector(length, delta, length // 2, jxy)
    szsz = sxsx = 0.0
    for a, s in enumerate(states):
        b0, b1 = s & 1, (s >> 1) & 1
        szsz += v[a] ** 2 * (b0 - 0.5) * (b1 - 0.5)
        if b0 != b1:
            sxsx += v[a] * v[index[s ^ 0b11]]
    return float(szsz), float(0.25 * sxsx)


# ---------- DMRG: sector ground energy and correlators ----------
def _dmrg(length, delta, n_up, jxy=1.0, chi=96, corr=False):
    from tenpy.algorithms import dmrg
    from tenpy.models.spins import SpinModel
    from tenpy.networks.mps import MPS

    model = SpinModel(dict(L=length, S=0.5, Jx=jxy, Jy=jxy, Jz=jxy * delta, hz=0.0,
                           lattice="Chain", bc_MPS="finite", bc_x="periodic", conserve="Sz"))
    prod = ["down"] * length
    for i in np.unique(np.round(np.linspace(0, length - 1, n_up)).astype(int)):
        prod[i] = "up"
    while prod.count("up") < n_up:  # rounding collisions
        prod[prod.index("down")] = "up"
    psi = MPS.from_product_state(model.lat.mps_sites(), prod, bc="finite")
    info = dmrg.run(psi, model, dict(trunc_params=dict(chi_max=chi, svd_min=1e-12),
                                     max_E_err=1e-11, max_sweeps=60, mixer=True))
    energy = float(info["E"])
    if not corr:
        return energy
    # TODO: unconnected correlator, see the note on ed_nn_correlators above.
    szsz = float(psi.correlation_function("Sz", "Sz", [0], [1])[0, 0])
    spsm = psi.correlation_function("Sp", "Sm", [0], [1])[0, 0]
    smsp = psi.correlation_function("Sm", "Sp", [0], [1])[0, 0]
    return energy, szsz, float(0.25 * (spsm + smsp).real)


def dmrg_sector_energy(length, delta, n_up, jxy=1.0, chi=96):
    if n_up in (0, length):
        return jxy * delta * length / 4.0
    return _dmrg(length, delta, n_up, jxy, chi)


# ---------- observables ----------
def spin_gap(length, delta=1.0, with_dmrg=True):
    nu0, nu1 = length // 2, length // 2 + 1
    ed = ed_sector_energy(length, delta, nu1) - ed_sector_energy(length, delta, nu0)
    be = bethe_sector_energy(length, delta, length - nu1) - bethe_sector_energy(length, delta, length - nu0)
    tn = (dmrg_sector_energy(length, delta, nu1) - dmrg_sector_energy(length, delta, nu0)) if with_dmrg else np.nan
    return ed, be, tn


def sector_energies(length, delta=1.0, method="ed"):
    """E0(Sz) for Sz = 0 .. L/2."""
    out = []
    for sz in range(length // 2 + 1):
        n_up = length // 2 + sz
        if method == "ed":
            out.append(ed_sector_energy(length, delta, n_up))
        elif method == "bethe":
            out.append(bethe_sector_energy(length, delta, length - n_up))
        else:
            out.append(dmrg_sector_energy(length, delta, n_up))
    return np.array(out)


def magnetization_curve(e0_of_sz, hs):
    """Stair m(h)/(L/2): ground Sz minimises E0(Sz) - h*Sz."""
    sz_vals = np.arange(len(e0_of_sz))
    smax = sz_vals[-1]
    return np.array([sz_vals[np.argmin(e0_of_sz - h * sz_vals)] / smax for h in hs])


def bethe_nn_correlators(length, delta, jxy=1.0, eps=1e-4):
    m = length // 2
    dE_dDelta = (bethe_sector_energy(length, delta + eps, m, jxy)
                 - bethe_sector_energy(length, delta - eps, m, jxy)) / (2 * eps)
    szsz = dE_dDelta / (length * jxy)
    jz = jxy * delta
    dE_dJxy = (bethe_sector_energy(length, jz / (jxy + eps), m, jxy + eps)
               - bethe_sector_energy(length, jz / (jxy - eps), m, jxy - eps)) / (2 * eps)
    sxsx = dE_dJxy / (2 * length)
    return float(szsz), float(sxsx)


def main():
    gap_lengths = [6, 8, 10, 12]
    mag_L = 12
    corr_L = 12
    corr_deltas = [0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5]

    print("== spin gap E(Sz=1)-E(Sz=0), Delta=1 ==")
    gap = []
    for L in gap_lengths:
        ed, be, tn = spin_gap(L, 1.0)
        gap.append((L, ed, be, tn))
        print(f"  L={L:>2}: ED={ed:.6f} Bethe={be:.6f} DMRG={tn:.6f}")

    print(f"== magnetization sectors E0(Sz), L={mag_L}, Delta=1 ==")
    e_ed = sector_energies(mag_L, 1.0, "ed")
    e_be = sector_energies(mag_L, 1.0, "bethe")
    e_tn = sector_energies(mag_L, 1.0, "dmrg")

    print(f"== nearest-neighbour correlators, L={corr_L} ==")
    corr = []
    for d in corr_deltas:
        zz_e, xx_e = ed_nn_correlators(corr_L, d)
        zz_b, xx_b = bethe_nn_correlators(corr_L, d)
        _, zz_t, xx_t = _dmrg(corr_L, d, corr_L // 2, corr=True)
        corr.append((d, zz_e, zz_b, zz_t, xx_e, xx_b, xx_t))
        print(f"  D={d:.2f}: <SzSz> ED={zz_e:+.5f} TN={zz_t:+.5f} | <SxSx> ED={xx_e:+.5f} TN={xx_t:+.5f}")

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, (a1, a2, a3) = plt.subplots(1, 3, figsize=(15, 4.3))

    Ls = [g[0] for g in gap]
    a1.plot(Ls, [g[1] for g in gap], "o-", label="ED", ms=8)
    a1.plot(Ls, [g[2] for g in gap], "s--", label="Bethe", ms=6)
    a1.plot(Ls, [g[3] for g in gap], "x:", label="DMRG", ms=9, mew=2)
    a1.set_xlabel("chain length $L$"); a1.set_ylabel(r"spin gap  $E(S_z{=}1)-E(S_z{=}0)$")
    a1.set_title(r"(a) spin gap, $\Delta=1$ (closes $\sim 1/L$)"); a1.legend()

    sz = np.arange(mag_L // 2 + 1)
    hs = np.linspace(0, 2.6, 600)
    a2.step(hs, magnetization_curve(e_ed, hs), where="post", label="ED", lw=2.5)
    a2.step(hs, magnetization_curve(e_be, hs), where="post", label="Bethe", ls="--", lw=1.8)
    a2.step(hs, magnetization_curve(e_tn, hs), where="post", label="DMRG", ls=":", lw=1.8)
    a2.set_xlabel("field $h_z$"); a2.set_ylabel(r"magnetization  $\langle S^z_{\rm tot}\rangle / (L/2)$")
    a2.set_title(rf"(b) magnetization curve, $L={mag_L}$, $\Delta=1$"); a2.legend()

    ds = [c[0] for c in corr]
    a3.plot(ds, [c[1] for c in corr], "-", color="#185FA5", label=r"$\langle S^zS^z\rangle$ ED")
    a3.plot(ds, [c[3] for c in corr], "x", color="#185FA5", ms=9, mew=2, label=r"$\langle S^zS^z\rangle$ DMRG")
    a3.plot(ds, [c[2] for c in corr], "s", color="#185FA5", ms=4, label=r"$\langle S^zS^z\rangle$ Bethe")
    a3.plot(ds, [c[4] for c in corr], "-", color="#993C1D", label=r"$\langle S^xS^x\rangle$ ED")
    a3.plot(ds, [c[6] for c in corr], "x", color="#993C1D", ms=9, mew=2, label=r"$\langle S^xS^x\rangle$ DMRG")
    a3.plot(ds, [c[5] for c in corr], "s", color="#993C1D", ms=4, label=r"$\langle S^xS^x\rangle$ Bethe")
    a3.axvline(1.0, color="gray", lw=0.8, ls="--")
    a3.set_xlabel(r"anisotropy $\Delta$"); a3.set_ylabel("nearest-neighbour correlator")
    a3.set_title(rf"(c) NN correlators, $L={corr_L}$"); a3.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig("xxz_observables_comparison.png", dpi=130)
    print("saved figure -> xxz_observables_comparison.png")

    with open("xxz_observables_comparison.csv", "w") as fh:
        fh.write("# spin_gap: L,ED,Bethe,DMRG\n")
        for L, ed, be, tn in gap:
            fh.write(f"gap,{L},{ed},{be},{tn}\n")
        fh.write("# magnetization sector energies: Sz,ED,Bethe,DMRG\n")
        for s in sz:
            fh.write(f"mag,{s},{e_ed[s]},{e_be[s]},{e_tn[s]}\n")
        fh.write("# nn_corr: Delta,szsz_ED,szsz_Bethe,szsz_DMRG,sxsx_ED,sxsx_Bethe,sxsx_DMRG\n")
        for row in corr:
            fh.write("corr," + ",".join(str(x) for x in row) + "\n")


if __name__ == "__main__":
    main()
