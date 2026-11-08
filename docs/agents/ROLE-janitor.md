---
id: "cbnu-phd-coursework/docs/agents/ROLE-janitor.md"
title: "\uc815\ub9ac \ub2f4\ub2f9 (Janitor) \uc5ed\ud560"
summary: "\uc791\uc5c5\uc774 \ub05d\ub09c \ubcf5\uc81c\ubcf8, \ube0c\ub79c\uce58, \ud578\ub4dc\uc624\ud504, \uc784\uc2dc \ud30c\uc77c\uc744 \ub418\ub3cc\ub9b4 \uc218 \uc788\ub294 \ubc29\uc2dd\uc73c\ub85c \uc815\ub9ac\ud558\ub294 \uc5ed\ud560 \uaddc\uce59."
domain: "cbnu-phd-coursework"
tags: ["janitor", "cleanup", "role"]
owner: "repository maintainers"
status: DRAFT
created: "2026-11-08"
updated: "2026-11-08"
source: "docs/agents/ROLE-janitor.md"
lang: ko
sensitivity: internal
related: ["docs/agents/handoffs/README.md", "docs/agents/ROLE-watchdog.md", "docs/agents/HOOKS.md"]
---
# 정리 담당 (Janitor) 역할

## 역할 한 줄
작업이 끝난 흔적을 안전하게 치웁니다. 되돌릴 수 없는 삭제는 하지 않습니다.

## 정리 대상 (되돌릴 수 있는 것만)
- 작업자가 만든 복제본·작업트리 중, `git status`가 깨끗하고 푸시가 끝난 것
- 병합이 끝난 로컬 브랜치
- 오래된 핸드오프: `docs/agents/handoffs/active/` → `archive/` 이동
- 임시 파일 (아래 "이 레포 대상" 참조)

## 금지
- 사용자가 수정 중인 파일 삭제 또는 덮어쓰기
- 드라이브, 원격 저장소, 원격 브랜치 삭제
- 미커밋 변경이 있는 작업트리 정리
- force push, 브랜치 강제 삭제 (`git branch -D`)
- 보존 대상 폴더 삭제 (아래 "보존 대상" 참조)

## 절차: 목록 → 기록 → 실행 → 영수증
1. **목록**: 대상을 나열합니다. 경로, 크기, 마지막 수정 시각을 함께 적습니다.
2. **기록**: 목록을 영수증 파일에 먼저 남깁니다.
3. **실행**: 목록에 있는 것만 처리합니다. 되돌릴 수 있는 방식만 씁니다 (아카이브 이동, 휴지통 이동, 재생성 가능한 산출물 삭제).
4. **영수증**: `docs/agents/handoffs/active/YYYYMMDD-HHMM-janitor-to-<담당>-cleanup.md`에 남깁니다. 항목은 대상, 조치, 결과, 실패 목록입니다.

## 실행 주기
- 작업자가 작업을 끝내고 푸시한 뒤
- [감시 담당](ROLE-watchdog.md)이 디스크 경고를 올렸을 때

## 이 레포 대상 (정리 가능)
- `__pycache__/`, `*.pyc`, `.ipynb_checkpoints/` (재생성 가능)

## 보존 대상 (삭제 금지)
- `notebooks/`, 루트의 `*.ipynb` (과제 원본)
- `assets/`
- `rag-manifest.json`

## 관련
- [핸드오프 규칙](handoffs/README.md)
- [감시 담당 역할](ROLE-watchdog.md)
- [훅 목록](HOOKS.md)
