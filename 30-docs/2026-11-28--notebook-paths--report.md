# 노트북 경로 조사·이동 영향·검증 보고

이전의 “경로 패턴 0”은 Orca·Colab 경로만 찾은 제한된 스캔 결과를 전체 경로처럼 보고한 오류였다.
실제 원본에는 `.mat` 상위 상대경로 탐색 4개, Windows 조건부 폰트 경로 2개, CWD 다운로드 2개가 있다.
이번 보완은 4개 노트북의 `find_data_file` 탐색 경로만 바꾸며 셀 출력·노트북 메타데이터·나머지 코드는 보존한다.

## 원본에서 확인한 경로와 영향

| 원본 패턴 | 노트북·셀 | 기존 동작과 이동 영향 |
|---|---|---|
| `filename`, `../filename`, `../../filename` | lab4_1 cell 4, lab4_2 cell 7과 두 접두사본 = 4개 | CWD에서 최대 2단계 상위를 탐색. 노트북이 `10-source/`로 한 단계 내려가면 옛 레포 루트의 2단계 상위 자료를 놓칠 수 있음 |
| `cwru_normal.mat`, `cwru_fault_inner.mat`, `cwru_fault_outer.mat`, `cwru_fault_ball.mat` | lab4_1은 정상·내륜, lab4_2는 cell 7·13에서 정상·세 고장 클래스 | 파일을 못 찾으면 회귀의 RMS 기본값·분류의 합성 데이터 fallback 사용 |
| `C:/Windows/Fonts/malgun.ttf` | manufacturing_ai_lab2_1·lab2_2 cell 1 = 2개 | Windows 분기 + exists 검사로 보호. 폰트가 없으면 이름 기반 fallback, Darwin/Linux는 별도 폰트 분기. 이번 이관과 무관한 시스템 경로라 수정하지 않음 |
| `urlretrieve(url, filename)` | manufacturing_ai_lab2_1·lab2_2 cell 2 = 2개 | CWD에 `cwru_normal.mat`·`cwru_fault.mat`를 캐시. 네트워크 실패 시 합성 신호 fallback. `10-source/`에서 실행하면 그 폴더에 생성될 수 있으며 이 동작은 보존 |

기본본과 접두사본 lab4_1~4는 각각 바이트 동일쌍이다. 1·2의 두 쌍에는 같은 경로 수정,
3·4의 두 쌍에는 원문 보존을 적용해 현재도 네 쌍 모두 동일하다.

## 최소 경로 수정

기존 `filename`, `..`, `../..` 우선순위는 유지한다.
CWD 이름이 `10-source`인 경우에만 `../../..`를 추가해 이관 전 레포 루트에서의 2단계 상위를 유지한다.
표준 데이터 구획 `20-assets/24-data` 및 `../20-assets/24-data`도 탐색해 루트·10-source 두 CWD에서 찾는다.
사용자 홈·체크아웃 절대경로를 새로 하드코딩하지 않는다. 기존 파일을 못 찾으면 여전히 None을 반환한다.

실제 이관 파일 13개 중 **9개는 바이트 동일**, **4개는 한 셀의 탐색 함수만 수정**했다.
원래 SHA-256·현재 SHA-256과 변경 사유는 [manifest](2026-11-28--repo-layout--manifest.json)에 각각 기록한다.
원문 `.mat` 파일은 이 저장소에 추적돼 있지 않으며, 현재 checkout의 직접·상위·표준 데이터 후보에도 없었다.

## 실행한 검증

```text
python3 50-tests/verify_schema.py
python3 50-tests/verify_paths.py
```

- 경로 helper 네 개를 AST로 추출해 독립 실행했다. 루트·10-source CWD에서 실제 임시 파일 144건을 올바르게 선택·열었다.
- 파일 부재 32건에서 None, 회귀·이진/다중 분류 fallback 분기 6건을 확인했다.
- Windows 폰트 존재/부재·Darwin·Linux 분기 8건을 확인했다. 실제 Windows 폰트 설치를 실행한 검증은 아니다.
- CWD별 캐시 사용·오프라인 fallback 8건을 확인했고 실제 네트워크 요청은 하지 않았다.
- fallback의 수치 연산·SciPy 로더·폰트·네트워크는 결정적인 stub으로 대체했다. 실제 MAT 파싱·전체 학습·노트북 커널 실행을 주장하지 않는다.

기록: [경로 검사](../50-tests/2026-11-28--notebook-paths--check.json),
[스키마 검사](../50-tests/2026-11-28--metadata-schema--check.json),
[종합 검사](../50-tests/2026-11-28--repo-layout--check.json).
