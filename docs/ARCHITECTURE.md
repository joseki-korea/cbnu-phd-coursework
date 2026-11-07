---
id: cbnu-phd-coursework/docs/ARCHITECTURE.md
title: Repository Architecture and Migration Design
repo: joseki-korea/cbnu-phd-coursework
device_scope: all
doc_type: architecture
tags:
- architecture
- directory-design
- migration-plan
status: DRAFT
updated: '2026-11-07'
source_of_truth: docs/ARCHITECTURE.md
summary: Repository Architecture and Migration Design for cbnu-phd-coursework.
domain: cbnu-phd-coursework
owner: repository maintainers
created: '2026-11-08'
source: docs/ARCHITECTURE.md
lang: en
sensitivity: internal
related:
- README.md
---

# Repository Architecture and Migration Design

## 1. Overview
This document specifies the baseline directory structure, target standard architecture, migration mappings, safety verifications, and rollback protocols for `cbnu-phd-coursework` conforming to `REPO-STANDARD-ALL-20261107`.

## 2. Baseline Architecture (CURRENT Tree)

### Tracked Root Files (origin/main)
- `<student-notebook-01>`
- `<student-notebook-02>`
- `<student-notebook-03>`
- `<student-notebook-04>`
- `<student-notebook-05>`
- `<student-notebook-06>`
- `<student-notebook-07>`
- `lab4_1_regression_activation_and_loss.ipynb`
- `lab4_2_classification_activation_and_loss.ipynb`
- `lab4_3_challenging_problems.ipynb`
- `lab4_4_techniques_for_challenging_problems.ipynb`
- `manufacturing_ai_lab2_1.ipynb`
- `manufacturing_ai_lab2_2.ipynb`

### Tracked Directory Hierarchy (origin/main, depth ≤ 3)
- None (flat root layout)

## 3. Target Standard Architecture (TARGET Tree)

### Tracked Root Files (Target)
- `.gitignore`
- `<student-notebook-01>`
- `<student-notebook-02>`
- `<student-notebook-03>`
- `<student-notebook-04>`
- `<student-notebook-05>`
- `<student-notebook-06>`
- `<student-notebook-07>`
- `README.md`
- `lab4_1_regression_activation_and_loss.ipynb`
- `lab4_2_classification_activation_and_loss.ipynb`
- `lab4_3_challenging_problems.ipynb`
- `lab4_4_techniques_for_challenging_problems.ipynb`
- `manufacturing_ai_lab2_1.ipynb`
- `manufacturing_ai_lab2_2.ipynb`
- `rag-manifest.json`

### Tracked Directory Hierarchy (Target, depth ≤ 3)
- `assets/`
- `assets/binaries/`
- `assets/components/`
- `assets/images/`
- `assets/src/`
- `assets/videos/`
- `docs/`
- `handoffs/`

## 4. Current → Target Mapping Table
Status of directory and file movements relative to `origin/main`:

| Source Baseline Path | Target Architecture Path | Migration Status | Classification / Rationale |
| :--- | :--- | :--- | :--- |
| N/A | N/A | None Staged | Canonical layout established via additive standard scaffolding |

> [!NOTE]
> All relocations staged in this PR are held in status `pending design PASS`. No additional filesystem relocations will be performed without explicit reviewer approval.

## 5. Move-Safety Validation & Grep Evidence
Verification that file relocations do not disrupt import paths, runtime execution, or build automation:

- No file relocations staged in this branch; all files retain original locations.

## 6. Migration Execution & Rollback Plan

### Migration Protocol
1. File movements are performed exclusively via `git mv` to preserve commit history.
2. Ingestible documentation files are indexed in `rag-manifest.json` with verified SHA8 signatures.
3. Build and test scripts are executed post-relocation to confirm zero functional regression.

### Rollback Commands
In the event that reviewer assessment requires reverting staged relocations, execute:
```bash
# No relocations to roll back
```
