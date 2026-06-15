---
frontmatter-version: 1
title: Exact-Solution Physics Review
section: issue-notes/open
issue-type: review
status: draft
last-edited-by: claude
created: 2026-06-14
updated: 2026-06-14
---

# Exact-Solution Physics Review

상태: open issue note  
범위: exact-solution theory note의 physics 정확성과 convention 검증 (현재
`Models/1d-spin-chains/exact-solutions/`)

## Current Agreement

- `tfim-chain.md`을 `xx-chain.md` 표준(자기완결 유도, 코드-평가형 물리량)으로 재작성했고, 일반 BdG
  대각화는 `method/bogoliubov-diagonalization.md`로 분리했다.
- writing style과 language 통일은 끝났다. 남은 것은 **physics correctness와 convention 검증**이다.
- 이 노트는 그 검증 포인트를 to-do로 모은다. 각 항목은 사용자 확인 또는 ED 교차검증으로 닫히기
  전까지 open이다.
- 항목은 derivation을 의심한다는 뜻이 아니라, normalization·sign·convention처럼 **코드 비교 전에
  못 박아야 하는 선택**을 표면화한 것이다.

## Scope And Non-Goals

- Scope: `tfim-chain.md`, `method/bogoliubov-diagonalization.md`의 physics 검증. `xx-chain.md`,
  `method/jordan-wigner.md`는 2026-06-14 검토 완료(아래 Reviewed 참조). 이후 다른 모델
  노트(`xxz-chain` 등)가 같은 표준으로 작성되면 같은 패턴으로 항목을 추가한다.
- Non-goals: writing style/language(완료), 코드 구현, benchmark 수치 확정.

## Review Items

표기: `[ ]` open, `[x]` resolved. 각 항목은 `claim — 위치 — 검토 이유 — 검증 방법`.

### tfim-chain.md

- [ ] **유한-$L$ 기저에너지 parity selection rule** — `Physical Quantities / Ground-State Energy`.
  $k=0,\pi$ unpaired 모드가 Bogoliubov vacuum parity를 정하고, parity가 sector와 어긋나면 최소
  $\epsilon(k)$를 더해 flip한다고 적었다. 케이스를 완전 열거하지 않은 "recipe" 수준이다.
  검증: $L=4,6,8$에서 OBC/PBC, 양 sector ED 기저에너지와 직접 비교.
- [ ] **$B(k)=\tfrac{J_z}{4}\sin k$ 계수** — `Solution / PBC Diagonalization`. pairing 항을
  antisymmetrize하면 $\sin k$에 비례한다고만 적고 정확한 계수 전개는 생략했다.
  검증: Fourier 전개를 명시적으로 다시 해 계수 확인, $\epsilon(k)=2\sqrt{A^2+B^2}$가 알려진 TFIM
  스펙트럼/gap을 재현하는지 확인.
- [ ] **PBC sector ↔ momentum grid mapping** — `Solution / PBC Diagonalization`.
  $e^{ikL}=-\lambda_{\Pi}$로 $\lambda_{\Pi}=-1$을 periodic, $+1$을 antiperiodic grid에 대응시켰다.
  sector 라벨(NS/Ramond)과 vacuum parity 일관성을 확인해야 한다.
  검증: 작은 $L$에서 각 sector grid의 vacuum parity가 $\lambda_{\Pi}$와 맞는지 점검.
- [ ] **$\langle S_i^x\rangle=\tfrac{1}{L}\sum_k A(k)/\epsilon(k)$ 닫힌형** — `Physical Quantities /
  Transverse Magnetization`. per-mode $\langle n_k\rangle=\tfrac12(1-2A/\epsilon)$에서 유도. 부호와
  정규화 확인 필요. 검증: ED transverse magnetization과 비교.
- [ ] **$\langle S_i^xS_j^x\rangle$ Wick (3항 $\Gamma$ 식)** — `Physical Quantities / Correlators`.
  Majorana covariance의 4-fermion Wick 전개 항과 부호 확인. 검증: ED와 비교.
- [ ] **$\langle S_i^zS_j^z\rangle$ Pfaffian index set과 부호** — `Physical Quantities / Correlators`.
  string을 Majorana $\{w_{2i+1},\ldots,w_{2j}\}$로 두고 $\operatorname{Pf}$로 적었다. index set과
  overall sign이 Majorana convention $w_{2i+1}=i(c_i^\dagger-c_i)$에 의존한다.
  검증: ED $\langle S_i^zS_j^z\rangle$와 비교, 작은 $|i-j|$에서 부호 확인.
- [ ] **$\xi^{-1}=\lvert\log(2h_x/J_z)\rvert$ 정규화** — `Physical Quantities / Correlation Length`.
  표준 결과지만 우리 convention($S^a=\sigma^a/2$, 결합 $J_z$·$h_x$)에서 계수가 맞는지 미확인.
  $\Delta=\lvert h_x-J_z/2\rvert$는 dispersion에서 직접 확인 가능.
  검증: $\epsilon(i\kappa)=0$ 조건을 우리 $A(k),B(k)$로 직접 풀어 $\kappa_*$ 확인.

### method/bogoliubov-diagonalization.md

- [ ] **$E_{\mathrm{shift}}=E_{\mathrm{const}}+\tfrac12\operatorname{Tr}A$,
  $E_{\mathrm{vac}}=E_{\mathrm{const}}+\tfrac12\operatorname{Tr}A-\tfrac12\sum_{E_\alpha>0}E_\alpha$** —
  `Quasiparticle Modes`. normal-ordering 상수의 부호/convention 확인. 검증: 작은 BdG 행렬에서 직접
  대각화한 기저에너지와 비교.
- [ ] **Ground-state correlations $\langle c_i^\dagger c_j\rangle=\sum_\alpha v_iv_j^*$,
  $\langle c_ic_j\rangle=\sum_\alpha u_iv_j^*$** — `Ground-State Correlations`. $u,v$의 index/conjugation
  convention이 $\gamma_\alpha$ 정의·정규화와 self-consistent한지 확인. 검증: 자유 fermion 한계와
  비교, $\Gamma$가 valid covariance(고유값 $\in[-1,1]$)인지 점검.
- [ ] **Bogoliubov amplitudes $u_k=\cos\theta_k$, $v_k=i\sin\theta_k$, $\tan2\theta_k=B/A$** —
  `Translation-Invariant Two-Mode Form`. two-mode 형식의 $iB$ pairing과 부호 일관성 확인.

### xxz-chain.md, method/bethe-ansatz.md (draft 2026-06-14)

ED로 확인된 부분(=신뢰):

- [x] **Reference 에너지 $E_{\mathrm{ref}}=J_{xy}\Delta L/4$** — spin ED와 일치($L=4,6,8$).
- [x] **Ground state가 $M=L/2$ ($S_{\mathrm{tot}}^z=0$) sector** — $\Delta=0,0.5,1,2$에서 확인.
- [x] **특수점 thermodynamic 에너지** $\Delta=0\to-J_{xy}/\pi$, $\Delta=1\to J_{xy}(\tfrac14-\log2)$ —
  유한 $L$ 추세가 수렴($L=6\ldots12$).

검증 완료(=신뢰):

- [x] **XXZ 2-magnon scattering phase / Bethe equations / 에너지식** — `Solution / XXZ Bethe
  Equations`. 문서의 momentum-form Bethe 방정식을 $\Delta=0$ free-fermion 해에서 시작해 Newton
  continuation으로 $M=L/2$ real root를 풀고, $E=J_{xy}\Delta L/4+J_{xy}\sum(\cos k_j-\Delta)$를
  $S^z=0$ 섹터 ED와 비교: $L=8,10,12$, $\Delta=0,0.25,0.5,0.75,1.0,1.5,2.0$ 전부 $\sim10^{-14}$ 일치.
  $-2\Delta$ scattering 형태와 부호, real momentum modulus-1, 에너지식이 한 번에 확인됨.
  ($\varepsilon(k)=J_{xy}(\cos k-\Delta)$ 분산도 이 에너지식에 포함되어 검증됨.) 검증 스크립트:
  `Projects/1D-multi-solver-demo/verify_xxz_bethe.py` (core gapless 구간 PASS, 기계정밀도).
- [x] **TN(DMRG) 교차검증** — TeNPy `SpinModel` DMRG(PBC)를 ED·Bethe와 비교: Heisenberg
  $\Delta=1$에서 $L=4\ldots14$ 세 방법이 $\sim10^{-13}$ 일치, DMRG는 $L=20$까지 연장되어
  thermodynamic anchor $\tfrac14-\log2$로 수렴. convention(Jx=Jy=$J_{xy}$, Jz=$J_z$)이 ED와 정확히
  맞음(OBC에서 $L=10$ 기계정밀도 일치로 확인). 스크립트/그림:
  `Projects/1D-multi-solver-demo/compare_xxz_solvers.py`, `xxz_solver_comparison.png`. (참고: 단순
  continuation Bethe solver는 $\Delta=1$, $L\ge16$에서 nan — 그 구간은 DMRG가 커버.)
- [x] **에너지 외 3개 관측량 3-way 비교** — ED·Bethe·DMRG가 (i) spin gap $E(S_z{=}1)-E(S_z{=}0)$ vs
  $L$ (gapless $\sim1/L$), (ii) 자기화 계단 $\langle S^z_{\rm tot}\rangle$ vs $h_z$ (포화장 $h_{\rm
  sat}=2J$), (iii) 최근접 상관 $\langle S^zS^z\rangle,\langle S^xS^x\rangle$ vs $\Delta$ ($\Delta{=}1$
  교차)에서 모두 일치. Bethe는 sector별 ground 에너지 + Hellmann–Feynman($\partial E/\partial J$)로
  기여. 내부 검증: ED-direct = Bethe-HF, 합규칙 $2\langle S^xS^x\rangle+\Delta\langle S^zS^z\rangle=E_0/L$.
  스크립트/그림: `Projects/1D-multi-solver-demo/compare_xxz_observables.py`,
  `xxz_observables_comparison.png`.
- [x] **얽힘 엔트로피 + 상관 decay** — (a) block 얽힘 $S(\ell)$, $\Delta=1$, $L=16$ PBC: ED=DMRG
  ($\sim10^{-9}$), $c=1$ Calabrese–Cardy 형식 일치(fit $c\approx1.07$, SU(2)점 finite-size 잔차).
  (b) 횡 상관 $|\langle S^x_0S^x_r\rangle|$ (OBC): gapless $\Delta=1$ 멱법칙 vs gapped $\Delta=2$
  지수감쇠(횡), 종 $\langle S^zS^z\rangle$은 $\Delta=2$에서 Néel 장거리질서. Bethe/적분가능성은 $c=1$·
  멱지수 이론 기준선으로 기여. 스크립트/그림:
  `Projects/1D-multi-solver-demo/compare_xxz_entanglement_decay.py`, `xxz_entanglement_decay.png`.

검증 필요(=open):

- [ ] **일반 gapless $0<\Delta<1$ 기저에너지 적분 kernel** — `Physical Quantities / Ground-State
  Energy`. $\Delta=\cos\gamma$ root-density 적분의 정확한 kernel을 명시하지 않고 "reference에 맞춰야
  한다"로 남겨둠. **우선순위 하향**: 유한-$L$ 에너지가 직접 검증됐으므로 이 항목은 thermodynamic
  닫힌형 편의용. Yang-Yang/Takahashi와 대조해 확정 후 채울 것.
- [ ] **강한 gapped $\Delta\gtrsim3$ ground state** — continuation solver가 깨짐(near-degenerate
  real roots). 문서 오류가 아니라 solver 한계. rapidity/log 형식 solver로 확장하면 확인 가능.

### Reviewed 2026-06-14 — xx-chain.md, method/jordan-wigner.md

`method/jordan-wigner.md`:

- [x] **Parity string과 exchange relations** — $p_\ell=1-2n_\ell=e^{i\pi n_\ell}$, $P_j$
  Hermitian/unitary, $\{P_j,c_k\}=0\,(k<j)$, $[P_j,c_k]=0\,(k\ge j)$, 그리고 on-site spin algebra
  $[S^+,S^-]=2S^z$, $(S^+)^2=0$을 대수적으로 확인. 오류 없음.
- [ ] (optional, 스타일) `Applications` 표가 XX/TFIM의 model-specific 조건을 method 노트에 둔다.
  포인터 수준이라 허용 범위지만, Method/Model 분리를 엄격히 하려면 조건 열을 줄일 수 있다.

`xx-chain.md`:

- [x] **String reduction과 boundary parity** — 일반 쌍 $i<j$ 환원($P_iP_j=p_iQ_{ij}$), OBC/PBC
  fermion Hamiltonian, $\Pi=(-1)^{N_f}$ 경계항을 대수적으로 확인. 오류 없음.
- [x] **Ground-state energy 닫힌형(OBC/PBC, even/odd)** — spin ED와 end-to-end 비교에서 $L=2\ldots8$
  OBC·PBC 전부 $<10^{-9}$ 일치. JW 매핑 + parity sector + free-fermion + 닫힌형을 한 번에 검증.
- [x] **Longitudinal correlator** $\langle S^z_iS^z_j\rangle=(G_{ii}-\tfrac12)(G_{jj}-\tfrac12)-G_{ij}G_{ji}$
  ($i\ne j$) — free-fermion Wick으로 확인.
- [ ] (optional, 완결성) **Transverse correlator** $\langle S^x_iS^x_j\rangle$가 "Gaussian Wick
  determinants or Pfaffians" 포인터로 남아 있다. 새 가이드라인 기준 명시적 construction으로 채울 수
  있다. 사용자 관리 파일이라 보고만 하고 수정은 보류.

Cross-note: XX의 PBC sector↔momentum grid mapping($\lambda_{\Pi}=-1$ periodic, $+1$ antiperiodic,
$c_L=-\lambda_{\Pi}c_0$)이 검증된 에너지와 일치하므로, 같은 mapping을 쓰는 tfim의
`PBC sector ↔ momentum grid mapping` 항목 중 **grid 공식 부분은 부분적으로 de-risk**된다. 다만 tfim의
BdG vacuum-parity 규칙(pairing case)은 여전히 별도 확인이 필요하다.

## Approval Needed

- 사용자가 각 항목을 confirm 또는 correct.
- 특히 convention 선택(Majorana 정의, parity sector 라벨, normal-ordering 상수)은 사용자 판단이
  우선한다. 확정된 선택은 `conventions.md` 또는 해당 노트에 반영한다.

## Verification

- 주 수단은 ED 교차검증이다. `1D-multi-solver-demo`의 ED form이 준비되면 작은 $L$에서 OBC/PBC, 양
  sector의 기저에너지·magnetization·correlator를 exact 식과 직접 비교한다.
- gap $\Delta=\lvert h_x-J_z/2\rvert$는 dispersion에서 즉시 확인 가능하므로 먼저 점검한다.
- 부호·계수는 symbolic 전개로 재확인한다.

## Rollback Or Close Conditions

- 모든 item이 confirmed 되거나, 수정이 해당 노트에 반영되면 이 노트를 `issue-notes/closed/`로 옮긴다.
- 새 모델 노트가 추가되면 같은 체크리스트 패턴으로 항목을 늘린다.
