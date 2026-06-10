# Bethe Ansatz

## 소개

Bethe ansatz는 1D many-body quantum system의 고유상태를 quasi-particle rapidity 또는 momentum의
집합으로 표현하는 해법이다. 이 방법은 임의의 1D spin chain에 적용되는 일반 기법이 아니라,
factorized scattering과 충분한 수의 conserved quantities를 갖는 integrable model에서 작동한다.

이 프로젝트에서는 Bethe ansatz를 XXZ chain과 Heisenberg antiferromagnetic point의 exact reference를
이해하기 위한 방법으로 사용한다.

## 정의

Bethe ansatz의 핵심 가정은 many-body wavefunction을 몇 개의 plane-wave sector의 중첩으로 두고,
입자 간 산란을 pairwise scattering data로 환원할 수 있다는 것이다. Periodic boundary condition에서는
일관성 조건이 Bethe equations로 주어진다.

XXZ chain의 경우 이 방법은 $K=0$, $h_x=0$인 1D Hamiltonian limit과 연결된다.

| Limit | Condition | 이 프로젝트에서의 역할 |
|---|---|---|
| XXZ chain | $K=0$, $h_x=0$ | integrable reference family |
| Heisenberg AFM point | $K=0$, $h_x=h_z=0$, $J_{xy}=J_z=1$ | thermodynamic-limit anchor |

## Heisenberg AFM Ground-State Anchor

Isotropic antiferromagnetic Heisenberg chain의 thermodynamic-limit ground-state energy per site는
다음 값으로 주어진다.

$$
e_0=\frac{1}{4}-\log 2.
$$

이 값은 finite-$L$ ED pass/fail 기준이 아니라 thermodynamic-limit anchor로 사용한다. Finite-size
reference로 어떤 값을 사용할지는 별도 limit 문서와 progress note에서 확정한다.

## 참고 문서

- C. N. Yang and C. P. Yang, "One-Dimensional Chain of Anisotropic Spin-Spin Interactions. I. Proof of Bethe's Hypothesis for Ground State in a Finite System", Physical Review 150, 321 (1966).
- [../../model-hamiltonian.md](../../model-hamiltonian.md)
- [1D multi-solver first slice](../../../../Projects/1D-multi-solver-demo/progress/open/first-slice.md)
