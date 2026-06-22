# 1D Multi-Solver Demo 계획서

상태: 1차 확정
확정 기록: 사용자가 "plan.md는 1차로 완성되었다. 확정되었다"라고 명시함
운영 규칙: 구현은 [next-actions.md](next-actions.md)의 Roadmap과 승인된 구현 순서를 따른다. 계획에서 벗어나는 범위 확장은 별도 확인 후 진행한다.

이 계획은 네 문서로 나뉜다.

| 문서 | 다룬다 |
|---|---|
| [scope-and-design.md](scope-and-design.md) | 범위와 설계 — 무엇을 만들고 왜 그렇게 만드는지. 자주 바뀌지 않는다. |
| [current-status.md](current-status.md) | 현재 상태 — 지금 무엇이 결정/구현되어 있는지. 코드가 바뀌면 같이 갱신한다. |
| [next-actions.md](next-actions.md) | 다음 작업 — Roadmap, 승인된 구현 순서, 아직 열려 있는 질문. |
| [decision-log.md](decision-log.md) | 결정 로그 — 언제 무엇이 왜 결정됐는지 시간순 기록. 기록된 시점의 사실이며 이후 갱신하지 않는다. |

설계를 확인하려면 scope-and-design.md, 지금 뭐가 끝났는지 확인하려면 current-status.md, 다음에 뭘 할지 확인하려면 next-actions.md, 결정이 언제 왜 내려졌는지 확인하려면 decision-log.md를 본다.

각 문서 안의 섹션은 평문 번호(`1`, `5.1`)로 매기고, 문서 간 참조는 파일명과 함께 `[current-status.md](current-status.md) 1`처럼 적는다. 같은 번호가 문서마다 따로 존재하므로 파일명을 빼면 안 된다.
