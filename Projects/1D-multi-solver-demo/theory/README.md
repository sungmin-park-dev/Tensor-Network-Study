# Theory Documents

상태: 1차 이론 문서 구조  
범위: `1D-multi-solver-demo`의 이론 명세와 구현 전 검증 기준

## 1. Purpose

이 디렉터리는 solver 구현 전에 고정해야 하는 물리 모델, 기호, exact reference, 관측량,
리포트 항목을 분리해 기록한다. 각 문서는 단일 책임을 가진다. Hamiltonian 정의, 기호 표,
수치 검증 기준, 리포트 항목을 한 문서에 혼합하지 않는다.

## 2. Reading Order

권장 읽기 순서는 다음과 같다.

| Order | Document | Responsibility |
|---|---|---|
| 1 | `parameters-and-symbols.md` | symbol table, code field names, derived quantities |
| 2 | `conventions.md` | indexing, boundary, operator normalization, sign convention |
| 3 | `model-hamiltonian.md` | Hamiltonian family definition |
| 4 | `progress/open/first-slice.md` | first implementation slice and benchmark candidates |
| 5 | `exact-solutions/` | exact reference values and finite-size caveats |
| 6 | `observables-and-plots.md` | physical quantities, report tables, plot requirements |

## 3. Section Boundaries

`parameters-and-symbols.md` is the source of truth for names. A symbol should be introduced there
before being used as a persistent parameter in another document.

`conventions.md` defines how objects are interpreted. It may refer to symbols, but it should not
duplicate the full parameter table.

`model-hamiltonian.md` defines the Hamiltonian. It should contain the main equations and physical
term definitions, not the full code-field mapping.

`progress/open/first-slice.md` defines implementation-slice restrictions. It should not redefine the
full Hamiltonian. Completed or superseded progress notes move to `progress/close/`.

`exact-solutions/` defines reference solutions. It should distinguish finite-$L$ exact values from
thermodynamic-limit anchors.

`observables-and-plots.md` defines the report contract. It should state what a user must see before
solver results are compared.

## 4. Notation Discipline

- 문서에서 반복적으로 재사용되지 않을 기호는 도입하지 않는다.
- 한 문단 또는 한 수식 설명에서만 필요한 대상은 새 기호보다 prose와 기존 index로 설명한다.
- Geometry와 model parameter를 구분하기 위한 최소 기호는 허용하되, 후속 문서나 구현에서 실제로
  추적할 필요가 없는 auxiliary set notation은 피한다.
- 현재 승인된 범위를 벗어난 확장 notation은 별도 계획이 승인되기 전까지 theory 문서에 추가하지
  않는다.

## 5. Revision Discipline

- 지적한 것만 수정한다.
- 지적이 모호한 경우에는 수정하기 전에 되묻는다.

## 6. Writing Style

Theory notes follow [writing-guidelines.md](writing-guidelines.md). This file combines the LSWT
writing-style policy with local writing rules established during the exact-solution note review.
