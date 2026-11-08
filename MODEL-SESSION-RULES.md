# MODEL-SESSION-RULES

## Status
DRAFT

## Inheritance
전역 vault 규칙 → 이 파일 순서로 상속한다. 지역 규칙은 전역 규칙을 완화할 수 없다.

## Model placement
Main 및 persona 세션은 Claude Opus를 사용한다. 작업 좌석은 Codex Terra, Antigravity (AGY), Claude Haiku를 병렬로 사용하며 저장소 또는 파일마다 한 좌석만 담당한다.

## Naming
`<device4>-<session4>-<model>-<role>` (예: `NWKW-a1b2-terra-fix`).

## Context
컨텍스트가 40% 이상이거나 자동 압축(auto-compaction)이 한 번 발생하면 `handoffs/active/`에 역할, 진행, 대기, 다음 단계, 원장 경로를 2000 토큰 이하로 기록한다. 후임 좌석이 이어받고 기존 좌석은 대기한다. 슬래시 리셋(slash-reset) 주입은 하지 않는다.

## Approval
merge, force push, deploy, delete는 CEO 승인 후 진행한다.
