# 검사·증거

표준 23키 메타 스키마와 상대 데이터 경로·fallback을 검사하는 스크립트다.
구조·원문 보존·스키마·경로 검사 JSON을 보관한다.
전체 노트북 학습·실제 MAT 파싱·Windows 설치 검증을 대신하지 않는다.

상태: populated / indexed.
진입: 메타 스키마·상대경로·링크·복구 결과를 재검증할 때
이탈: [상위 색인](../README.md)으로 돌아간다.
키워드: 스키마, 로컬링크, 경로테스트, 복구, 원문보존. [메타](meta.yaml).

| 하위 항목 | 내용·진입 조건 |
|---|---|
| [2026-11-28--metadata-schema--check.json](2026-11-28--metadata-schema--check.json) | 15개 메타의 표준 23키·탐색 경로·상태 검사 결과 |
| [2026-11-28--notebook-paths--check.json](2026-11-28--notebook-paths--check.json) | 임시 파일 경로 선택과 조건부 fallback 검사 결과 |
| [2026-11-28--repo-layout--check.json](2026-11-28--repo-layout--check.json) | 원문·수정 범위·링크·rename 종합 검사 결과 |
| [verify_paths.py](verify_paths.py) | Python 3 표준 라이브러리만으로 추출 helper·guard·fallback 검사 |
| [verify_schema.py](verify_schema.py) | Python 3 + Ruby YAML 파서로 표준 메타·로컬 탐색 검사 |

검사: `python3 50-tests/verify_schema.py`는 Python 3와 Ruby 표준 YAML 파서, `python3 50-tests/verify_paths.py`는 Python 표준 라이브러리만 필요하다. 저장소 루트에서 실행한다.

관련 자료: [이관 근거·검증 범위 또는 원본 실습 위치](../30-docs/2026-11-28--repo-layout--plan.md)
