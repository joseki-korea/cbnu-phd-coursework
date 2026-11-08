---
id: "cbnu-phd-coursework/docs/agents/ROLE-watchdog.md"
title: "\uac10\uc2dc \ub2f4\ub2f9 (Watchdog) \uc5ed\ud560"
summary: "\uc138\uc158 \uc815\uccb4, \ub514\uc2a4\ud06c \uc5ec\uc720, \ub9e5\ub77d \uc0ac\uc6a9\ub7c9, \uaddc\uce59 \uc704\ubc18, \uc2e4\ud328 \ud14c\uc2a4\ud2b8\ub97c 5\ubd84\ub9c8\ub2e4 \ubcf4\uace0\ud558\ub294 \uc5ed\ud560 \uaddc\uce59."
domain: "cbnu-phd-coursework"
tags: ["watchdog", "monitoring", "role"]
owner: "repository maintainers"
status: DRAFT
created: "2026-11-08"
updated: "2026-11-08"
source: "docs/agents/ROLE-watchdog.md"
lang: ko
sensitivity: internal
related: ["docs/agents/ROLE-janitor.md", "docs/agents/handoffs/README.md", "docs/agents/HOOKS.md"]
---
# 감시 담당 (Watchdog) 역할

## 역할 한 줄
세션 상태를 지켜보고 문제를 알립니다. 직접 고치거나 지우지 않습니다.

## 감시 항목과 기준
| 항목 | 기준 | 조치 |
|---|---|---|
| 좌석 정체 | 20분 동안 출력 없음 | 경고 → 재촉 → 재배차 요청 |
| 디스크 여유 | 1.5GB 미만 | 경고 → janitor 정리 요청 |
| 맥락 사용량 | 40% 이상 | 담당에게 핸드오프 작성 요청 |
| 규칙 위반 | 이름 형식 어긋남, 우회 실행, 허용되지 않은 모델 사용 | 담당에게 경고 |
| 실패 테스트 | 이 레포 테스트 명령 실패 | 실패 1줄 보고 → 재배차 요청 |

## 주기
- 5분마다 한 번 점검합니다.

## 금지
- 직접 작업, 파일 수정, 커밋, 삭제
- 다른 세션의 작업 인수

## 보고 형식 (1줄)
`[WD HH:MM] <대상> <항목> <측정값> → <요청 조치>`

- 예: `[WD 14:35] ai-server-s1 정체 23분 → 재촉 요청`
- 예: `[WD 14:40] 레포 루트 디스크 1.2GB → janitor 정리 요청`

## 이 레포 감시 대상
- 테스트 명령: 실측 테스트 명령 없음
- 디스크 점검 위치: 레포 루트 및 `__pycache__/`
- 디스크 점검 명령: `df -h .`

## 관련
- [정리 담당 역할](ROLE-janitor.md)
- [핸드오프 규칙](handoffs/README.md)
- [훅 목록](HOOKS.md)
