---
id: cbnu-phd-coursework/wiki/schema
title: 위키 작성 규칙
summary: 수집, 질의, 점검 절차
domain: cbnu-phd-coursework
tags: [wiki, coursework]
owner: repository maintainers
status: draft
created: 2026-11-08
updated: 2026-11-08
source: docs/wiki/
lang: ko
sensitivity: internal
related: [index.md]
---

# 위키 작성 규칙

## Ingest

원본을 직접 읽고 주제별 페이지에 확인된 사실을 작성한다. 각 주장에 `[source: 경로#L줄 @sha8]`를 붙이며 sha8은 파일의 Git blob SHA-1 앞 8자리다. 비밀, 개인정보와 회사 내부 수치를 제외한다. 페이지 이름은 영문 소문자 kebab으로 정하고 정보칸을 채운다. 색인을 갱신하고 log에 추가한다.

## Query

색인과 페이지를 찾고 원본 줄과 해시를 확인해 답변에 인용한다. 근거가 없는 답변은 만들지 않는다. 재사용할 답은 원본 검증 후 수집한다.

## Lint

`python3 scripts/wiki-lint.py`로 정보칸, 색인, 인용 해시와 링크를 검사한다. 주장과 근거의 의미 일치, 민감정보 및 모순은 사람이 검토한다. `python3 scripts/rag-manifest.py`로 heading 단위 목록을 생성한다. 벡터는 저장소에 커밋하지 않는다.

## 페이지 유형

overview는 전체, modules는 폴더, concepts는 용어, entities는 대상, howto는 절차, faq는 근거 있는 질문을 다룬다. 한 페이지는 한 주제만 다룬다.
