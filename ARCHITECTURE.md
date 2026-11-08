---
id: cbnu-phd-coursework/ARCHITECTURE.md
title: Repository Architecture Pointer
repo: joseki-korea/cbnu-phd-coursework
device_scope: all
doc_type: architecture
tags:
- architecture
- pointer
status: DRAFT
updated: '2026-11-07'
source_of_truth: docs/ARCHITECTURE.md
summary: Repository Architecture Pointer for cbnu-phd-coursework.
domain: cbnu-phd-coursework
owner: repository maintainers
created: '2026-11-08'
source: ARCHITECTURE.md
lang: en
sensitivity: internal
related:
- README.md
---

# Repository Architecture — cbnu-phd-coursework

본 문서는 `cbnu-phd-coursework` 레포지토리의 아키텍처 및 디렉토리 구조에 대한 상위 요약 및 포인터입니다.

## 1. 아키텍처 요약
- **핵심 역할**: 충북대학교 산업AI 박사과정 연구 및 실습 과제 저장소
- **주요 구성 (Top-level directories)**:
  - `.github/`: 워크플로우 및 PR 템플릿
  - `assets/`: 이미지, 바이너리, 비디오 및 UI 컴포넌트 관리
  - `docs/`: 표준 규칙, 멀티에이전트 역할, 아키텍처 설계, 자산 맵 및 위키
  - `handoffs/`: 세션 인수인계 및 운영 기록 (active/archive)
  - `notebooks/`: 강의 실습 및 과제 Jupyter 노트북
  - `scripts/`: RAG 매니페스트 및 위키 린트 스크립트

## 2. 정본 문서 안내
상세한 디렉토리 레이아웃, Current→Target 매핑, 시맨틱 재구성 설계 및 롤백 계획은 아래 정본 문서를 참고하십시오:
👉 **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**
