# 버핏의 DCF 계산

버핏은 WACC를 쓰지 않는다. 멍거가 "워런이 WACC 얘기하는 걸 들어본 적이 없다"고 할 정도. 그의 방식은 세 발언으로 요약된다.

## 1. 할인은 국채 금리로 한다 (1998 주총)

> "우리는 미래 현금흐름을 9%나 10%로 할인하지 않는다. 미 국채 금리(U.S. treasury rate)를 쓴다. 우리는 꽤 확신할 수 있는(quite certain) 것들만 다루려 한다."

> "내재가치를 계산하려면, 창출될 것으로 기대하는 현금흐름을 현재가치로 할인하면 된다 — 우리의 경우, 장기 국채 금리(long-term Treasury rate)로."

> "우리는 모든 증권에 같은 할인율을 쓴다. 대신 어떤 상황에서는 현금흐름 추정을 더 보수적으로 할 수 있다."

- 리스크가 크다고 할인율을 높이지 않는다: **"높은 할인율로 리스크를 보상할 수는 없다(You can't compensate for risk by using a high discount rate)."**
- 리스크 처리는 할인율이 아니라 ① 확실한 기업만 계산 대상으로 선별 ② 현금흐름 추정을 보수적으로 ③ Margin of Safety로 한다.
- 1994년 주총에도 같은 취지 발언. 금리가 비정상적으로 낮을 때는 그 낮은 금리를 그대로 쓰지 않고 정상화한다.

## 2. 기대수익률 10% 미만이면 안 산다 (2003 주총)

> "10%는 우리가 포기하는 기준선이다(10% is the figure we quit on) — 실질 기대수익률(real return)이 10% 미만이면 주식을 사고 싶지 않다. 금리가 6%든 1%든."

버핏 스스로 이 숫자를 "자의적(arbitrary)"이라고 인정했다. 근거는 CAPM이 아니라 기회비용이다. 같은 자리에서 멍거:

> "우리는 미래의 기회비용(future opportunity cost)을 추측하는 것이다. 워런은 앞으로 높은 수익률에 자본을 투입할 기회가 올 거라 보기 때문에, 지금 10% 미만에는 내놓지 않으려는 것이다."

매수가 기준 기대수익률 ≥ 10%는 10%로 할인한 내재가치 ≥ 현재가와 수학적으로 동치. "버핏이 10% 할인율을 썼다"는 이 발언의 재해석이다.

## 3. 공식 할인율도, DCF 스프레드시트도 없다

**1996년 주총**, 멍거:

> "워런이 할인된 현금흐름(discounted cash flows) 얘기는 자주 하는데, 실제로 계산하는 건 한 번도 못 봤다(I've never seen him do one)."

버핏: "어떤 건 혼자 있을 때만 하지(Some things you only do in private, Charlie)." 이어서:

> "연필과 종이로 직접 계산해야 할 정도면, 너무 아슬아슬해서(too close) 고려할 가치가 없다. 엄청난 안전마진이 있다고 그냥 소리를 질러야(scream at you) 한다."

**앨리스 슈뢰더(전기 『스노볼』 작가, 2008 버지니아대 Darden 강연)** — 버핏의 파일 전체를 열람한 유일한 사람:

- "재무 모델(financial model) 비슷한 것도 본 적이 없다."
- Mid-Continent Tab Card 투자(1959): 판단 기준은 "매출 200만 달러에서 15% 수익을 얻을 수 있는가" 하나. 대신 자신과 경쟁사의 손익계산서를 분기별·공장별로 분석해, 경마 핸디캐퍼(horse handicapper)처럼 성패를 가를 한두 가지 요인(매출 성장, 원가 우위)을 골라냈다. 18년 보유, 연 33% 복리 수익.

## 정리

| | 발언 | 실제 의미 |
|---|---|---|
| 이론 | 국채 금리로 할인 (1998) | 할인율은 비교 잣대일 뿐, 리스크는 선별과 MoS로 |
| 실전 | 10% 미만이면 패스 (2003) | 국채 금리 vs 10% 중 높은 쪽이 사실상 할인율 |
| 본심 | 계산 자체를 안 함 (1996) | 정밀한 DCF가 필요한 투자는 애초에 안 함 |

## 출처

- 1996·1998·2003 버크셔 해서웨이 주총 Q&A. 1994년 이전 주총은 공식 기록이 없고, 이후 것도 상당수 참석자 노트(Whitney Tilson 등) 경유라 문구가 자료마다 조금 다름. 복수의 독립 자료가 일관되게 인용. 영상: CNBC Warren Buffett Archive (1994~)
- [25iq — Munger and Buffett on discounting at the 30-year Treasury rate](https://25iq.com/2015/11/21/why-and-how-do-munger-and-buffett-discount-the-future-cash-flows-at-the-30-year-u-s-treasury-rate/)
- [nvariant — Why Warren Buffett never calculates a DCF](https://nvariant.substack.com/p/why-warren-buffett-never-calculates)
- [GuruFocus — Alice Schroeder on How Buffett Values a Business](https://www.gurufocus.com/news/85318/alice-schroeder-on-how-buffett-values-a-business-and-invests)
- [Saber Capital — Buffett Case Study on Investment Filters (PDF)](https://sabercapitalmgt.com/wp-content/uploads/2013/09/buffett_case-study-on-investment-filters-tabulating-company.pdf)

적용 사례: [삼양식품 Buffett-style DCF](../SamyangFood/samyang.md)
