---
id: cbnu-phd-coursework/RAG.md
title: RAG ingestion
summary: RAG ingestion for cbnu-phd-coursework.
domain: cbnu-phd-coursework
tags:
- rag
owner: repository maintainers
status: draft
created: '2026-11-08'
updated: '2026-11-08'
source: RAG.md
lang: en
sensitivity: internal
related:
- README.md
repo: cbnu-phd-coursework
device_scope: all
doc_type: rag
source_of_truth: RAG.md
---

# RAG ingestion

Use `rag-manifest.json` for indexed paths and hashes, and `.ragignore` to exclude generated, private, binary, and dependency content. Index the explicit README and manifest exceptions for media folders. Keep one topic per document, preserve provenance, and chunk long sections at ingestion. Never index secrets or personal data. Recompute hashes after documentation edits.

## Wiki

`docs/wiki/index.md` lists evidence-linked pages; `docs/wiki/SCHEMA.md` describes ingest, query, and lint. Run `python3 scripts/wiki-lint.py` and `python3 scripts/rag-manifest.py` after updates. Vector indexes are generated locally outside the repository.
