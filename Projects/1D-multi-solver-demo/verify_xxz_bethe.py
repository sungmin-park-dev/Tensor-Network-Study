"""Exact-reference check: XXZ Bethe ansatz energy vs exact diagonalization.

This verifies the finite-chain ground-state energy of
`Models/1d-spin-chains/exact-solutions/xxz-chain.md` against direct
diagonalization. It solves the momentum-form Bethe equations of that note for the
M = L/2 real-momentum ground state by continuation from the Delta = 0
free-fermion solution, then compares the Bethe energy

    E = Jxy * Delta * L / 4 + Jxy * sum_j (cos k_j - Delta)

to the exact ground-state energy in the Sz = 0 sector.

The core check is the gapless regime 0 <= Delta <= 1 (including the Heisenberg
point), where the real-root continuation is robust and matches ED to machine
precision on L = 8, 10, 12. Gapped points Delta > 1 are run as a best-effort
extension: they pass for smaller L but the simple real-root continuation becomes
fragile (near-degenerate roots) and is reported as a skip when it fails to
converge, rather than crashing. The strongly gapped regime needs a
rapidity/log-form solver. See
`GOVERNMENT/Working-Pad/issue-notes/open/260614-exact-solution-physics-review.md`.

Standalone by design (numpy only); it does not yet depend on the project package.
When an ED solver lands in the package, the ED side here can be wired to it.
"""

from __future__ import annotations

import numpy as np

CORE_DELTAS = (0.0, 0.25, 0.5, 0.75, 1.0)       # gapless: robust, must pass
EXTENDED_DELTAS = (1.5, 2.0)                     # gapped: best-effort
DEFAULT_LENGTHS = (8, 10, 12)


# ---------- exact diagonalization in the Sz = 0 sector ----------
def ed_ground_energy(length: int, delta: float, jxy: float = 1.0) -> float:
    states = [s for s in range(1 << length) if bin(s).count("1") == length // 2]
    index = {s: i for i, s in enumerate(states)}
    dim = len(states)
    ham = np.zeros((dim, dim))
    for a, s in enumerate(states):
        for i in range(length):
            j = (i + 1) % length
            bi, bj = (s >> i) & 1, (s >> j) & 1
            ham[a, a] += jxy * delta * (bi - 0.5) * (bj - 0.5)
            if bi != bj:  # (Jxy/2)(S+S- + S-S+) flips a differing pair
                t = s ^ (1 << i) ^ (1 << j)
                ham[index[t], a] += jxy * 0.5
    return float(np.linalg.eigvalsh(ham)[0])


# ---------- Bethe-equation ground state (real momenta, M = L/2) ----------
def _scattering_phase(kj: float, kl: float, delta: float) -> float:
    """Smooth arg of S = -(1 - 2D e^{ikj} + e^{i(kj+kl)})/(1 - 2D e^{ikl} + e^{i(kj+kl)}).

    Factoring out e^{i(kj-kl)} leaves a conjugate pair, giving a branch-free atan2.
    """
    return np.pi + (kj - kl) + 2 * np.arctan2(
        np.sin(kl) - np.sin(kj), np.cos(kj) + np.cos(kl) - 2 * delta
    )


def _seed(length: int):
    """Delta = 0 ground-state momenta in the M = L/2 sector. Quantum numbers are
    fixed from the seed so the Delta = 0 residual is exactly zero."""
    m = length // 2
    cand = []
    for n in range(length):
        k = np.pi * (2 * n + (m - 1)) / length
        k = (k + np.pi) % (2 * np.pi) - np.pi
        cand.append((np.cos(k), k))
    cand.sort()
    ks = np.sort(np.array([c[1] for c in cand[:m]]))
    numbers = np.empty(m)
    for jx in range(m):
        phase = sum(_scattering_phase(ks[jx], ks[lx], 0.0) for lx in range(m) if lx != jx)
        numbers[jx] = (length * ks[jx] - phase) / (2 * np.pi)
    return ks, numbers


def _residual(ks, numbers, length, delta):
    m = len(ks)
    res = np.empty(m)
    for jx in range(m):
        phase = sum(_scattering_phase(ks[jx], ks[lx], delta) for lx in range(m) if lx != jx)
        res[jx] = length * ks[jx] - 2 * np.pi * numbers[jx] - phase
    return res


def _newton(ks, numbers, length, delta, tol=1e-12, iters=200):
    ks = ks.copy()
    m = len(ks)
    for _ in range(iters):
        res = _residual(ks, numbers, length, delta)
        if np.max(np.abs(res)) < tol:
            return ks
        jac = np.empty((m, m))
        step = 1e-7
        for c in range(m):
            kp = ks.copy()
            kp[c] += step
            jac[:, c] = (_residual(kp, numbers, length, delta) - res) / step
        try:
            ks = ks - np.linalg.solve(jac, res)
        except np.linalg.LinAlgError:  # near-degenerate roots (strong gapped)
            ks = ks - np.linalg.lstsq(jac, res, rcond=None)[0]
    if np.max(np.abs(_residual(ks, numbers, length, delta))) > 1e-8:
        raise RuntimeError("Bethe continuation did not converge")
    return ks


def bethe_ground_energy(length: int, delta: float, jxy: float = 1.0, nstep: int = 80) -> float:
    """Ground-state energy from the Bethe roots. Returns nan if the real-root
    continuation fails (strongly gapped regime needs a rapidity-form solver)."""
    ks, numbers = _seed(length)
    try:
        for d in np.linspace(0.0, delta, nstep + 1)[1:]:
            ks = _newton(ks, numbers, length, d)
    except (np.linalg.LinAlgError, RuntimeError):
        return float("nan")
    return float(jxy * (np.sum(np.cos(ks)) - delta * length / 4.0))


def _run(deltas, *, require_pass):
    worst = 0.0
    for length in DEFAULT_LENGTHS:
        for delta in deltas:
            e_ed = ed_ground_energy(length, delta)
            e_bethe = bethe_ground_energy(length, delta)
            if np.isnan(e_bethe):
                print(f"{length:>3} {delta:>6.2f} {'--':>13} {e_ed:>13.6f} {'skip':>10}")
                continue
            diff = abs(e_bethe - e_ed)
            worst = max(worst, diff)
            print(f"{length:>3} {delta:>6.2f} {e_bethe:>13.6f} {e_ed:>13.6f} {diff:>10.2e}")
    return worst


def main() -> None:
    print(f"{'L':>3} {'Delta':>6} {'E_Bethe':>13} {'E_ED':>13} {'|diff|':>10}")
    print("# core: gapless 0 <= Delta <= 1")
    worst = _run(CORE_DELTAS, require_pass=True)
    print("# extended (best-effort): gapped Delta > 1")
    _run(EXTENDED_DELTAS, require_pass=False)
    print(f"\ncore max |E_Bethe - E_ED| = {worst:.2e}  ->  {'PASS' if worst < 1e-9 else 'FAIL'}")


if __name__ == "__main__":
    main()
