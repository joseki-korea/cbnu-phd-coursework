---
id: "cbnu-phd-coursework/docs/agents/handoffs/README.md"
title: "\ud578\ub4dc\uc624\ud504 \uaddc\uce59"
summary: "\uc5d0\uc774\uc804\ud2b8 \uc138\uc158 \uac04 \uc791\uc5c5 \uc778\uc218\uc778\uacc4 \ud30c\uc77c\uc758 \uc774\ub984, \uc791\uc131, ACK, \ubcf4\uad00 \uaddc\uce59."
domain: "cbnu-phd-coursework"
tags: ["handoff", "agents", "rules"]
owner: "repository maintainers"
status: DRAFT
created: "2026-11-08"
updated: "2026-11-08"
source: "docs/agents/handoffs/README.md"
lang: ko
sensitivity: internal
related: ["docs/agents/handoffs/TEMPLATE.md", "docs/agents/ROLE-janitor.md", "RULES.md"]
---
# 핸드오프 규칙

## 목적
에이전트 세션이 바뀔 때 작업 상태를 파일로 넘깁니다. 대화 기록에 의존하지 않고, 누가 읽어도 같은 내용을 보게 하려는 것입니다.

## 파일 이름
`YYYYMMDD-HHMM-<from>-to-<to>-<topic>.md`

- 예: `20261108-1430-claude-to-codex-login-fix.md`
- `<from>`, `<to>`: 역할 이름 (`claude`, `codex`, `agy`, `janitor`, `watchdog`, `human`)
- `<topic>`: 영문 소문자와 하이픈만 사용

## 규칙
1. **append-only**: 한 번 쓴 핸드오프는 내용을 고치지 않습니다. 정정은 새 파일로 쓰고, 이전 파일에서 새 파일을 링크합니다.
2. **ACK**: 받은 쪽은 파일 끝에 `ACK: <역할> <YYYYMMDD-HHMM>` 줄을 추가하고 커밋합니다.
3. **보관**: 작업이 끝나면 `active/`에서 `archive/`로 옮깁니다 (`git mv`).
4. **형식**: [TEMPLATE.md](TEMPLATE.md)를 복사해서 씁니다.
5. **근거**: 근거는 `경로#줄 @sha8` 형식으로 적습니다.
6. **비밀 금지**: 비밀번호, 토큰, 키, 채팅 ID, 자격 정보는 적지 않습니다.
7. **범위**: `active/`에는 진행 중인 파일만 둡니다. 오래된 파일 정리는 [정리 담당 역할](../ROLE-janitor.md)이 맡습니다.

## 폴더
- `active/`: 진행 중 핸드오프
- `archive/`: 끝난 핸드오프

## 절차 요약
1. 보내는 쪽: 템플릿 복사 → 이름 짓기 → `active/`에 저장 → 커밋
2. 받는 쪽: 읽기 → ACK 줄 추가 → 커밋
3. 완료: 보내는 쪽 또는 받는 쪽이 `archive/`로 이동 → 커밋

## 관련
- [정리 담당 역할](../ROLE-janitor.md)
- [감시 담당 역할](../ROLE-watchdog.md)
- [훅 목록](../HOOKS.md)
