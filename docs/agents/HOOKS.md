---
id: "cbnu-phd-coursework/docs/agents/HOOKS.md"
title: "\ud6c5 \ubaa9\ub85d (HOOKS)"
summary: "\uc774 \ub808\ud3ec\uc5d0 \uc2e4\uc81c\ub85c \uc788\ub294 \ud6c5(Claude Code, Codex, git, pre-commit, CI, package.json)\uacfc \ucd94\uac00 \ubc29\ubc95."
domain: "cbnu-phd-coursework"
tags: ["hooks", "git", "ci", "claude-code", "codex"]
owner: "repository maintainers"
status: DRAFT
created: "2026-11-08"
updated: "2026-11-08"
source: "docs/agents/HOOKS.md"
lang: ko
sensitivity: internal
related: ["docs/agents/ROLE-janitor.md", "docs/agents/ROLE-watchdog.md", "docs/agents/handoffs/README.md"]
---
# 훅 목록 (HOOKS)

## 실측 결과 (점검일 2026-11-08)
이 레포에 있는 훅을 직접 확인한 결과입니다. 점검 명령은 아래 "재점검" 절을 봅니다.

| 종류 | 확인한 위치 | 실측 결과 | 시점 | 하는 일 | 실패 시 동작 |
|---|---|---|---|---|---|
| Claude Code | `.claude/settings*.json`의 `hooks` | 없음(실측) | — | — | — |
| Codex | `.codex/` | 없음(실측) | — | — | — |
| git | `.githooks/`, `.husky/`, `core.hooksPath`, `.git/hooks/` (sample 제외) | 없음(실측) | — | — | — |
| pre-commit | `.pre-commit-config.yaml` | 없음(실측) | — | — | — |
| CI | `.github/workflows/` | 없음(실측) (`.github/`에는 `pull_request_template.md`만 있음) | — | — | — |
| package.json | `prepare`, `precommit`, `husky`, `lint-staged` | 없음(실측) | — | — | — |

## 추가 방법 (종류별)
- **git**: `.githooks/pre-commit`을 만들고 실행 권한을 줍니다. 각 복제본에서 `git config core.hooksPath .githooks`를 한 번 실행합니다.
- **Claude Code**: `.claude/settings.json`의 `hooks`에 로컬 스크립트만 연결합니다. 원격 호출은 넣지 않습니다.
- **pre-commit**: `.pre-commit-config.yaml`을 만들고 `pre-commit install`을 실행합니다.
- **CI**: `.github/workflows/*.yml`에 `permissions: contents: read`를 먼저 적습니다.

## 안전 규칙
1. **비밀 금지**: 훅 파일에 키, 토큰, 비밀번호를 넣지 않습니다.
2. **네트워크 최소**: 훅은 로컬 검사만 합니다. 외부 호출이 필요하면 이 파일에 이유를 적고 승인을 받습니다.
3. **되돌리기**: 훅 파일을 지우고 `git config --unset core.hooksPath`를 실행하면 해제됩니다. 해제 방법을 항상 함께 적습니다.
4. **갱신**: 훅을 추가하거나 바꾸면 이 표를 고치고, 바뀐 날짜를 `updated`에 적습니다.

## 재점검
```
ls -A .claude .codex .githooks .husky .github/workflows 2>/dev/null
ls -A .pre-commit-config.yaml 2>/dev/null
git config --get core.hooksPath
```
결과가 없으면 "없음(실측)"으로 적습니다.

## 관련
- [핸드오프 규칙](handoffs/README.md)
- [정리 담당 역할](ROLE-janitor.md)
- [감시 담당 역할](ROLE-watchdog.md)
