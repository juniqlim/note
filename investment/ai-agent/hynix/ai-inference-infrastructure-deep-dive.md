# AI 추론 인프라 투자 — HBM/GPU 너머의 기회

2026년 2월 8일 작성

## 핵심 테제

GPU와 메모리(HBM) 다음 단계의 AI 인프라 병목(Bottleneck)이 현실화되고 있다.
에이전트 기반 추론(Inference) 수요 폭증이 만드는 **네트워킹, 냉각, 전력, 스토리지, 커스텀 ASIC** 레이어의 투자 기회를 정리한다.

---

## 1. 추론 시대의 진짜 병목: GPU가 아니라 "연결"과 "전력"

### 2026년 핵심 병목 3가지

| 병목 | 상세 | 수혜 |
|------|------|------|
| **KV 캐시 용량** | 에이전트가 수백만 토큰 컨텍스트 유지 → GPU 메모리 초과 → NVMe SSD로 오프로드 필요 | 엔터프라이즈 SSD |
| **인터커넥트 대역폭** | 구리(Copper) 한계 도달 → 실리콘 포토닉스/광 연결로 전환 중 | 광 트랜시버, CPO |
| **전력 공급** | AI 데이터센터 전력 수요 2030년까지 165% 증가 (Goldman Sachs) | 전력 반도체, 냉각 |

NVIDIA CES 2026에서 발표한 **ICMSP (Inference Context Memory Storage Platform)** 가 이를 증명:
KV 캐시를 NVMe SSD로 오프로드하는 것을 표준화했다. 즉 **추론 시대에 SSD는 선택이 아니라 필수 인프라**가 된다.

---

## 2. 레이어별 기회 분석

### A. 광 네트워킹 / 인터커넥트 — "구리 시대의 종말"

**테제**: AI 스케일링의 병목이 컴퓨트에서 연결(Connectivity)로 이동. 2026년은 "구리 시대 → 광 시대" 전환의 원년.

| 회사 | 티커 | 역할 | 밸류에이션 | 평가 |
|------|------|------|-----------|------|
| **Broadcom** | AVGO | AI 스위칭 실리콘 80%+ 점유, 커스텀 ASIC 설계 | 높음 (이미 반영) | 해자 최강이나 비쌈 |
| **Marvell** | MRVL | 1.6T 광 인터커넥트, PCIe 6 리타이머, 커스텀 ASIC | 중간 | Celestial AI 인수($5.5B)로 포토닉스 역량 확보 |
| **Fabrinet** | FN | 광 트랜시버 계약 제조 (NVIDIA, Cisco향) | P/E ~47-51x | 실행력 좋으나 밸류에이션 부담 |
| **Coherent Corp** | COHR | AI 데이터컴 사업 YoY +23%, 광 부품 | 중간 | 포트폴리오 다각화, 순수 AI 비중 아직 작음 |
| **Arista Networks** | ANET | AI 네트워킹 패브릭, EtherLink | 높음 | 2026 매출 $10B 타겟, 이미 시장 인정 |

**실리콘 포토닉스 전환 타임라인**:
- 2026 H1: NVIDIA Quantum-X InfiniBand 스위치 (115 Tb/s, 포토닉스 기반)
- 2026 H2: NVIDIA Spectrum-X Photonics 이더넷 스위치
- CPO(Co-Packaged Optics) 시장: 2026~2036 CAGR 37%, $20B+

> **주목**: Marvell(MRVL)이 가장 흥미롭다. Celestial AI 인수로 실리콘 포토닉스 핵심 역량을 확보했고, Amazon/Google/Microsoft/Meta 4대 하이퍼스케일러 모두와 커스텀 ASIC 관계를 맺고 있다. 데이터센터 매출 FY2026 +40% 성장 전망.

---

### B. 냉각 / 열 관리 — "녹이지 않는 인프라"

**테제**: NVIDIA H100 칩 하나가 700W 열을 발생. 수만 개 GPU 집적 시 액체냉각(Liquid Cooling)은 필수.

| 회사 | 티커 | Forward P/E | 데이터센터 매출 성장 | 특징 |
|------|------|------------|-------------------|------|
| **Vertiv Holdings** | VRT | ~30x | +20% YoY | 전력+냉각 풀 에코시스템, NVIDIA 레퍼런스 아키텍처 파트너, 백로그 $9.5B |
| **Modine Manufacturing** | MOD | ~20x | **+60% YoY 가이던스** | Vertiv 절반 밸류에이션에 유사 성장, 순수 냉각 노출도 높음 |

액체냉각 시장: 2025 $5.1B → 2030 $16.16B (CAGR 26%)

> **주목**: **Modine(MOD)**가 가장 매력적. Forward P/E ~20x로 Vertiv의 절반 수준이면서, 데이터센터 냉각 매출 성장률은 +60%로 더 빠르다. Airedale 인수 기반 Climate Solutions 부문이 핵심. 중형주(시총 $6.9B)라 기관 관심도 상대적으로 낮다.

---

### C. 전력 관리 반도체 — "전력 효율의 게이트키퍼"

**테제**: 데이터센터 전력 수요 폭증 → 전력 변환 효율이 핵심 → 파워 반도체 수혜.

| 회사 | 티커 | 역할 | 상태 |
|------|------|------|------|
| **Monolithic Power Systems** | MPWR | AI 서버용 전력 관리 IC, NVIDIA 시스템 통합 | 엔터프라이즈 데이터 부문 2026 +50% 성장 전망. 주가 이미 반영 중 (52주 신고가) |
| **Navitas Semiconductor** | NVTS | GaN/SiC 기반 차세대 전력 반도체, 800V DC 아키텍처 | 아직 소규모, 2026은 전환기. 800V 데이터센터 아키텍처 채택 시 폭발적 성장 가능 |

> **주목**: **Navitas(NVTS)**는 고위험-고수익 옵션. NVIDIA가 800V 아키텍처 전환을 예고했고, GaN/SiC가 기존 실리콘 대비 에너지 효율 2-3% 향상. 단, 아직 매출이 작고 흑자전환 전이라 위험도 높다. MPWR은 실적이 검증되었으나 밸류에이션이 높아진 상태.

---

### D. 엔터프라이즈 SSD / 스토리지 — "추론의 숨은 필수재"

**테제**: KV 캐시 오프로드 + AI 데이터 저장 → 엔터프라이즈 SSD 수요 구조적 증가. NAND 공급은 HBM 전환으로 축소.

| 회사 | 티커 | Forward P/E | 특징 |
|------|------|------------|------|
| **SanDisk** | SNDK | **~18x** | WD에서 2025 스핀오프. 매출 55%가 엔터프라이즈 SSD. 128TB DC SN670이 AI 추론 표준. S&P 500 2025 최고 수익률(+550%). Kioxia JV 2034년까지 연장. |
| **Kioxia** | 6600.T | — | 2024 도쿄 IPO. 332층 BiCS10 생산 2026 가속. SanDisk과 합작 |

NAND 가격 2026년 상승 예상:
- SanDisk이 3D NAND 엔터프라이즈 SSD 가격을 Q1 2026에 2배 인상
- 삼성/SK하이닉스가 HBM 우선 생산 → NAND 공급 축소 → 구조적 가격 상승

> **주목**: **SanDisk(SNDK)** Forward P/E ~18x는 AI 스토리지 순수 플레이(Pure-Play) 치고 매우 저렴하다. Simply Wall St 추정 페어밸류 대비 32% 할인 거래 중. NVIDIA ICMSP 표준과 직접 수혜. 다만 2025년 +550% 급등 후이므로 엔트리 타이밍 주의.

---

### E. 커스텀 ASIC / 추론 전용 칩 — "GPU 독점 해체"

**테제**: 하이퍼스케일러들이 NVIDIA 의존도 줄이기 위해 자체 ASIC 개발 가속. 설계 파트너(Broadcom, Marvell)가 수혜.

| 하이퍼스케일러 | 칩 | 설계 파트너 | 세대 |
|--------------|-----|-----------|------|
| Google | TPU (Ironwood) | **Broadcom** | 7nm → 5nm → 3nm |
| Amazon | Trainium 3 | **Marvell** | TSMC 3nm, HBM3E 144GB |
| Meta | MTIA | **Broadcom** | 자체 학습/추론 가속기 |
| Microsoft | Maia 200 | **Marvell** | 차세대 추론 ASIC |
| OpenAI | 신규 ASIC | **Broadcom** | 2026년 시작 |

> 커스텀 ASIC 시장이 GPU 시장보다 빠르게 성장할 전망 (Futurum Group). Broadcom은 이미 반영되었고, **Marvell(MRVL)**이 4대 하이퍼스케일러 중 3곳(AWS, Google Axion, Microsoft Maia, Meta DPU)과 관계를 맺어 분산된 수혜 구조.

---

### F. 반도체 테스트 — "누가 칩을 만들든 검사는 필요"

| 회사 | 티커 | 역할 | 밸류에이션 |
|------|------|------|-----------|
| **Advantest** | ATEYY (6857.T) | 글로벌 1위 ATE(자동화 테스트 장비) | P/E ~44x |

- AI 칩이 복잡해질수록 테스트 수요 증가 (HBM, 3nm ASIC 등)
- 2026 생산능력 3,000 → 5,000 유닛 확대
- FY2027 매출 1.07조엔 ($7.28B), 순이익 3,285억엔 ($2.23B)
- "칩 브랜드 무관" = NVIDIA든 Google TPU든 Trainium이든 수혜

> P/E 44x로 싸진 않지만, "ASML of Testing"이라는 독과점 지위 고려 시 ASML(~35x)과 유사한 프리미엄. AI 칩 다양화(커스텀 ASIC 증가)가 오히려 테스트 수요를 더 키운다.

---

### G. 엣지 AI 추론 — "클라우드 이후"

| 회사 | 티커 | 역할 | 상태 |
|------|------|------|------|
| **Qualcomm** | QCOM | Snapdragon X NPU (80 TOPS), 온디바이스 AI | 모바일/PC 교체 사이클 수혜. 밸류에이션 합리적 |
| **Lattice Semiconductor** | LSCC | 저전력 FPGA, 엣지 AI, 보드 관리 | 매출 68% GM, 산업용 사이클 바닥 통과 중. 2026 회복 시 업사이드 |
| **Renesas** | RNECF (6723.T) | 엣지 MCU/MPU, Ethos-U55 NPU 탑재 | 산업용 IoT/로보틱스 AI 추론 |

엣지 AI 칩 시장: 2026 $4.44B → 2031 $11.54B (CAGR 21%)

> **주목**: **Lattice(LSCC)**는 서브 1W 전력의 FPGA로 엣지 AI에서 독점적 지위를 가지고 있으나, 산업/자동차 부문 부진으로 주가 하락. 2026년 사이클 회복 시 연간 $60-80M 매출 역풍이 순풍으로 전환. 68% GM은 AI 반도체 중에서도 최상위.

---

## 3. 일본/한국/대만 — 간과된 공급망

| 회사 | 국가 | 티커 | 역할 | 밸류에이션 |
|------|------|------|------|-----------|
| **TSMC** | 대만 | TSM | 모든 AI 칩 제조 (NVIDIA, Broadcom, Marvell, Google, Amazon 등) | Forward P/E ~24x, 2026 매출 +30% |
| **Advantest** | 일본 | 6857.T | AI 칩 테스트 장비 글로벌 1위 | P/E ~44x |
| **Kioxia** | 일본 | 6600.T | 3D NAND 제조, SanDisk JV 파트너 | 2024 도쿄 IPO, 성장 가속 |
| **Renesas** | 일본 | 6723.T | 엣지 AI MCU/MPU | 산업용 사이클 바닥 |
| **SK하이닉스** | 한국 | 000660.KS | HBM 1위 (57-62% 점유) | **Forward P/E ~8x** (별도 분석 완료) |

> TSMC Forward P/E ~24x는 연 30% 성장 기업치고 저렴하다. 모든 AI 칩이 TSMC를 거치므로 "누가 이기든 TSMC는 수혜"라는 구조. 대만 지정학 리스크가 할인 요인.

---

## 4. 최종 관심 종목 요약 (밸류에이션 + 해자 + 추론 수혜 기준)

### Tier 1: 강한 확신 (합리적 밸류에이션 + 강한 해자 + 추론 직접 수혜)

| 종목 | 티커 | Forward P/E | 핵심 논거 |
|------|------|------------|----------|
| **SK하이닉스** | 000660.KS | ~8x | HBM 독과점, 추론 메모리 대체 불가 (기존 분석 참조) |
| **SanDisk** | SNDK | ~18x | 추론 KV 캐시 오프로드 직접 수혜, NVIDIA ICMSP 표준, 엔터프라이즈 SSD 55% |
| **Modine Manufacturing** | MOD | ~20x | AI 냉각 순수 노출, Vertiv 절반 밸류에이션, DC 매출 +60% |
| **TSMC** | TSM | ~24x | 모든 AI 칩 제조, 2026 매출 +30%, 5년 CAGR 25% |

### Tier 2: 주시 (좋은 포지셔닝이나 밸류에이션 또는 리스크 주의)

| 종목 | 티커 | 이유 |
|------|------|------|
| **Marvell** | MRVL | 커스텀 ASIC + 포토닉스, 4대 하이퍼스케일러 관계. 밸류에이션 주의 |
| **Lattice Semi** | LSCC | 엣지 AI FPGA 독점, 68% GM. 사이클 회복 타이밍 불확실 |
| **Coherent Corp** | COHR | AI 데이터컴 성장 +23%, 광 부품 포트폴리오 |
| **Vertiv** | VRT | Forward P/E ~30x, 냉각 업계 1위이나 MOD 대비 비쌈 |

### Tier 3: 고위험 워치 (옵션성 높으나 실적 미검증)

| 종목 | 티커 | 이유 |
|------|------|------|
| **Navitas Semi** | NVTS | GaN/SiC 전력 반도체, 800V DC 전환 수혜. 아직 소규모, 흑자전환 전 |
| **Kioxia** | 6600.T | 도쿄 IPO 후 성장 가속, 332층 NAND. 유동성/정보 제한 |

---

## 5. 기존 분석과의 연결

README.md의 핵심 테제("추론 시대 최대 수혜 = DRAM/HBM, SK하이닉스 fPER 8배")는 유지된다.

이 문서는 **DRAM/HBM 레이어 다음으로 수혜받는 인프라 레이어**를 분석한 것이다:

```
[GPU/HBM] ← 기존 분석 (SK하이닉스)
    ↓
[네트워킹/인터커넥트] ← Marvell, Coherent, Fabrinet
    ↓
[스토리지 (NVMe SSD)] ← SanDisk, Kioxia
    ↓
[냉각] ← Modine, Vertiv
    ↓
[전력] ← MPWR, Navitas
    ↓
[테스트] ← Advantest
    ↓
[파운드리] ← TSMC
```

**핵심 인사이트**: 추론(Inference) 스케일링은 학습(Training)과 달리 **모든 레이어를 동시에 확장**해야 한다. 학습은 GPU 클러스터 하나를 키우면 되지만, 추론은 전 세계 사용자에게 동시에 서빙해야 하므로 네트워킹, 스토리지, 냉각, 전력이 모두 병목이 된다.

---

## Sources

- [NVIDIA BlueField-4 ICMSP 발표](https://nvidianews.nvidia.com/news/nvidia-bluefield-4-powers-new-class-of-ai-native-storage-infrastructure-for-the-next-frontier-of-ai)
- [NVIDIA KV Cache Offload to NVMe SSDs](https://blocksandfiles.com/2026/01/06/nvidia-standardizes-gpu-cluster-kv-cache-offload-to-nvme-ssds/)
- [TrendForce: Memory Wall Bottleneck](https://www.trendforce.com/insights/memory-wall)
- [Goldman Sachs: AI Data Center Power 165% increase](https://www.goldmansachs.com/insights/articles/ai-to-drive-165-increase-in-data-center-power-demand-by-2030)
- [Data Center Power Revolution 2026](https://www.datacenterknowledge.com/operations-and-management/2026-predictions-ai-sparks-data-center-power-revolution)
- [AI Interconnects Outpacing GPUs](https://www.ainvest.com/news/shifting-power-ai-infrastructure-interconnects-outpacing-gpus-strategic-play-2601/)
- [The Second Wave: AI Networking and Storage Picks and Shovels](https://markets.financialcontent.com/stocks/article/marketminute-2026-1-1-the-second-wave-why-2026-marks-the-great-rotation-into-ai-networking-and-storage-picks-and-shovels)
- [Silicon Photonics Commercial Breakthrough 2026](https://www.digitimes.com/news/a20251229PD203/siph-cpo-optical-communications-broadcom-nvidia-2026.html)
- [NVIDIA Spectrum-X Photonics](https://nvidianews.nvidia.com/news/nvidia-spectrum-x-co-packaged-optics-networking-switches-ai-factories)
- [Liquid Cooling Market $16.16B by 2030](https://www.globenewswire.com/news-release/2026/02/04/3232076/28124/en/Data-Center-Liquid-Cooling-Market-Report-2026-16-16-Bn-Opportunities-Trends-Competitive-Landscape-Strategies-and-Forecasts-2020-2025-2025-2030F-2035F.html)
- [Modine vs Vertiv Cooling Analysis](https://247wallst.com/investing/2026/01/16/3-stocks-are-betting-on-data-center-cooling-heres-whos-best-positioned/)
- [SanDisk Enterprise SSD Price Doubling](https://www.tomshardware.com/pc-components/ssds/sandisk-to-double-price-of-3d-nand-for-enterprise-ssds-in-q1-2026-hyperscalers-to-pay-top-dollar-for-storage-as-ai-continues-to-roll)
- [SanDisk AI Storage Pure-Play](https://markets.financialcontent.com/stocks/article/predictstreet-2026-1-9-sndk-surge-why-sandisk-is-the-pure-play-ai-storage-winner-of-2026)
- [SanDisk Kioxia JV Extension to 2034](https://finance.yahoo.com/news/sandisk-extends-kioxia-venture-ai-010847397.html)
- [Custom ASIC vs GPU Market](https://markets.financialcontent.com/stocks/article/tokenring-2026-1-5-the-silicon-sovereignty-era-hyperscalers-break-nvidias-grip-with-3nm-custom-ai-chips)
- [Marvell Celestial AI Acquisition](https://optics.org/news/16/11/47)
- [Advantest AI Testing Wave](https://www.rcrwireless.com/20260130/test-measurement/advantest-rises-with-the-ai-tide)
- [MPWR Enterprise Data +50% Growth](https://seekingalpha.com/news/4548358-monolithic-power-systems-signals-floor-of-50-percent-enterprise-data-growth-for-2026-amid)
- [Navitas 800V Data Center Power](https://seekingalpha.com/article/4861600-navitas-2-0-gan-and-sic-powerhouse-pivoting-into-the-ai-data-center-boom)
- [Lattice Semi Edge AI FPGA](https://beyondspx.com/quote/LSCC/analysis)
- [TSMC 2026 Undervalued](https://www.fool.com/investing/2026/01/14/artificial-intelligence-ai-semiconductor-stock-tsm/)
- [Fidelity AI Stocks Outlook 2026](https://www.fidelity.com/learning-center/trading-investing/AI-outlook)
- [Edge AI Chips Market $11.54B by 2031](https://www.mordorintelligence.com/industry-reports/edge-artificia-intelligence-chips-market)
- [Kioxia 332-layer BiCS10 Production 2026](https://www.tomshardware.com/pc-components/ssds/kioxias-next-gen-3d-nand-production-gets-expedited-to-2026-report-claims-high-capacity-332-layer-bics10-devices-to-sate-growing-demand-from-ai-data-centers)
