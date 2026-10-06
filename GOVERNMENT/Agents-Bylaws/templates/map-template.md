---
frontmatter-version: 1
template-version: 1
title: Template — map-*.md
section: agents-bylaws/templates
status: in-review
last-edited-by: codex
created: 2026-06-10
updated: 2026-06-30
must-read: GOVERNMENT/Agents-Bylaws/policies/frontmatter-policy.md
---

# Template — map-*.md

`map-*.md` is an agent navigation file. It owns folder navigation, source routing, and file-role boundaries only. Keep maps short; 100 lines or fewer is recommended.
File rows in contents tables use Obsidian wikilink aliases. Folder rows stay as inline-code paths.

---

## 구조 (복사해서 사용)

```markdown
---
frontmatter-version: 1
template-version: 1
title: Map — [name]
section: [layer-local path. Omit the layer prefix when a layer has one.]
status: in-review
last-edited-by: agent-id
created: YYYY-MM-DD
updated: YYYY-MM-DD
must-read: GOVERNMENT/Agents-Bylaws/templates/map-template.md
---

# Map — [name]

- [What this folder is.]
- [Primary role or inclusion rule.]
- [Important agent context, if needed.]

## 목차 <!-- 기본형 | 택일: 기본형 / 라이프사이클형 -->
<!--
- Static directory. List direct children only.
- Include only documents and folders directly under the current folder.
- Documents inside child folders belong in that child folder's README or map.
- For lifecycle folders such as open/closed, use the lifecycle form instead.
-->

| 항목 | 역할 |
|---|---|
| [[path/to/file\|file]] | Description |
| `subfolder/` | Description |

---

## 목차 <!-- 라이프사이클형 | 택일: 기본형 / 라이프사이클형 -->
<!--
- Use for workflow directories where files move through states such as open/closed.
- Add state subsections under `## 목차` and extend columns only when useful.
-->

### `open/` — [active item description]

| 항목 | 유형 | 역할 | 상태 |
|---|---|---|---|
| [[path/to/open-file\|open-file]] | [type] | Description | [status] |

### `closed/` — [closed item description]

| 항목 | 결과 |
|---|---|
| [[path/to/closed-file\|closed-file]] | [result] |

---

### Remarks

[Optional. Use only for child-folder context, source-of-truth routing, or caution notes. Omit this section when unnecessary.]

## 에이전트 지침

- [Rules specific to this folder. Do not repeat parent AGENTS.md.]
- [Read `GOVERNMENT/Agents-Bylaws/templates/[template]-template.md` before creating matching files.]

## 참고 문서
<!--
- Documents to check/update together when this map or referenced document changes.
- When practical, referenced documents should link back to this map.
-->

- [[GOVERNMENT/Agents-Bylaws/templates/map-template\|map-template]] — map 작성 기준
```

---

## frontmatter 필드 안내

| 필드 | 값 규칙 |
|---|---|
| `frontmatter-version` | frontmatter schema version. Current value is `1`; do not change it inside this template. |
| `template-version` | Content version of this map-template. New maps copy the current value. |
| `status` | Agent-created maps start as `in-review`; the user may later mark them `accepted`. |
| `section` | Layer-local path. Do not write full repo paths when a layer prefix is implied. |
| `must-read` | Use when a file must be read before editing this file or folder. Do not duplicate root AGENTS.md here. |

Full frontmatter policy should live at `GOVERNMENT/Agents-Bylaws/policies/frontmatter-policy.md`.

---

## 작성 규칙

- **Intro bullets**: Define the folder, role, and essential context in three bullets or fewer.
- **Map scope**: maps handle navigation, source routing, and file-role boundaries. Put detailed plans, research plans, batch plans, stop rules, and detailed operating principles in named documents, policies, or templates; link only from maps.
- **목차**: Capture each direct child's core role. Put extra routing context in `### Remarks` only when needed.
- **목차 표 범위**: Include only direct child documents and folders. Documents inside child folders belong in that child folder's README or map.
- **파일 항목 표기**: Use Obsidian wikilink aliases such as `[[path/to/file\|file]]`. Escape the alias separator as `\|` inside markdown tables.
- **폴더 항목 표기**: Use inline-code folder paths such as `subfolder/`, not wikilinks.
- **Remarks**: Optional. Use only for child-folder context, source-of-truth routing, or caution notes; omit the section when unnecessary.
- **에이전트 지침**: Include only folder-specific rules. Do not repeat parent AGENTS.md.
- **참고 문서**: When this template changes, check every repo `map-*.md` one by one. Do not keep a fixed target list; query the current list with `rg --files | rg '(^|/)map-[^/]+\.md$'`.
- **legacy heading 금지**: Do not add expanded legacy headings such as `Read First`, `Source Of Truth`, `Belongs Here`, `Does Not Belong Here`, `Key Documents`, `Folder Roles`, `Agent Notes`, or `Rules` to new maps.
- **100줄 초과 시**: Consider a separate named document and link it from the map.
- **에이전트 자율 업데이트 주의**: If an agent updates a map alone, user review is recommended.

## template-version 관리

`template-version` tracks this map-template's content structure and rules. It is separate from the frontmatter schema version `frontmatter-version`.

- **This file's `template-version`**: The current map-template baseline.
- **Each `map-*.md` `template-version`**: The template version the map was last reconciled against.
- **Drift**: A map with a lower or missing `template-version` is a reconcile target.

### 버전을 올리는 기준

- Increment only when map structure, rules, or fields change in a way downstream maps must reconcile.
- Do not increment for typo fixes or wording changes that do not affect downstream maps.
- When incrementing, update both this file's frontmatter and the copy block.

현재는 `map-*.md`에만 적용한다. Other template families and automated drift checks are future work.

## 업데이트 절차

When this template changes, especially when `template-version` changes, inspect every repo `map-*.md` individually. Apply the template changes and set `template-version` to the current value, or record a justified exception.

Do not hard-code the target list in this document. Query the real list at update time:

```bash
rg --files | rg '(^|/)map-[^/]+\.md$'
```

## 참고 문서

- `/Users/david/GitHub/ai-automation-dashboard/GOVERNMENT/Agents-Bylaws/templates/map-template.md` — AAD baseline used for this template reconciliation.
