# 1D Multi-Solver Demo — 결정 로그

이 문서는 시간순 기록이다. 각 항목은 기록된 시점의 사실이며, 이후 갱신 책임을 지지 않는다.
지금 무엇이 참인지는 [scope-and-design.md](scope-and-design.md)와 [current-status.md](current-status.md)를 본다.

2026-06-10, 초기 계획 확정 시점:

1. 프로젝트 경로는 `Projects/1D-multi-solver-demo/`로 둔다.
2. 패키징 이름은 숫자와 kebab case를 살린 `1d-multi-solver-demo`로 둔다.
3. Python import package 디렉터리는 Python 문법 제약 때문에 `one_dimensional_multi_solver_demo`로 둔다.
4. 첫 구현 slice는 이론 문서, system-definition issue note, `SpinSystem`, `MethodForm`, `run_method_probe.py`, `test_method_forms.py` 순서로 진행한다.
5. XXZ, Cluster, Zeeman term은 최종적으로 같은 1D system family에서 on/off 가능해야 하지만, code probe는 XXZ + Zeeman subset과 method consumption trace에 한정한다.
6. `benchmark point`는 `검증 지점(benchmark point)`으로 풀어 쓰며, [scope-and-design.md](scope-and-design.md) 9.4에서 정의한다.
7. 첫 slice의 검증 지점 초안은 두 개다 (`BP-XXZ-1`, `BP-XXZ-2`, 9.4). 이 내용은 theory 문서와 exact reference 정리 과정에서 변경될 수 있다.
8. Cluster term convention은 처음에는 미확정으로 두고 `../../../Models/1d-spin-chains/model-hamiltonian.md` 작성 중에 다시 검토하기로 했다.

2026-06-20:

9. Cluster term의 local operator convention을 spin operator `S = sigma/2`로 확정했다 (8번 항목의 후속 결정). 기존 `H_XXZ`, `H_Zeeman`과 같은 convention으로 통일하는 것이 더 일반적인 선택이라는 판단이다. `K_Pauli = K_spin / 8`로 환산한다. 자세한 내용은 [scope-and-design.md](scope-and-design.md) 5.1을 본다.
10. 1D PBC/OBC 전략을 "OBC가 기본, PBC는 탐색적"에서 "구현 난이도가 낮으면 OBC/PBC를 모두 구현해 정확도·속도를 직접 비교하고, 구현이 어려운 method에서만 더 쉬운 쪽을 고른다"로 수정했다. 궁극적인 목표가 솔버 결과 간 비교라는 판단에 따른 것이다. 자세한 내용은 [scope-and-design.md](scope-and-design.md) 6을 본다.
