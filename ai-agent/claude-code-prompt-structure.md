# Claude Code 프롬프트 구성

Claude Code는 단일 프롬프트가 아닌 110개 이상의 모듈형 컴포넌트를 환경과 설정에 따라 동적으로 조합한다. 0~8번 전체를 합치면 **~20.5K 토큰** 규모가 되며(`/context` 실측, MCP 미사용 기준), 그 중 도구 정의(~16.7K)가 대부분을 차지한다.

## 주요 구성 요소 (조합 순서)

| 순서 | 구성 요소 | 설명 |
|------|-----------|------|
| 0 | 모델 기초 프롬프트 (추정 수천 토큰) | Anthropic이 모델에 내장한 기본 지시 (안전, 톤, 정체성 등) |
| 1 | 메인 시스템 프롬프트 (~269 토큰) | Claude Code의 핵심 정체성. 변수(`${SECURITY_POLICY}` 등) 확장 포함 |
| 2 | 환경별 조건 섹션 | 로컬/클라우드 등 실행 환경에 따라 추가 |
| 3 | 도구 정의 (18개 내장 도구) | Write, Bash, Read, Edit, Glob, Grep 등 각 도구의 사용법 |
| 4 | 시스템 리마인더 (~40개) | 상태 변화에 따라 삽입되는 컨텍스트 지시 |
| 5 | CLAUDE.md 지시사항 | 3단계 스코프에서 로드 |
| 6 | MCP 도구 정의 | 연결된 MCP 서버의 도구들 (컨텍스트 비용 큼) |
| 7 | 대화 히스토리 | 메시지, 도구 결과, 파일 내용 등 |
| 8 | 출력 스타일/커스텀 지시 | 포맷팅, 톤 설정 |

## CLAUDE.md 로드 스코프 (우선순위 순)

1. **Managed** — 기업 정책 (오버라이드 불가)
2. **CLI 인자** — `--append-system-prompt` 등
3. **Local** — `.claude/*.local.*` (개인 프로젝트 설정)
4. **Project** — `.claude/CLAUDE.md` (팀 공유)
5. **User** — `~/.claude/CLAUDE.md` (전역 개인 설정)

## 컨텍스트 관리

컨텍스트 윈도우가 한계에 가까워지면 자동으로:

- 오래된 도구 출력부터 제거
- 대화 히스토리 요약 (compaction)
- CLAUDE.md 지시사항은 보존됨

### 주의도 유지 순서 (추정)

```
가장 잘 유지됨
  ↑ 0. 모델 기초 프롬프트    — 모델 자체에 내재화 + 컨텍스트 최상단
  │ 1. 메인 시스템 프롬프트   — system role, 최상단
  │ 2. 환경별 조건 섹션      — 시스템 프롬프트와 함께 상단 배치
  │ 3. 도구 정의            — 매 호출마다 참조
  │ 4. 시스템 리마인더       — 대화 중간에 반복 주입 (recency 효과)
  │ 8. 출력 스타일/커스텀 지시 — 시스템 레벨 설정
  │ 5. CLAUDE.md           — 보존되지만 중간 위치
  │ 6. MCP 도구 정의        — 외부 서버 의존, 컨텍스트 비용 큼
  │ 7. 대화 히스토리         — compaction 시 요약됨
  ↓    오래된 도구 출력      — 가장 먼저 제거됨
가장 먼저 까먹음
```

- **위치 효과**: 컨텍스트 앞(primacy)과 끝(recency)이 중간보다 주의도 높음 ("lost in the middle" 현상)
- **반복 효과**: 시스템 리마인더가 ~40개인 이유. 핵심 규칙을 대화 중간에 반복 주입하여 망각 방지
- **실용 팁**: CLAUDE.md 규칙은 짧고 핵심적으로 작성할수록 잘 지켜짐. 길수록 중간 내용이 묻힘

## 서브에이전트 (Task)

서브에이전트는 별도의 컨텍스트 윈도우를 받으며, Plan/Explore/Bash 등 에이전트 유형별로 전용 시스템 프롬프트가 추가된다.

## 모델 기초 프롬프트 (Model System Prompt)

Claude Code 프롬프트와 별개로, Anthropic이 모델 자체에 내장하는 **기초 시스템 프롬프트**가 존재한다. claude.ai, API, Claude Code 등 어떤 인터페이스에서든 동일하게 적용된다.

### 프롬프트 2겹 구조

```
[모델 기초 프롬프트]  ← Anthropic이 모델에 내장 (claude.ai에서도 동일)
  └─ [Claude Code 프롬프트]  ← Claude Code 전용 (110개+ 모듈 조합)
```

### 모델 기초 프롬프트 주요 내용

- 모델 정체성 (이름, 제작사, 지식 커트오프 날짜)
- 안전 가이드라인 (아동 안전, 무기 정보 거부, 악성코드 거부 등)
- 톤/스타일 지침 (친절, 과도한 포매팅 금지)
- 제품별 접근 방법 안내 (웹, API, Claude Code, Chrome 확장 등)
- 정치적 균형성, 사용자 웰빙 고려

### 모델별 차이

| 모델 | 지식 커트오프 |
|------|-------------|
| Opus 4.6 | 2025년 5월 |
| Sonnet 4.5 | 2025년 4월 |
| Haiku 4.5 | 2025년 1월 |

- Anthropic이 [공식 문서](https://platform.claude.com/docs/en/release-notes/system-prompts)에서 모델별 기초 프롬프트를 공개하고 있음
- 모델 버전이 올라갈 때마다 기초 프롬프트도 함께 업데이트됨

### 토큰 규모 추정

- 정확한 토큰 수는 미공개이나, claude.ai에서 도구 포함 전체 시스템 프롬프트가 **~24,000 토큰**이라는 측정치가 있음 ([HN](https://news.ycombinator.com/item?id=43909409))
- 이 중 검색 도구 지시사항만 **6,471 토큰** ([Simon Willison](https://simonwillison.net/2025/May/25/claude-4-system-prompt/))
- 순수 기초 프롬프트(안전, 톤, 정체성)는 **수천 토큰 수준**으로 추정
- 비교: OpenAI Codex도 상황별로 여러 프롬프트를 조합하는 구조 ([GitHub에 공개](https://github.com/openai/codex))
  - 메인 프롬프트: ~24KB, 약 520줄/5,800단어 (약 6,000토큰). 코드 리뷰(6KB), 권한/샌드박스, 모델별 변형 등 별도 파일 존재
  - 참고: Claude Code 메인 시스템 프롬프트는 26줄 (~269토큰). 단순 비교하면 Codex가 20배 길지만, Claude Code는 도구 정의·리마인더 등을 별도 모듈로 분리한 구조 차이

### 실측 비교 (2026.02.10)

각 CLI의 내장 토큰 사용량 명령으로 측정했다.
- **Claude Code**: 세션 초반 `/context` 실행. Messages 8토큰 시점에서 System prompt 3.8K + System tools 16.7K = ~20.5K.
- **Codex CLI**: 새 세션에서 "hi" 1회 전송 후 `/status` 실행. Context window 8.63K used / 258K.

| 제품 | 시스템 프롬프트+도구 | 컨텍스트 윈도우 | 점유율 | 측정 방법 |
|------|-------------------|---------------|-------|----------|
| **Claude Code** | **~20.5K** | 200K | 10.3% | `/context` |
| **Codex CLI** | **~8.6K** | 258K | 3.3% | `/status` |
| Claude Chat (claude.ai) | ~24K | — | — | 외부 측정 (HN) |

- Claude Code는 도구 정의(~16.7K)가 전체의 80%를 차지. 도구마다 git commit 절차, PR 생성 등 세밀한 행동 규칙이 포함되어 있어 길다.
- Codex는 프롬프트가 짧은 대신, 모델(gpt-5.3-codex) 자체의 내재화된 능력에 더 의존하는 설계로 보인다.
- 매 질의마다 대화 히스토리 전체가 시스템 프롬프트와 함께 재전송되므로, 시스템 프롬프트 크기 차이(~12K)는 대화가 길어질수록 누적 비용에 영향을 준다.

## 출처

- Claude Code 시스템 프롬프트 버전별 변경 이력: [Piebald-AI/claude-code-system-prompts](https://github.com/Piebald-AI/claude-code-system-prompts)
- 모델 기초 프롬프트 공식 공개: [Anthropic System Prompts](https://platform.claude.com/docs/en/release-notes/system-prompts)
- Claude Code 메인 시스템 프롬프트 원문: [system-prompt-main-system-prompt.md](https://github.com/Piebald-AI/claude-code-system-prompts/blob/main/system-prompts/system-prompt-main-system-prompt.md)
- claude.ai 전체 시스템 프롬프트 ~24,000 토큰 측정: [Hacker News](https://news.ycombinator.com/item?id=43909409)
- Claude 4 시스템 프롬프트 분석 (검색 도구 6,471토큰): [Simon Willison](https://simonwillison.net/2025/May/25/claude-4-system-prompt/)
- OpenAI Codex 프롬프트 (GitHub 공개): [openai/codex](https://github.com/openai/codex)
- "Lost in the middle" 현상: [Liu et al., 2023](https://arxiv.org/abs/2307.03172)
