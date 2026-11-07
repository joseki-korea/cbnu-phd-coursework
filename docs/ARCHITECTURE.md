---
id: cbnu-phd-coursework/docs/ARCHITECTURE.md
title: "Repository Architecture and Migration Design"
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
---

# Repository Architecture and Migration Design

## 1. Overview
This document specifies the current baseline directory structure, target standard architecture, migration mappings, safety verifications, and rollback protocols for `cbnu-phd-coursework`.

## 2. Baseline Architecture (CURRENT Tree)
Pre-migration directory layout on default branch `origin/main` (depth ≤ 3):

- Root directory only (no subdirectories in origin default branch)

## 3. Target Standard Architecture (TARGET Tree)
Target directory structure conforming to `REPO-STANDARD-ALL-20261107`:

- `assets/`
- `assets/binaries/`
- `assets/components/`
- `assets/images/`
- `assets/videos/`
- `assets/src/`
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
