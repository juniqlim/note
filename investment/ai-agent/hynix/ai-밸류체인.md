# AI 밸류체인 — 세그먼트별 비교 (2026.02 스냅샷)

> **⚠ 데이터 기준일 2026-02-08.** 시총·주가·배수는 그 시점 값이다. 5개월 이상 지났고 그 사이 메모리 섹터가 크게 움직였다 —
> 하이닉스는 이 문서의 fPER 8배 → **현재 26F ~4.2배**(52주 최고 대비 -53%). 최신 판단은 `hynix.md` 상단을 본다.
> 이 문서의 용도는 **개별 수치가 아니라 세그먼트 간 상대 위치와 프레임**이다.

---

## 결론

| # | 결론 | 근거 |
|---|---|---|
| 1 | **fPER 기준 최대 비대칭 = SK하이닉스** | 밸류체인 전체 최저 배수(8x)이면서 추론의 대체불가 병목(메모리 대역폭) |
| 2 | **"삽 파는 회사" 3총사 = TSMC · NVIDIA · Broadcom** | AI 누가 이기든 통과. 24x / 24x / 33x로 성장 대비 합리적 |
| 3 | **클라우드 3사는 "AI 세금"을 내는 중** | CapEx 합산 ~$700B(+36% YoY)로 FCF 악화. 단기 압박 / 장기 독점 강화 |
| 4 | **소프트웨어 레이어가 전 세그먼트 중 가장 비싸다** | fPER 19~200x. 성장이 뛰어나도 이미 가격에 반영 |
| 5 | **저평가는 배수가 아니라 "왜 싼가"로 판별된다** | 하이닉스 8x·마이크론 12x는 **시클리컬 디스카운트** — 배수가 싼 게 아니라 이익 지속성을 시장이 의심하는 것 → `시스템반도체-비시클리컬-분석.md`, `hynix.md` §4 |

---

## 전체 비교표

| 세그먼트 | 종목 | 시가총액 | Forward PER | 성장률 | 해자 | 추론 수혜 |
|---|---|---|---|---|---|---|
| **Memory/HBM** | SK Hynix | ₩579조 (~$400B) | **~8x** | +51% (DRAM) | ★★★★★ | ★★★★★ |
| Memory/HBM | Micron (MU) | $444B | ~12x | +114% (2개월) | ★★★★☆ | ★★★★★ |
| Memory/HBM | Samsung Electronics | ~$350B+ | ~10x | 이익추정 +115% 상향 | ★★★☆☆ | ★★★★★ |
| **Foundry** | TSMC (TSM) | $1.81T | ~24x | +30% | ★★★★★ | ★★★★★ |
| **GPU** | NVIDIA (NVDA) | $4.51T | ~24x | +55~60% | ★★★★★ | ★★★★★ |
| GPU | AMD | $411B | ~28~34x | +64% EPS | ★★★☆☆ | ★★★☆☆ |
| **Custom ASIC** | Broadcom (AVGO) | $1.58T | ~33x | +52% | ★★★★☆ | ★★★★★ |
| Custom ASIC | Marvell (MRVL) | ~$100B | ~24x | ~+30% | ★★★☆☆ | ★★★★★ |
| **Networking** | Arista (ANET) | $173B | ~39x | +20% | ★★★★☆ | ★★★★☆ |
| **Power/Energy** | Vertiv (VRT) | $68B | ~32~38x | +29% | ★★★☆☆ | ★★★★☆ |
| Power/Energy | Eaton (ETN) | $142B | ~25~27x | +10% | ★★★★☆ | ★★★☆☆ |
| Power/Energy | Schneider Electric | ~$130B+ | **~24x** | 안정 성장 | ★★★★☆ | ★★★★☆ |
| Power/Energy | Constellation (CEG) | $98B | ~27x | ~15% | ★★★★☆ | ★★★★☆ |
| Power/Energy | Vistra (VST) | $52B | **~14x** | ~20% | ★★★☆☆ | ★★★★☆ |
| **Cloud** | Amazon (AMZN) | $2.26T | ~27x | +17% | ★★★★★ | ★★★★★ |
| Cloud | Microsoft (MSFT) | $2.98T | ~26x | +17% | ★★★★★ | ★★★★★ |
| Cloud | Alphabet (GOOGL) | $3.9~4.0T | ~29x | +15% | ★★★★★ | ★★★★★ |
| **AI SW** | Palantir (PLTR) | ~$330B | **~103~137x** | +61% | ★★★☆☆ | ★★★★☆ |
| AI SW | ServiceNow (NOW) | $105~124B | ~28~45x | +20%+ | ★★★★☆ | ★★★★☆ |
| AI SW | Salesforce (CRM) | $179B | ~19x | +15% | ★★★★☆ | ★★★★☆ |
| AI SW | Snowflake / MongoDB / Datadog | $70B / $30B / $60B | 165x / 76x / 66x | — | ★★★☆☆ | ★★★☆☆ |
| **Edge AI** | Qualcomm (QCOM) | ~$157B | **~11~14x** | Edge AI 초기 | ★★★☆☆ | ★★★★★ |
| Edge AI | ARM Holdings | ~$170B+ | ~60~70x | +30% AI 비중 | ★★★★☆ | ★★★★☆ |
| **DC REIT** | Equinix (EQIX) | ~$100B | 25~28x AFFO | +10% | ★★★★★ | ★★★★☆ |
| DC REIT | Digital Realty (DLR) | $57B | 18~21x AFFO | +10% | ★★★★☆ | ★★★★☆ |

> **fPER 정렬**: SK Hynix(8) < Samsung(10) < Micron(12) < Qualcomm(11~14) < Vistra(14) < Salesforce(19) < NVIDIA(24) = TSMC(24) = Marvell(24) = Schneider(24) < Eaton(26) < MSFT(26) < CEG(27) < AMZN(27) < AMD(28~34) < GOOGL(29) < Vertiv(32~38) < Broadcom(33) < Arista(39) < ARM(60~70) < Datadog(66) < MongoDB(76) < Palantir(103~137) < Snowflake(165)

### 수치 충돌 기록

두 소스가 같은 날짜에 다른 값을 보고했다. 배수는 **선행/후행 기준 차이**, 마이크론 시총은 **한쪽이 스테일**로 판단해 아래 채택값을 썼다.

| 항목 | 소스 A | 소스 B | 채택 | 판단 |
|---|---|---|---|---|
| SK Hynix PER | ~16x | ~8x | **8x (선행)** | A는 TTM(후행 18x)에 가까운 값을 Forward로 표기 |
| Micron 시총 | ~$120B | $444B | **$444B** | 주가 $394.69 × 발행주식 기준. A가 스테일 |
| NVIDIA fPER | 25~31x (FY27) | ~24x | **24x** | 회계연도 기준 차이 |
| Palantir fPER | 137~200x | 103~137x | **103~137x** | 겹치는 구간 채택 |
| Arista PER | ~45x (TTM) | ~39x | **39x (선행)** | 기준 차이 |

---

## 1. Memory / HBM

**시장 규모**: 2025년 $35B → 2026년 $54.6B (BofA, +58% YoY) → 2028년 ~$100B TAM (CAGR ~40%)

### SK Hynix (000660.KS)
- fPER **~8x** — 밸류체인 전체 최저. HBM 점유율 **57~62%**(HBM4 기준 70% 전망), 2026년 물량 완판(sold out), NVIDIA 1순위 공급사
- **Bull**: DRAM 슈퍼사이클, HBM 대체불가. Goldman: "2026년까지 HBM3/3E 지배적 1위 유지"
- **Bear**: 메모리 사이클 하락 시 실적 급감, 삼성 추격
- → 상세 판단은 `hynix.md`

### Micron (MU)
- fPER ~12x. 2개월간 +114% 급등, 2026년 HBM 전량 매진
- **차별화**: 미국 유일 메모리 제조사 = 지정학 프리미엄 + CHIPS Act 보조금
- **하이닉스 대비**: 12x vs 8x. 하이닉스가 HBM 1위이면서 더 싸다. 마이크론의 이점은 미국 상장 접근성과 지정학

### Samsung Electronics
- fPER ~10x. HBM 점유율 ~25%, HBM3E 수율 문제로 하락 중
- 단 **이익 추정치 상향 폭이 3사 중 가장 큼(+115%)** — 기대가 가장 낮았기 때문

**추론 수혜 ★★★★★** — 추론 서버 1대당 HBM 탑재량이 학습 서버 대비 동등 이상. 추론 스케일링이 HBM 수요의 핵심 드라이버.

---

## 2. Foundry — TSMC

- fPER ~24x. 2026년 USD 매출 **+30%** 가이던스, CapEx $52~56B(2nm 양산), AI 매출 CAGR 60%(2029년까지), HPC가 매출 58%
- **해자 ★★★★★ 최강** — 2nm 이하에서 경쟁자 부재. 삼성/인텔 5년 이상 뒤처짐. NVIDIA·Apple·Broadcom·AMD 전부 의존
- **Bear**: 대만 지정학, 미국 팹 건설비용
- **핵심**: "AI 칩 누가 이기든 TSMC는 이긴다." 대형 테크 중 Meta 다음으로 낮은 배수

**추론 수혜 ★★★★★** — 추론용 칩(Blackwell, 커스텀 ASIC)도 전부 TSMC 생산.

---

## 3. GPU / Accelerators

**구조 변화**: 커스텀 ASIC 시장이 **CAGR 27%로 GPU보다 빠르게 성장** → Broadcom/Marvell 수혜.

### NVIDIA (NVDA)
- $4.51T, fPER ~24x, FY2026 매출 $213.3B, GPU 점유율 90%+
- **해자**: CUDA 생태계 lock-in. 매출/이익 규모 자체가 해자
- **Bear**: 고객사 자체 칩(TPU, Trainium), 성장 둔화 시 멀티플 압축
- fPER 24x는 55~60% 성장 대비 합리적

### Broadcom (AVGO)
- fPER ~33x. FY2026 AI 반도체 매출 **$40.4B**(+103% YoY), 전체 매출의 50% 도달 전망. AI 주문잔고 **$73B**
- **커스텀 ASIC 60~80% 장악** — Google TPU, Meta MTIA, OpenAI, Anthropic
- **해자**: SerDes + HBM 컨트롤러 + 광인터커넥트 + 네트워킹 실리콘 풀스택. Tomahawk 6(102.4Tbps)
- **핵심**: "Post-NVIDIA" 시대의 설계 파트너. 하이퍼스케일러가 자체 칩 갈수록 수혜

### Marvell (MRVL)
- fPER ~24x. AWS Trainium 등 커스텀 실리콘 20~25% 점유
- **Broadcom과 같은 스택인데 배수는 24x vs 33x** — 상대 저평가

### AMD
- fPER ~28~34x — **NVIDIA보다 비싸면서 해자는 약하다**
- 데이터센터 매출 CAGR 60%+ 목표, MI400으로 추론 공략. 다만 CUDA 장벽 + 추론 전용 ASIC과 양면 경쟁

**추론 수혜 ★★★★★** — 2026년 추론이 전체 AI 컴퓨트의 2/3 차지 전망. 커스텀 ASIC이 추론 효율에 특화되어 더 빠르게 성장.

---

## 4. Networking — Arista (ANET)

- fPER ~39x, 2026년 매출 $10B+ 목표(+20%), AI DC 매출 $2.75B
- 800GbE Ethernet이 AI 클러스터 표준으로 부상, InfiniBand 대비 채택 가속
- **해자**: EOS 소프트웨어 전환비용. Meta/Microsoft 주요 고객
- **Broadcom과의 관계**: Broadcom Jericho3가 Arista R4 시리즈의 핵심 실리콘 — 상호보완이지만 **Broadcom 해자가 더 넓다**
- **주의**: 20% 성장에 fPER 39x는 밸류체인 내 네트워킹 중 가장 비쌈

---

## 5. Power / Energy

**수요 구조**: DC 전력 시장 2025 $35B → 2030 $50.5B(CAGR 7.5%). AI 랙당 전력 2023년 10~15kW → 2026년 **120~150kW(10배)**

| 종목 | fPER | 포인트 |
|---|---|---|
| **Vistra (VST)** | **~14x** | 에너지 섹터 최저. 텍사스 원자력+가스, 목표가 +54%, Strong Buy. 화석연료 ESG 리스크 |
| **Schneider Electric** | ~24x | 전력 인프라 중 가장 합리적 배수 |
| **Eaton (ETN)** | ~25~27x | 전기 포트폴리오가 매출 70%, "전례 없는 수요"(CEO). 성장 10%로 가장 낮음 |
| **Constellation (CEG)** | ~27x | 미국 최대 원자력. DC 장기 PPA + 탄소 제로. 규제 리스크 |
| **Vertiv (VRT)** | ~32~38x | 액체 냉각 지배, 매출 +29% / FCF +133%. 경쟁 심화(Schneider, ABB) + 고평가 |

**공통 한계**: 전력 인프라는 AI 수요와 직결되지만 **반도체 대비 해자가 약하다**. 발전 자산(CEG, VST)만 물리적 진입장벽 보유.

**추론 수혜 ★★★★☆** — 추론 서버는 24/7 상시 가동. 전력/냉각 수요가 학습보다 오히려 지속적.

---

## 6. Cloud Platforms

### 2026년 AI CapEx

| | 금액 |
|---|---|
| Amazon | **$200B** (발표 시 주가 -6%) |
| Alphabet | $175~185B |
| Microsoft | ~$150B |
| **4사 합계** | **~$700B** (2025 대비 +36%) |

> **핵심 리스크**: Amazon 2026년 FCF **-$17~28B** 전망(Morgan Stanley/BofA). Microsoft FCF -28% 전망.
> 이들은 밸류체인의 최대 수혜자이자 **최대 구매자**다. 지금은 구매자 쪽 부담이 드러나는 국면.

| 종목 | fPER | Bull | Bear |
|---|---|---|---|
| Amazon | ~27x | AWS 1위, Bedrock/Trainium 풀스택, 리테일 캐시카우 | $200B CapEx로 FCF 적자 전환 |
| Microsoft | ~26x | OpenAI 파트너, Azure+Copilot, 기업 시장 지배 | YTD -17%, FCF -28%, 회수 지연 |
| Alphabet | ~29x | 검색 캐시카우 + Gemini + TPU + GCP 풀스택 | 검색 광고 AI 카니발라이제이션 |

자체 칩 개발 가속(TPU, Trainium, Maia) = NVIDIA 의존도 축소 시도 → Broadcom/Marvell 수혜의 반대편.

---

## 7. AI Software

**전 세그먼트 중 가장 비싸다** (fPER 19~200x).

| 종목 | fPER | 성장 | 판단 |
|---|---|---|---|
| **Salesforce (CRM)** | **~19x** | +15% | AI SW 중 최저 배수. Agentforce ARR +330% → $540M, 9,500 유료 딜. CRM 데이터 lock-in |
| ServiceNow (NOW) | ~28~45x | +20%+ | Now Assist ACV $600M → 2026 $1B 목표. AI Control Tower로 에이전트 오케스트레이션. **1년간 -50%** |
| Datadog / MongoDB / Snowflake | 66x / 76x / 165x | — | BofA: "SaaSpocalypse" 이후 반등 전망 |
| **Palantir (PLTR)** | **~103~137x** | +61% | 정부/국방 lock-in + AIP. **배수가 "완벽한 실행"을 전제** — 리스크/리워드 비대칭 |

**추론 수혜 ★★★★☆** — AI 에이전트 시대의 직접 수혜자이나, 이미 가격에 반영.

---

## 8. Edge AI / On-Device

| 종목 | fPER | 포인트 |
|---|---|---|
| **Qualcomm (QCOM)** | **~11~14x** | 전 세그먼트 통틀어 최저 배수. On-device inference 핵심 플레이어. RISC-V 스타트업 Ventana 인수로 ARM 의존 축소 시도 |
| ARM Holdings | ~60~70x | 아키텍처 독점(toll booth). Armv9 SVE2로 추론 최적화. 배수가 부담 |

Edge AI는 "Cloud → Edge" 전환의 **초기 단계**. 동인은 클라우드 비용 절감 + 지연시간.

**추론 수혜 ★★★★★** — On-device inference가 Edge AI의 본질.

---

## 9. Data Center REITs

| 종목 | P/AFFO | 포인트 |
|---|---|---|
| Equinix (EQIX) | 25~28x | 260개 DC / 71개 시장. **interconnection 네트워크 효과 = 복제 불가**. 2029년까지 용량 2배(과거 27년 구축분을 5년 내 추가). AFFO 변곡점 2026 |
| Digital Realty (DLR) | 18~21x | 미국 임대 DC 전력 점유율 15% 1위. 대규모 캠퍼스형. interconnection 해자는 약함 |

하이퍼스케일러 CapEx $700B의 물리적 수혜처. 현재 18~28x AFFO는 역사적 평균 범위.
**Bear 공통**: 금리 민감 + 하이퍼스케일러 자체 DC 건설 증가.

---

## 10. AI Model Companies (비상장)

| 기업 | 밸류에이션 (2026.02) | 간접 투자 경로 |
|---|---|---|
| OpenAI | ~$730B | Microsoft |
| Anthropic | ~$380B (Series G) | Google, Amazon |

모델 레이어는 **commoditization 리스크**가 있다(오픈소스, DeepSeek). 해자는 모델 자체가 아니라 데이터 플라이휠 + 엔터프라이즈 lock-in에서 형성된다.

---

## 종합

### 해자 순위 (대체불가능성)

1. **TSMC** — 첨단 공정 독점, 대안 없음
2. **NVIDIA** — CUDA 생태계 + 소프트웨어 스택
3. **SK Hynix** — HBM 1위, 2026년 완판
4. **ARM** — CPU 아키텍처 toll booth
5. **Broadcom** — 커스텀 ASIC + 네트워킹 이중 해자
6. **Arista** — AI DC Ethernet 1위
7. **Equinix** — 글로벌 인터커넥션 네트워크 효과

### 가성비 순위 (fPER 대비 성장)

| 순위 | 종목 | fPER | 성장 | PEG | 평가 |
|---|---|---|---|---|---|
| 1 | **SK Hynix** | ~8x | +51% | 0.16 | 극히 저평가 (단 시클리컬 디스카운트) |
| 2 | **Micron** | ~12x | +40%+ | 0.30 | 저평가 (동일 단서) |
| 3 | **Vistra** | ~14x | +20% | 0.70 | 저평가 |
| 4 | **Salesforce** | ~19x | +15% | 1.27 | 적정~약간 저평가 |
| 5 | **NVIDIA** | ~24x | +55% | 0.44 | 성장 대비 적정 |
| 6 | **TSMC** | ~24x | +30% | 0.80 | 적정 |
| 7 | **Broadcom** | ~33x | +52% | 0.63 | 성장 대비 적정 |
| 8 | **MSFT / AMZN** | ~26~27x | +17% | ~1.5 | 적정 (CapEx 리스크) |
| 9 | **Eaton** | ~26x | +10% | 2.50 | 고평가 |

> **PEG의 함정**: 하이닉스 0.16은 "싸다"가 아니라 **"시장이 +51% 성장의 지속을 믿지 않는다"**로 읽어야 한다.
> 시클리컬은 이익 고점에서 배수가 가장 낮게 보인다. → `hynix.md` §4, `시스템반도체-비시클리컬-분석.md`

### 카테고리별 Best Pick

| 카테고리 | Pick | 이유 |
|---|---|---|
| Memory/HBM | **SK Hynix** | fPER 8x, HBM 1위 |
| Foundry | **TSMC** | 누가 이기든 이김 |
| GPU | **NVIDIA** | fPER 24x에 절대 해자 |
| Custom ASIC | **Broadcom** > Marvell | AI 매출 +103%, 70% 점유. 단 Marvell이 배수는 쌈 |
| Networking | **Arista** (유일 pure play) | 다만 39x로 비쌈 |
| Power | **Vistra** | fPER 14x + 원자력 |
| Cloud | **Amazon** | AWS 1위 (FCF 적자 리스크) |
| AI SW | **Salesforce** | fPER 19x, Palantir의 1/5 |
| Edge AI | **Qualcomm** | 전체 최저 배수 |
| DC REIT | **Equinix** | interconnection 해자 |

### 추론(Inference) 스케일링 최대 수혜

1. **커스텀 ASIC** (Broadcom, Marvell) — 추론 효율 특화 설계
2. **HBM** (SK Hynix, Micron) — 추론 서버에도 HBM 필수
3. **Edge AI** (Qualcomm, ARM) — On-device가 차세대 성장축
4. **전력/냉각** (Vistra, Schneider, Vertiv) — 추론은 24/7, 학습보다 지속적
5. **Cloud** (AWS, Google, Azure) — 추론 API가 클라우드 성장 핵심

### Under-the-Radar

| 종목 | 이유 |
|---|---|
| **Micron (MU)** | 메모리 3사 중 최저 배수 + 미국 생산 지정학 프리미엄 |
| **Qualcomm (QCOM)** | fPER 11~14x. Edge AI 수혜가 미반영 |
| **Marvell (MRVL)** | Broadcom과 같은 스택, 24x vs 33x |
| **Dell Technologies** | AI 서버 직접 수혜, fPER ~15x |
| **Applied Digital (APLD)** | CoreWeave와 $11B DC 계약. 장기 영업이익 6x |
| **Quanta Services (PWR)** | DC 전력 인프라 건설 핵심 계약자. AEP $72B 프로그램 수주 |
| **MKS Instruments** | 반도체 장비 핵심 부품. 첨단 노드 확대 간접 수혜 |

---

## Sources

*2026.02.08 웹 리서치 기준. Forward PER은 데이터 소스에 따라 차이가 있다 — 「수치 충돌 기록」 참조.*

**Memory/HBM**
- [SK Hynix HBM Market Share - Astute Group](https://www.astutegroup.com/news/general/sk-hynix-holds-62-of-hbm-micron-overtakes-samsung-2026-battle-pivots-to-hbm4/)
- [SK Hynix HBM 2026 Market Outlook](https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/)
- [SK Hynix Market Cap - CompaniesMarketCap](https://companiesmarketcap.com/sk-hynix/marketcap/)
- [SK Hynix Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/HAM:HY9H)
- [Micron Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/MU) · [Statistics - StockAnalysis](https://stockanalysis.com/stocks/mu/statistics/)
- [2026 AI & Semiconductor Outlook - Fabricated Knowledge](https://www.fabricatedknowledge.com/p/2026-ai-and-semiconductor-outlook)

**Foundry / GPU / ASIC**
- [TSMC Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/TSM) · [Statistics](https://stockanalysis.com/stocks/tsm/statistics/) · [Why 2026 Will Be Even Bigger - Seeking Alpha](https://seekingalpha.com/article/4855898-tsmc-why-2026-will-be-even-bigger)
- [NVIDIA Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/NVDA) · [Market Cap](https://companiesmarketcap.com/nvidia/marketcap/) · [Poised for $6T - Seeking Alpha](https://seekingalpha.com/article/4855757-nvidia-poised-to-unlock-6-trillion-in-2026)
- [NVIDIA vs AMD vs Broadcom - Motley Fool](https://www.fool.com/investing/2026/01/31/nvidia-vs-amd-vs-broadcom-the-best-ai-chip-stock-t/)
- [AMD AI Upside 2026 - Seeking Alpha](https://seekingalpha.com/article/4858648-amd-serious-ai-driven-upside-in-2026) · [MI350 Challenge](https://seekingalpha.com/article/4856532-amds-mi350-ai-accelerator-that-could-challenge-nvidias-dominance-in-2026)
- [Broadcom AI Revenue - FinancialContent](https://markets.financialcontent.com/stocks/article/tokenring-2026-2-6-the-new-silicon-hegemony-broadcoms-ai-revenue-set-to-eclipse-legacy-business-by-end-of-fy-2026) · [Custom AI Silicon Boom](https://markets.financialcontent.com/wral/article/tokenring-2026-2-2-broadcoms-custom-ai-silicon-boom-beyond-the-google-tpu)
- [Marvell vs Broadcom Valuation Disparity - Trefis](https://www.trefis.com/stock/mrvl/articles/584726/marvell-vs-broadcom-same-ai-stack-20x-valuation-disparity/2025-12-09)
- [AI Accelerator Market $600B by 2033 - Bloomberg](https://www.bloomberg.com/company/press/ai-accelerator-market-looks-set-to-exceed-600-billion-by-2033-driven-by-hyperscale-spending-and-asic-adoption-according-to-bloomberg-intelligence/)

**Networking / Power**
- [Arista Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/ANET) · [Statistics](https://stockanalysis.com/stocks/anet/statistics/) · [AI Networking Growth Engine](https://seekingalpha.com/article/4862890-arista-networks-the-ai-networking-growth-engine)
- [Vertiv Statistics - StockAnalysis](https://stockanalysis.com/stocks/vrt/statistics/) · [Deep Dive - PredictStreet](https://markets.financialcontent.com/wral/article/predictstreet-2026-1-2-the-cooling-heart-of-the-ai-era-a-deep-dive-into-vertiv-holdings-vrt)
- [Eaton Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/ETN)
- [Constellation Statistics - StockAnalysis](https://stockanalysis.com/stocks/ceg/statistics/) · [Vistra Statistics](https://stockanalysis.com/stocks/vst/statistics/)

**Cloud / AI SW**
- [Big Tech $700B AI CapEx - CNBC](https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html)
- [Amazon $200B CapEx - IndexBox](https://www.indexbox.io/blog/amazon-announces-200-billion-capex-forecast-for-2026-amid-ai-infrastructure-race/)
- [Amazon Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/AMZN) · [Microsoft Market Cap - Capital.com](https://capital.com/en-int/markets/shares/microsoft-corp-share-price/market-cap) · [Alphabet Statistics](https://stockanalysis.com/stocks/googl/statistics/)
- [Palantir Forward PE - GuruFocus](https://www.gurufocus.com/term/forward-pe-ratio/PLTR) · [2026 Forecast - IO Fund](https://io-fund.com/ai-stocks/palantir-stock-2026-forecast-valuation)
- [ServiceNow AI Growth - Motley Fool](https://www.fool.com/investing/2026/02/03/servicenow-slip-strong-ai-growth-buy-dip-stock/) · [Agentic AI - AInvest](https://www.ainvest.com/news/servicenow-agentic-ai-revolution-strategic-buy-2026-2512/)
- [Salesforce Agentforce - Motley Fool](https://www.fool.com/investing/2025/12/08/is-it-time-to-buy-salesforce-stock-with-ai-agent/) · [Statistics](https://stockanalysis.com/stocks/crm/)

**Edge AI / REIT**
- [Qualcomm Edge AI Pivot - FinancialContent](https://markets.financialcontent.com/stocks/article/finterra-2026-2-5-the-edge-ai-pivot-a-deep-dive-into-qualcomm-qcom-in-2026)
- [ARM Holdings in AI Era - FinancialContent](https://markets.financialcontent.com/stocks/article/finterra-2026-2-5-the-invisible-titan-a-deep-dive-into-arm-holdings-arm-in-the-ai-era)
- [Equinix Statistics - StockAnalysis](https://stockanalysis.com/stocks/eqix/) · [Digital Realty Statistics](https://stockanalysis.com/stocks/dlr/statistics/)
- [Data Center REITs AI Demand - S&P Global](https://www.spglobal.com/market-intelligence/en/news-insights/articles/2025/6/digital-realty-equinix-ramp-up-datacenters-as-ai-drives-demand-90542889)
- [Hyperscaler Capex $500B - Motley Fool](https://www.fool.com/investing/2026/02/07/this-datacenter-reit-could-double-as-hyperscalers/)

**Under-the-Radar**
- [Undervalued AI Enablers - ainvest](https://www.ainvest.com/news/undervalued-ai-enablers-outperform-2026-radar-infrastructure-stocks-strong-analyst-backing-scalable-cases-2601/)
