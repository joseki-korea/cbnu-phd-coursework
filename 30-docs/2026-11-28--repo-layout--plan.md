# 실습 저장소 구획 이관 계획

기존 루트의 실습 노트북 13개를 `10-source/`로 옮긴다.
코드·셀 출력·메타데이터를 포함한 노트북 바이트와 원래 파일명은 그대로 보존한다.
이 문서는 14구획 시범의 범위·원래 위치·복구 방법을 설명한다.

기본 9구획은 00-guide, 10-source, 20-assets, 30-docs, 40-context, 50-tests, 60-config, 70-release, 90-archive다.
20-assets 아래에는 21-images, 22-design, 23-media, 24-data, 25-models를 둔다.
자료가 없는 구획은 meta.yaml에 content_state: empty로 표시한다.

## 파일과 링크

원래 위치 → 새 위치와 SHA-256은 [이동 manifest](2026-11-28--repo-layout--manifest.json)에 있다.
원문 노트북에는 로컬 Markdown 링크나 이 저장소 파일을 가리키는 외부 링크가 없었다.
새 루트·00-guide·10-source 색인에서 새 상대 경로로 연결한다. symlink나 절대 로컬 경로는 사용하지 않는다.
개인 실습본·기본 실습본은 별개 원본으로 보존하며 중복처럼 보여도 삭제하거나 합치지 않는다.

## 검증과 복구

SHA-256·JSON 구조·README 링크·YAML·Git rename·diff 공백을 검사한다.
노트북 커널·의존성 실행 및 학습 결과는 이번 구조 변경 검증에 포함하지 않는다.
복구 리허설은 독립 임시 clone에서 이관 커밋을 revert하고 index tree가 원래 base tree와 같은지 확인한다.
실제 PR의 병합·원본 main 적용·다른 레포 확대는 허브가 별도로 판단한다.

## 후속 확대

경로 하드코딩·CI·자동 실행·linked worktree·활성 변경이 없는 작은 레포를 먼저 한 곳씩 배정한다.
프레임워크·정본·자동 실행 레포는 경로 계약표와 복구 수단·실행 검증을 마련한 뒤 배정한다.
한 origin/공통 Git 저장소당 작성자 한 명과 기준 SHA를 고정한다.
