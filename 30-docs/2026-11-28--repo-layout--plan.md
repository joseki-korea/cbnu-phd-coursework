# 실습 저장소 구획 이관 계획

기존 루트의 실습 노트북 13개를 `10-source/`로 옮긴다.
원래 파일명을 보존한다. 9개는 원문 바이트 그대로이며, 4개는 이동으로 달라진 데이터 탐색 경로만 최소 수정한다.
13개 모두 셀 출력·노트북 메타데이터·탐색 함수 외 코드는 보존한다.
이 문서는 14구획 시범의 범위·원래 위치·복구 방법을 설명한다.

기본 9구획은 00-guide, 10-source, 20-assets, 30-docs, 40-context, 50-tests, 60-config, 70-release, 90-archive다.
20-assets 아래에는 21-images, 22-design, 23-media, 24-data, 25-models를 둔다.
자료가 없는 구획은 meta.yaml에 content_state: empty로 표시한다.

## 파일과 링크

원래 위치 → 새 위치와 SHA-256은 [이동 manifest](2026-11-28--repo-layout--manifest.json)에 있다.
원문 노트북에는 로컬 Markdown 링크나 이 저장소 파일을 가리키는 외부 링크가 없었다.
그러나 `.mat` 상위 상대경로 탐색 4개와 조건부 Windows 폰트 경로 2개, CWD 다운로드 2개가 있었으므로
앞선 “경로 패턴 0” 보고를 정정한다. [경로 보고서](2026-11-28--notebook-paths--report.md)에 영향·fallback·검증을 기록했다.
새 루트·00-guide·10-source 색인에서 새 상대 경로로 연결한다. symlink나 절대 로컬 경로는 사용하지 않는다.
lab4_1~4 접두사본/기본본 네 쌍은 현재 바이트 동일본이며 삭제하거나 합치지 않는다.
`aliases`는 이관 전 레포 루트 기준의 이력 경로이며 활성 children 링크가 아니다.
빈 구획과 새 안내·문서는 `migration_state: indexed`, 실제 노트북 이관 대상인 루트·10-source는 `migrated`로 표기한다.

## 검증과 복구

원래/현재 SHA-256·JSON 구조·README 링크·표준 23키 YAML·Git rename·diff 공백을 검사한다.
4개 수정 노트북은 함수 탐색 경로만 바뀌었는지 JSON 구조를 대조하고, 임시 파일로 실제 경로 선택과 fallback을 검사한다.
노트북 커널·의존성 실행 및 학습 결과는 이번 구조 변경 검증에 포함하지 않는다.
복구 리허설은 독립 임시 clone에서 보완 커밋부터 이관 커밋까지 역순 revert하고 index tree가 원래 base tree와 같은지 확인한다.
실제 PR의 병합·원본 main 적용·다른 레포 확대는 허브가 별도로 판단한다.

## 후속 확대

경로 하드코딩·CI·자동 실행·linked worktree·활성 변경이 없는 작은 레포를 먼저 한 곳씩 배정한다.
프레임워크·정본·자동 실행 레포는 경로 계약표와 복구 수단·실행 검증을 마련한 뒤 배정한다.
한 origin/공통 Git 저장소당 작성자 한 명과 기준 SHA를 고정한다.
