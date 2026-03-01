# growterm 탭별 ResponseTimer 분리

## 배경
ResponseTimer가 앱 전체에 1개뿐이라 탭 전환 시 측정이 깨지는 문제가 있었다. 탭별 독립 측정 + 탭별 시간 표시 + 전체 avg 윈도우 타이틀 표시가 필요했다.

## 변경 사항

### 1. `response_timer.rs`
- `pub fn stats(&self) -> (Duration, u32)` 추가: total_sum, count 반환 (윈도우 타이틀 전체 avg 계산용)
- `pub fn set_enabled(&mut self, enabled: bool)` 추가: 새 탭 생성 시 enabled 상태 상속용
- `MIN_DURATION_FOR_AVG` (1초) 추가: 1초 미만 응답은 avg에서 제외
- `display_text()`에 avg 카운트 표시: `"⏱ 3s avg 3s/2"`

### 2. `tab.rs`
- `Tab` 구조체에 `pub response_timer: ResponseTimer` 필드 추가
- `spawn_with_cwd()`에서 `ResponseTimer::new()` 생성
- `tab_bar_info()`: 각 탭의 `response_timer.display_text()`를 타이틀에 포함 (`"⌘1 ⏱ 3s avg 3s/1"`)

### 3. `app.rs`
- 전역 `response_timer` 제거 → `response_timer_enabled: bool`로 대체
- Enter 시: `tabs.active_tab_mut().response_timer.on_enter()` 호출
- RedrawRequested: 모든 탭 순회하며 각 탭의 `on_pty_output()` + `tick()` 호출
- ToggleResponseTimer: 모든 탭의 timer를 toggle
- 새 탭 생성 시: `tab.response_timer.set_enabled(response_timer_enabled)`로 상속
- `build_title()`: 모든 탭의 stats 합산하여 전체 avg 계산 (`"growterm | avg 3s/5"`)

## 핵심 설계 결정
- `enabled` 상태는 앱 레벨 bool + 각 탭의 ResponseTimer 내부 enabled 이중 관리
- 탭 바: 탭별 현재 상태 + 탭별 avg 표시
- 윈도우 타이틀: 전체 탭 합산 avg만 표시
- 1초 미만 응답은 avg에서 제외 (빠른 명령어가 avg를 왜곡하는 것 방지)
