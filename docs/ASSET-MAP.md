---
id: cbnu-phd-coursework/docs/ASSET-MAP.md
title: Asset Mapping and Semantic Migration Plan
repo: joseki-korea/cbnu-phd-coursework
device_scope: all
doc_type: architecture
tags:
- architecture
- assets
- semantic-reorg
status: DRAFT
updated: '2026-11-07'
source_of_truth: docs/ASSET-MAP.md
summary: Asset Mapping and Semantic Migration Plan for cbnu-phd-coursework.
domain: cbnu-phd-coursework
owner: repository maintainers
created: '2026-11-08'
source: docs/ASSET-MAP.md
lang: en
sensitivity: internal
related:
- README.md
---

# Asset Mapping & Semantic Reorganization Plan — cbnu-phd-coursework

본 문서는 `cbnu-phd-coursework` 레포지토리의 소스코드 및 에셋을 기능/모듈별로 시맨틱하게 재구성하기 위한 이동 계획 설계 테이블입니다.
**주의: 본 계획은 설계 단계(DESIGN ONLY)이며, 3자 검토자(Reviewer) PASS 이전까지는 실제 `git mv` 이동 작업을 일절 수행하지 않습니다 (0 moves executed).**

## 1. 시맨틱 이동 계획 테이블 (Semantic Move Plan Table)

| 원본 경로 (Source) | 목표 경로 (Target) | 모듈 성격 및 목적 | 진행 상태 |
|---|---|---|---|
| `<student-notebook-01>` | `notebooks/<student-notebook-01>` | 회귀 분석 및 손실함수 실습 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-02>` | `notebooks/<student-notebook-02>` | 분류 활성화 함수 실습 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-03>` | `notebooks/<student-notebook-03>` | 도전 과제 심화 실습 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-04>` | `notebooks/<student-notebook-04>` | 심화 최적화 기법 실습 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-05>` | `notebooks/<student-notebook-05>` | 선형 회귀 모델 구현 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-06>` | `notebooks/<student-notebook-06>` | 로지스틱 회귀 모델 구현 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `<student-notebook-07>` | `notebooks/<student-notebook-07>` | MNIST 신경망 분류 실습 (CEO decision: rename/private) | **PLANNED (DESIGN ONLY — 0 executed)** |
| `lab4_1_regression_activation_and_loss.ipynb` | `notebooks/templates/lab4_1.ipynb` | 표준 회귀 실습 템플릿 | **PLANNED (DESIGN ONLY — 0 executed)** |
| `lab4_2_classification_activation_and_loss.ipynb` | `notebooks/templates/lab4_2.ipynb` | 표준 분류 실습 템플릿 | **PLANNED (DESIGN ONLY — 0 executed)** |
| `manufacturing_ai_lab2_1.ipynb` | `notebooks/manufacturing/lab2_1.ipynb` | 제조 AI 머신러닝 실습 1 | **PLANNED (DESIGN ONLY — 0 executed)** |
| `manufacturing_ai_lab2_2.ipynb` | `notebooks/manufacturing/lab2_2.ipynb` | 제조 AI 머신러닝 실습 2 | **PLANNED (DESIGN ONLY — 0 executed)** |

## 2. 참조 갱신 계획 (Reference-Update Plan)
- 상기 이동 계획 실행 시 임포트 경로 및 관련 문서 상호 링크를 일괄 동기화할 예정입니다.
- 정적 리소스 및 빌드 설정 파일의 상대 경로 무결성을 사전에 검증합니다.

## 3. 빌드 및 테스트 검증 프로토콜 (Build/Test Verification Commands)
```bash
# 1. 파일 이동 전/후 무결성 검증 (Git 변경 요약)
git diff -M --summary origin/main

# 2. RAG 매니페스트 및 프론트엔드/백엔드 구동 검증
python3 -c "import json; json.load(open('rag-manifest.json'))"
```
