# 구글/Gemini AI 경쟁력 현황 메모 (2026.02.08)

## 모델 현황

### Gemini 3 라인업
- **Gemini 3 Pro** (2025.11): LMArena 1501 Elo (1위 달성), GPQA Diamond 91.9%
- **Gemini 3 Flash** (2026.01): Pro급 성능(GPQA 90.4%)을 저비용으로 제공
- **Gemini 3 Deep Think**: 제한적 롤아웃 중, "안전성 평가" 명목으로 수개월째 지연
- **Gemini 3 Ultra**: 출시일 미정
- **Gemini 4**: 하사비스가 "추론과 에이전시의 도약"으로 티저만 함

### 벤치마크 vs 실전
| 영역 | 1위 | Gemini 위치 |
|------|-----|-------------|
| SWE-bench (실제 코딩) | Claude 4.5 Sonnet (77.2%) | 뒤처짐 |
| 수학 추론 (AIME 2025) | GPT-5.2 (100%) | 뒤처짐 |
| LMArena Elo (종합) | Gemini 3 Pro (1501) | 1위 |
| ARC-AGI-2 | GPT-5.2 (52.9%) | Deep Think 45.1% |

**핵심**: 벤치마크는 선방하지만, 에이전트용 실전 코딩에서 Claude/GPT에 밀림

## 코딩 도구 난립

- **Gemini CLI** (v0.27): 매주 릴리스하지만 실사용 안정성 부족
- **Jules**: 비동기 코딩 에이전트, GitHub 전용. CLI 버전(Jules Tools) + API 공개
- **Antigravity**: 다중 에이전트 개발 플랫폼
- **Gemini Code Assist**: 무료 월 18만 건 코드 완성
- **Conductor**: 컨텍스트를 마크다운으로 관리하는 CLI 확장

**문제**: 제품이 너무 많고 각각 미완성. Anthropic(Claude Code)이나 OpenAI(Codex)는 하나에 집중

## 하사비스의 전략 방향

1. **멀티모달 → 옴니모델**: Gemini + Veo(비디오) + Imagen(이미지) 통합
2. **월드 모델**: 세계를 이해하고 시뮬레이션하는 모델, 하사비스가 가장 시간 투자 중
3. **에이전트**: "신뢰할 수 있는 AI 에이전트"가 2026 핵심이라고 발언

→ 장기 비전은 그럴듯하지만, 지금 시장이 원하는 "코딩 에이전트"에서는 느림

## 조직 이슈

### 인력 규모 (모델이 밀릴 이유가 없는 규모)
- Google DeepMind: ~7,000명
- Anthropic: ~3,000~4,000명
- OpenAI: ~1,600명+

### 내부 문제
- 제품 중심 전환으로 **기초 연구 인력 사기 저하** (前 직원 증언)
- Gemini 앱팀 → DeepMind 통합 (단기적으로 속도 저하 우려)
- 연구 인력 유출 ↔ 제품/응용 인력 유입 (Hume AI, Apple Siri 임원 영입)
- **대기업 비효율**: 7,000명이 1,600명보다 느린 전형적 대기업병

## 클라우드 인프라 — 아이러니한 구도

- **Anthropic이 Google Cloud TPU 최대 고객**: 수백억 달러 규모, TPU 100만 개, 1GW+ 계획
- 구글 TPU로 학습한 Claude가 Gemini를 이기는 구조
- 구글 입장에선 모델에서 지더라도 클라우드로 돈은 버는 안전장치
- Anthropic은 멀티클라우드 전략: Google TPU + AWS Trainium + NVIDIA GPU

## 투자 시사점

- 구글(Alphabet)은 AI 모델 경쟁에서 밀리더라도 **클라우드 인프라 수요**로 수혜
- "곡괭이 장사" 포지션 — AI 모델 승자가 누구든 TPU/클라우드는 팔림
- 다만 모델 경쟁력 약화 → Search/광고 시장 방어에 장기적 리스크
- Gemini 4가 반전 카드가 될 수 있으나, 구체적 일정 없음
