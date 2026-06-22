# XXZ 1D multi-solver findings

상태: draft v1 (2026-06-20)
범위: `H_XXZ + H_Zeeman` subset, 주로 Heisenberg point (`Jxy=1`, `Delta=Jz/Jxy=1`)
생성: `verify_xxz_bethe.py`, `compare_xxz_solvers.py`, `compare_xxz_observables.py`, `compare_xxz_entanglement_decay.py` (standalone 검증 스크립트, [current-status.md](../_meta/current-status.md) 1)
관련 결정/설계: [scope-and-design.md](../_meta/scope-and-design.md), [decision-log.md](../_meta/decision-log.md)

이 문서는 지금까지 standalone 스크립트로 만든 결과를 모은 첫 findings 초안이다.
method-consumption probe package(`one_dimensional_multi_solver_demo/`)를 거치지 않은 결과이므로,
package와 연결되기 전까지는 잠정적인 evidence로 취급한다.

같은 결과를 인터랙티브하게 보려면 [dashboard.html](dashboard.html)을 브라우저로 열면 된다
(`build_dashboard.py`가 CSV로부터 생성한다).

## 1. Energy benchmark — ED vs Bethe vs DMRG

![energy benchmark](../xxz_solver_comparison.png)

PBC, Heisenberg point(`Delta=1`)에서 chain length `L`을 4부터 20까지 늘리며 ground-state
energy per site를 비교했다. ED는 `L<=14`까지만 계산 가능하고(many-body basis 크기 제약),
Bethe ansatz와 DMRG(TeNPy)는 그 이상도 계산한다.

| L | E_ED/L | E_Bethe/L | E_DMRG/L | max abs diff |
|---|---|---|---|---|
| 4 | -0.500000 | -0.500000 | -0.500000 | 0 |
| 6 | -0.467129 | -0.467129 | -0.467129 | ~1e-14 |
| 8 | -0.456387 | -0.456387 | -0.456387 | ~1e-15 |
| 10 | -0.451545 | -0.451545 | -0.451545 | ~1e-14 |
| 12 | -0.448949 | -0.448949 | -0.448949 | ~1e-14 |
| 14 | -0.447396 | -0.447396 | -0.447396 | ~1e-14 |
| 16 | — | — | -0.446394 | — |
| 18 | — | — | -0.445708 | — |
| 20 | — | — | -0.445219 | — |

세 솔버가 겹치는 구간(`L<=14`)에서 energy per site 차이는 `~1e-14`–`1e-15` 수준으로,
[scope-and-design.md](../_meta/scope-and-design.md) 9.3의 목표(ED vs exact `<=1e-12`,
DMRG vs ED `<=1e-6`)를 훨씬 넘어선다. `L=20`에서 DMRG energy per site는 `-0.44522`로,
thermodynamic anchor `e0 = 1/4 - ln2 = -0.44315`에 유한-크기 보정만큼 가깝게 수렴한다.

## 2. Spin gap, magnetization, nearest-neighbor correlators

![observables](../xxz_observables_comparison.png)

세 패널 모두 ED/Bethe/DMRG가 시각적으로 구분 안 될 정도로 겹친다 (수치 차이는 위와 같은
order).

- (a) spin gap (`E(Sz=1) - E(Sz=0)`)은 `L=6`의 `0.685`에서 `L=12`의 `0.356`까지 줄어든다 —
  `1/L`로 닫히는 gapless 거동과 일치한다.
- (b) `L=12` 자기화 곡선은 `hz`를 늘릴 때 `Sz_tot/(L/2)`가 `0, 1/6, 1/3, ...`처럼 계단형으로
  증가한다 (finite-size plateau).
- (c) `Delta`를 늘릴 때 `<Sz Sz>`는 점점 더 음수로, `<Sx Sx>`는 점점 덜 음수로 이동하며
  `Delta=1`에서 교차한다 — XY-like에서 Ising-like easy-axis로의 anisotropy crossover.

## 3. Entanglement entropy scaling과 correlation decay

![entanglement and decay](../xxz_entanglement_decay.png)

- (a) `L=16`, PBC, Heisenberg point에서 subsystem entropy `S(l)`은 `c=1` CFT 공식
  `S(l) = (c/3) ln[(L/pi) sin(pi l/L)] + const`에 맞춰 fit한 결과 `c≈1.07`로, 이론값 `c=1`에
  근접한다 (finite-size/fit 오차 범위).
- (b) OBC에서 transverse correlator `|<Sx_i0 Sx_{i0+r}>|`의 거리별 decay를 gapless(`Delta=1`)와
  gapped(`Delta=2`)로 비교했다. gapless는 power-law로 천천히 줄고, gapped는 exponential로
  훨씬 빠르게 줄어 `r=20` 근처에서 약 1000배 차이가 난다 — gap이 correlation length를
  유한하게 만든다는 정성적 그림과 일치한다.

## 4. PBC/OBC 비교 (정책 evidence)

[scope-and-design.md](../_meta/scope-and-design.md) 6은 "구현이 쉬우면 OBC/PBC를 모두 구현해
비교한다"는 정책이다. 위 결과가 이미 그 일부를 보여준다 — 섹션 1·2·3(a)는 PBC(Bethe ansatz
reference와 맞추기 위해), 섹션 3(b)는 OBC(correlation decay 분석에 자연스러운 경계)로 실행했고,
둘 다 TeNPy에서 `bc_x` 플래그 하나로 구현 난이도 차이 없이 돌렸다.

## 5. 알려진 한계 / 후속 작업

- 이 결과는 standalone 스크립트가 직접 만든 것이고, package의 `MethodForm`을 거치지 않는다.
  `ObservableSpec`/`SolverResult`/`ComparisonReport` 계약이 확정되면 재배선이 필요하다
  ([current-status.md](../_meta/current-status.md) 1).
- nearest-neighbor correlator는 현재 unconnected `<Sz_i Sz_j>`만 계산한다. connected
  correlator(`scope-and-design.md` 9.2 convention)는 아직 구현 안 됨
  (`compare_xxz_observables.py`의 TODO 주석 참고).
- NQS 결과는 아직 없다 (roadmap stage 8, [next-actions.md](../_meta/next-actions.md) 1 참고).
