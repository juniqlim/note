# claude-skin 디스플레이 버그 수정

## 수정한 문제들

### 1. 긴 답변 시 화면 깨짐
- **원인**: `maxOutputLines`가 `rows - 6`으로 라인 개수만 세고, wrap되어 여러 행을 차지하는 긴 라인을 고려하지 않음
- **해결**: `wrappedLineCount`를 활용한 `visibleLines` 함수 추가. 뒤에서부터 각 라인이 실제로 차지하는 터미널 행 수를 계산하여 화면에 맞는 만큼만 선택

### 2. 이전 입력 프롬프트 색상
- `> `로 시작하는 이전 입력 라인에 `<Text color="green" dimColor>` 적용
- 활성 프롬프트(green bold)보다 어둡게 표시

### 3. 답변-질문 사이 간격 + 커서 위치
- output에 빈 줄 `""` 추가하여 간격 생성
- Ink에서 빈 문자열 `<Text>{""}</Text>`가 0 height로 렌더링되는 문제 → `line || " "` 처리
- `wrappedLineCount("")`가 1을 반환하므로 커서 계산과 렌더링이 일치

## 핵심 교훈
- Ink의 `<Text>{""}</Text>`는 높이 0으로 렌더링될 수 있지만, `wrappedLineCount`는 1로 계산 → 커서 위치 불일치 발생
- `<Box marginTop={1}>`로 감싸면 추가 공간이 생겨 커서 계산과 불일치
- 렌더링과 커서 계산이 동일한 데이터 모델을 사용해야 위치가 맞음
