# SK하이닉스를 넘어서 — 대안 후보 점검 (2026.02 스냅샷)

> **⚠ 데이터 기준일 2026-02-08.** 이 문서의 기준점 "하이닉스 fPER 8배"는 **현재 26F ~4.2배**다. 비교 구도의 절대 수준은 바뀌었고, **상대 순서는 대체로 유지**된다.
> **수치 출처는 `ai-밸류체인.md`** — 시총·배수·성장률은 그쪽이 단일 출처다. 이 문서는 **"하이닉스 대비 어떤가"라는 판정만** 갖는다.

**질문**: SK하이닉스(fPER 8배, HBM 57~62%)를 이기려면 무엇이 필요한가?

**답: 이기는 후보는 없다. 분산할 후보는 있다.**

하이닉스의 매력은 네 가지가 겹쳐서 나온다 — ① fPER 8x 최저 ② 어떤 칩(GPU/TPU/ASIC/Cerebras)이든 HBM은 필요 ③ 3사 과점 1위 ④ 2026년 완판. 아래 후보들은 이 중 **하나씩만** 갖는다.

---

## 1. 밸류체인 문서에 없는 후보

`ai-밸류체인.md`가 다루지 않는 영역만 여기 둔다.

### 추론 전용 칩 — 투자 경로가 거의 닫혔다

| 회사 | 상태 | 투자 경로 |
|---|---|---|
| **Cerebras** | 시리즈 H $1B 조달, 밸류 **$23B**(2026.02.04, Tiger Global 주도). **Q2 2026 IPO 목표** | 유일하게 열려 있음 |
| **Groq** | **NVIDIA가 ~$20B에 인수**(2025.12.24). 독립 존속하나 실질 산하 | 없음 (NVDA 간접) |
| **SambaNova** | Intel이 ~$1.6B 인수 협상 중 | 없음 (INTC 간접) |

Cerebras는 2024년 9월 첫 IPO 시도가 G42(UAE) 국가안보 이슈로 연기됐다가 CFIUS 승인 후 재추진 중이다. 매출 미공개라 P/S 추정 불가.

> **판정**: **하이닉스와 보완 관계이지 대체 관계가 아니다.** 추론 전용 칩이 GPU를 대체해도 HBM/DRAM은 그대로 필요하다. 3사 중 살 수 있는 건 Cerebras 하나뿐이고, 그마저 매출 불투명 + 상장 초기 변동성.

### 한국 종목 — 하이닉스를 대체할 후보 없음

| 종목 | fPER | 판정 |
|---|---|---|
| **한미반도체** (042700) | ~53x | TC 본더 세계 1위, 하이닉스에 공급. 2024 매출 +251%, 2026 목표 2조원. HBM4 775um 대응, 생산능력 420대. **성장이 이미 가격에** + 고객 다변화 부족 + **하이브리드 본딩 전환 시 기술 리스크** |
| **삼성전자** (005930) | ~10x | 하이닉스와 비슷하게 싸다. Google이 삼성 HBM4를 TPU에 인증 → 할인을 프리미엄으로 되돌릴 가능성. 다만 HBM 열위 + 사업 분산이 희석 요인 |
| **SK스퀘어** (402340) | — | 하이닉스 지분 20.07%. **하이닉스를 지주사 할인으로 사는 경로**. 단 2026-08 기준 **근거 약화** — AI컴퍼니 출자에서 빠져 희석만 맞고, 중복상장 3%룰로 의결권까지 잘림 (`hynix.md` §20 솔리다임 프리IPO) |
| 코리아써킷 / 네이버 | — | 메모리 부족 수혜 / AI GPU 1조 투자. 반도체 순수 플레이 아님 |

> **판정**: 한미반도체는 비싸고, 삼성은 열위이고, SK스퀘어는 하이닉스의 할인 버전이다. **셋 다 하이닉스를 이기지 못한다.**

### 반도체 장비 — 메모리 사이클보다 선행한다

| 종목 | fPER | 포인트 |
|---|---|---|
| **Lam Research** (LRCX) | ~23x | HBM 필수 공정(TSV·에칭·증착). **HBM 8-high → 12 → 16으로 갈수록 공정 복잡도↑ = 장비 수요↑**. 첨단 패키징 매출 2025년 $3B(3배). DRAM이 시스템의 23%(역대 최고) |
| **Applied Materials** (AMAT) | ~19x | Lam과 유사 포지션, 사업이 더 분산. 약간 저렴 |

> **판정**: **장비는 선행 투자라 메모리 사이클 리스크가 상대적으로 작다** — 하이닉스가 못 가진 유일한 장점. 다만 WFE 시장 자체의 사이클은 있다.

### Cloudflare (NET) — 에이전트 인프라, 수익성 미증명

적자. 2026 매출 ~$2.6B 전망. "Clawdbot" 바이럴로 Workers 플랫폼이 에이전트 배포 환경으로 부상. 테제는 검증됐으나 **수익성이 없고 AWS/Vercel과 경쟁**한다.

### ETF

| ETF | 비용 | 성격 |
|---|---|---|
| **SOXQ** (Invesco PHLX) | **0.19%** | 최저 비용, 동일 섹터 노출 |
| SOXX (iShares) | 0.35% | 개별 종목 비중 제한 → 더 분산. AMD/Micron 비중 높음 |
| SMH (VanEck) | 0.35% | NVIDIA 20% 집중 |

> **판정**: 하이닉스에 확신이 있으면 ETF는 **희석**이다. 미국 반도체 생태계 전체에 베팅하려면 SOXQ(최저비용).

---

## 2. 대형주 — 하이닉스 대비 판정

> 배수·시총·성장률은 `ai-밸류체인.md` 전체 비교표. 여기서는 **"vs 하이닉스" 한 줄만** 둔다.

| 종목 | fPER | 사이클 리스크 | vs SK하이닉스 |
|---|---|---|---|
| **SK하이닉스** | **8x** | 높음 | **기준** |
| **Micron** | 12x | 높음 | **가장 가까운 대안** — 같은 테제, 유사 밸류, 미국 상장. HBM 3위(~16%)가 유일한 열위 |
| 삼성전자 | 10x | 높음 | 저렴하나 HBM 열위 + 사업 희석 |
| **NVIDIA** | 24x | 중간 | 최강 해자, 3배 비쌈. **$4.5T에서 추가 상방 제한** + 추론 전환 시 ASIC에 잠식 |
| **TSMC** | 24x | 낮음 | 최강 해자, 3배 비쌈. **안정성을 원하면 TSMC, 상방을 원하면 하이닉스** |
| **Broadcom** | 33x | 중간 | Post-NVIDIA 핵심(ASIC 70%). 다만 **HBM은 어떤 칩이든 필요하므로 하이닉스가 더 안전** |
| **Vistra** | 14x | 낮음 | 반도체 사이클과 **무관** → 진짜 분산 효과. AI 직접 연관도는 낮음 |
| **Salesforce** | 19x | 낮음 | 에이전트 "사용처"에 직접 베팅하는 가장 싼 SW |
| Lam Research | 23x | 중간 | HBM 수혜 + 사이클 선행 |
| AMAT | 19x | 중간 | Lam 대비 분산 |
| Qualcomm | 11~14x | 중간 | **엣지 추론 보험**. 배당 2.3%. "에이전트가 엣지로 내려온다"는 전제 필요 |
| 클라우드 3사 | 26~29x | 낮음 | 에이전트 매출 직접 수혜. **CapEx $700B로 FCF 악화** |
| Vertiv | 32~38x | 중간 | 백로그 $9.5B로 가시성 높으나 비쌈 |
| 한미반도체 | 53x | 중간 | 성장주 프리미엄 |
| ARM | 60~70x | 낮음 | 너무 비쌈 |
| Datadog | 66x | 낮음 | 너무 비쌈 |
| Cloudflare | 적자 | 낮음 | 수익성 미증명 |
| Cerebras | N/A | 높음 | IPO 후 판단 |

---

## 3. 결론

### Tier 1 — 진지하게 고려

1. **Micron (MU)** — 하이닉스와 동일 테제, 미국 상장 접근성. **하이닉스를 못 사면 Micron**
2. **Salesforce (CRM)** — 인프라가 아닌 "사용처" 베팅. AI SW 중 최저 배수
3. **Vistra (VST)** — 반도체 사이클과 무관한 유일한 후보 = 진짜 분산

### Tier 2 — 보조

4. **NVIDIA** — PEG 0.44는 합리적이나 시총 상방 제한
5. **TSMC** — 안정성 선택지
6. **Broadcom** — NVIDIA 대체 테제에 베팅할 때
7. **Lam Research** — HBM 복잡도 증가의 선행 수혜
8. **Qualcomm** — 엣지 시나리오의 보험

### 최종 판단

> 추론의 병목은 메모리이고, 하이닉스는 그 병목의 과점 공급자다.
> **fPER 8x는 20개 후보 중 압도적 최저였다.**
>
> 그러나 **"하이닉스만이 답"은 아니다** — 셋 다 하이닉스가 못 가진 것을 하나씩 갖는다:
> - **Micron**: 같은 테제 + 미국 상장 (접근성)
> - **Salesforce**: 에이전트 사용처 (인프라가 아닌 수요처)
> - **Vistra**: 반도체 사이클 무관 (분산)
>
> | 성향 | 조합 |
> |---|---|
> | 공격적 | SK하이닉스 집중 |
> | 균형 | SK하이닉스 + Micron + Salesforce |
> | 보수 | TSMC + NVIDIA + SOXQ |

> **⚠ 이 결론의 전제가 바뀌었다.** 하이닉스 fPER 8x → 4.2x이고 주가는 52주 최고 대비 -53%다.
> "압도적 최저 배수"는 더 강해졌지만, **배수가 싸진 이유가 시클리컬 디스카운트 확대**라면 이야기가 다르다.
> 현재 판단은 `hynix.md` 상단 — 신규 매수 부적합 / 보유분 매도 없음.

---

## Sources

- [Cerebras IPO Q2 2026 (Seeking Alpha)](https://seekingalpha.com/news/4533742-ai-chipmaker-cerebras-targets-q2-2026-for-ipo-launch-report) · [$23B 밸류 (Bloomberg)](https://www.bloomberg.com/news/articles/2026-02-04/cerebras-raises-1-billion-in-funding-at-23-billion-valuation) · [IPO 준비 (SiliconANGLE)](https://siliconangle.com/2025/12/21/report-ai-chipmaker-cerebras-systems-rekindles-ipo-plans-targeting-early-2026-listing/)
- [Nvidia Groq 인수 $20B (CNBC)](https://www.cnbc.com/2025/12/24/nvidia-buying-ai-chip-startup-groq-for-about-20-billion-biggest-deal.html)
- [한미반도체 HBM 패키징 (Digitimes)](https://www.digitimes.com/news/a20251028PD237/hanmi-hbm-market-packaging-equipment.html) · [2026 매출 목표 (KED Global)](https://www.kedglobal.com/korean-chipmakers/newsView/ked202407050007)
- [한국 AI 반도체 공급망 (AInvest)](https://www.ainvest.com/news/strategic-imperative-investing-south-korea-ai-semiconductor-supply-chain-2507/) · [KOSPI 2026 전망 (Bloomberg)](https://www.bloomberg.com/news/articles/2026-01-06/korean-stocks-world-beating-rally-just-a-start-investors-say)
- [Lam Research 첨단 패키징](https://futurumgroup.com/insights/lam-research-q2-fy-2026-highlights-ai-driven-demand-and-packaging-gains/) · [LRCX vs AMAT](https://finance.yahoo.com/news/lrcx-vs-amat-chip-equipment-135400592.html)
- [Cloudflare 에이전트 인프라 (Fintool)](https://fintool.com/news/cloudflare-clawdbot-agentic-ai-surge)
- [반도체 ETF 비교 (US News)](https://money.usnews.com/investing/articles/best-semiconductor-etfs-to-buy) · [SMH vs SOXX (Motley Fool)](https://www.fool.com/investing/2026/01/06/smh-vs-soxx-better-buy-semiconductor-etf/)
- [SK Hynix 밸류에이션 (Simply Wall St)](https://simplywall.st/stocks/kr/semiconductors/kose-a000660/sk-hynix-shares/valuation)
