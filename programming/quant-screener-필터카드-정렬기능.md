# 퀀트 스크리너: 필터 카드화 + PER/ROE 정렬 기능

## 변경 사항

### 1. 필터 토글 카드화
- 기존: 탭 위에 체크박스가 따로 떠 있는 형태
- 변경: `.formulas`와 동일한 카드 스타일 적용 (흰색 배경, 테두리, 둥근 모서리)
- "필터" 타이틀 추가

### 2. PER/ROE 컬럼 정렬 기능
- 모든 6개 탭(종합2025, Ultra2025, DCF2025, DCF2024, MF2025, MF2024)에 적용
- PER/ROE 헤더 클릭 시 정렬:
  - 1번 클릭: 오름차순 (▲)
  - 2번 클릭: 내림차순 (▼)
  - 3번 클릭: 정렬 해제 (원래 순서 복귀)
- `-` 값은 `Infinity`로 처리하여 맨 뒤로 보냄

## 구현 포인트

- `sortState` 객체로 탭별 정렬 상태 관리
- `parseNum()`: `-`, `N/A`, `%` 등을 처리하는 숫자 파싱
- `colIdx`: 탭별로 다른 PER/ROE 배열 인덱스 매핑
  - ultra/dcf: PER=8, ROE=9
  - mf: PER=7, ROE=8
  - total: 객체 속성 (`r.per`, `r.roe`)
- `doSort()` → `renderAll()` → 각 render 함수에서 `sortData()` 적용
- CSS: `th.sortable` 클래스로 커서, 호버, 화살표 표시
