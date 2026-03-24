# How To Keep Your Job 번역

- 발표자: Dave Thomas
- 자료 공동 제작: Dave Thomas, Andy Hunt
- 원문 기반: [How-To-Keep-Your-Job-archived-reconstruction.pdf](/Users/juniq/ai-agent/How-To-Keep-Your-Job-archived-reconstruction.pdf)
- 주의: 이 문서는 웹 아카이브에서 복원한 슬라이드 HTML과 발표자 노트(speaker notes)를 바탕으로 한국어 번역본을 정리한 것입니다.
- 발표 맥락: 이 자료는 2003년 3월 24일 기준으로 이미 Slashdot에서 소개된 공개 발표 자료입니다. 다만 현재 공개적으로 확인 가능한 자료만으로는 이 발표가 처음 어디 행사/어느 장소에서 이루어졌는지는 특정되지 않습니다.
- 관련 정황: 슬라이드 노트에는 `Jay's symposium` 언급이 남아 있고, 자료 소개문도 단수 발표가 아니라 여러 발표(presentations)를 바탕으로 한 슬라이드라고 설명합니다. 따라서 특정 단일 행사 자료라기보다 여러 자리에서 사용된 강연 자료일 가능성이 있습니다.

## 표지

### 슬라이드 1

**직업을 지키는 법 (How to Keep Your Job)**  
데이브 토머스(Dave Thomas)  
더 프래그매틱 프로그래머스(The Pragmatic Programmers, LLC)

노트:
- 프로그래머가 가득한 방(roomful of programmers)과 작년 크리스마스 전구 상자(a box of last year's Christmas lights)의 차이가 뭔가? 내년에도 아직 작동하는 건 전구 쪽일지도 모른다.
- 지금은 경기 하강(downturn) 국면이 분명하지만, 쏟아지는 나쁜 뉴스 때문에 더 심각한 구조적 문제(underlying news)를 놓치고 있다.

### 슬라이드 2

> “공학(engineering)을 직업(career)으로 보는 사람들에게, 지금의 엔지니어링은 수년 사이 최악의 상태다.”

리얼 브라이언트(LeEarl Bryant), IEEE 회장(President), 2002년

노트:
- 오해하지 말라. 우리의 현재 경력(career) 자체가 위협받고 있다.
- 이 방에 있는 사람들의 절반은 5년 뒤 개발자(developer)가 아닐 수도 있고, 10년 전망은 더 나쁘다.
- 그런데도 우리는 주택담보대출(mortgage)을 갚아야 하고, 가족을 부양해야 하고, 갖고 싶은 장난감도 산다.
- 그러면 우리는 무엇을 해야 하는가? 이 발표는 그 질문에 대한 것이다.

### 슬라이드 3

**우리의 미래(Our Future)는 걸려 있다**

- 우리의 생계(livelihood)를 위협하는 요소를 본다.
- 왜 대규모 해법(large-scale solutions)이 우리를 구하지 못하는지 본다.
- 우리 각자에게 실제로 도움이 되는 로컬 해법(local solution)을 본다.

### 슬라이드 4

**위협들(The Threats)**

노트:
- 오늘은 큰 위협 세 가지를 보겠다. 실제로는 더 많다.
- 닷컴 붕괴 이후(ex dot com developers) 시장에 유입된 배경 약한 개발자들까지 포함하면 훨씬 복잡하지만, 여기서는 장기적으로 지속되는 위협(longer term threats)에 집중한다.

## 위협

### 슬라이드 5

> “공학 지식(engineering knowledge)의 반감기(half-life), 즉 어떤 것이 구식(obsolete)이 되기까지 걸리는 시간은 7년에서 2.5년 사이이다.”

윌리엄 울프(William Wulf), 미국공학한림원(National Academy of Engineering) 회장

**세상은 너무 빨리 변한다 (Things Move Too Fast)**

노트:
- 반감기(half-life)라는 표현은 일단 흥미롭지만, 핵심은 우리가 열심히 배운 것이 몇 년 안에 쓸모를 잃는다는 점이다.
- 가만히 들어보라. 째깍거리는 소리는 우리의 지식(knowledge)이 점점 가치(value)를 잃어가는 소리다.
- 그리고 더 나쁜 건, 어떤 사람들은 이 변화 속도를 더 유리하게 이용하고 있다는 점이다.

### 슬라이드 6

**나이 들어가는 개발자(The Graying Developer)**

- 더 젊은 사람들(younger folks)은 새 기술(new technologies)과 함께 성장한다.
- 그들은 더 저렴하다(are cheaper).
- 덜 자주 “안 됩니다(no)”라고 말한다.
- 다른 책임(commitments)이 상대적으로 적다.

노트:
- 뒤에서 들어오는 사람들은 우리보다 더 앞선 출발선에서 시작한다.
- 오래된 기술에 대한 짐(baggage)이 적고, 급여 기대치도 낮다.

### 슬라이드 7

**나이 들어가는 개발자(The Graying Developer)**

- 젊은 사람들은 종종 고용주(employers)에게 더 매력적으로 보인다.

노트:
- 젊은 개발자라서 지금 우쭐해하고 있다면 기억하라. 당신도 5년 뒤에는 “나이 든 프로그래머(old programmers)”가 된다.
- 새 기술을 따라잡는 문제 외에도 우리는 다른 위협을 동시에 맞고 있다.

### 슬라이드 8

**섹터 의존(Reliance on a Sector)**

- “나는 XYZ 프로그래머다.”
- 또는 특수한 경우로 “나는 자바(Java) 프로그래머다.”
- 우리는 특정 기술(technologies)과 그 기술을 후원하는 회사(companies)에 의존하게 된다.

노트:
- “전문화(specialization)는 곤충을 위한 것이다”라는 말이 있지만, 현실은 우리를 계속 전문화 쪽으로 밀어 넣는다.
- 게으른 고용주와 말도 안 되는 채용 공고(job ads), 지나치게 넓어진 분야(field) 때문에 점점 좁은 구석으로 몰린다.
- 결국 우리는 “개발자(developer)”가 아니라 특정 기술 라벨로 자신을 정의하게 되고, 경력(career)과 미래(future)를 그 기술과 그 배후 회사에 걸게 된다.

### 슬라이드 9

**회사 의존(Reliance on a Company)**

- 예시 회사:
- 디지털 이큅먼트(Digital Equipment)
- 탠덤(Tandem)
- 허니웰(Honeywell)
- 그리고 선(Sun)...

### 슬라이드 10

**섹터 의존(Reliance on a Sector): 선 마이크로시스템즈(Sun Microsystems) 2년 주가**

노트:
- 선(Sun)의 주가가 현금 보유 수준 정도로 내려가면, 자바(Java)도 더 이상 그렇게 안전해 보이지 않는다.
- IBM 같은 회사가 중간에 들어올 수는 있겠지만, CTO나 CIO 입장에서는 “선이 사라질 수 있다”는 사실 자체가 자바의 리스크 인식(perception of risk)을 바꾼다.

### 슬라이드 11

**섹터 의존(Reliance on a Sector): 선(Sun) 대 마이크로소프트(Microsoft)**

노트:
- 첫 번째 위협은 기술 노후화(technical obsolescence)였고, 두 번째는 한 바구니에 모든 달걀(all your eggs in one basket)을 넣는 문제였다.
- 이제 세 번째 위협으로 넘어간다.

### 슬라이드 12

**시장(The Market)**

본문 요지:
- 실업률이 오르는 가운데, 미국의 생산직(production jobs)이 중국으로 이동하고 있다는 CNN 기사 인용이 나온다.
- 특히 오래 일한 사람들의 고임금 일자리(higher-wage jobs)까지 이동하고 있다는 점을 강조한다.

노트:
- 우리는 자본주의(capitalism) 세계에 살고 있고, 시장(market)이 왕이다.
- 시장은 다윈식(Darwinian) 선택처럼 작동하며, 고객(customer)의 판단이 누가 살아남을지를 결정한다.
- 소프트웨어 개발(software development)에도 시장이 있고, 이제 그 시장은 전 세계적(world-wide)이다.
- 상품화(commoditized)된 산업이 더 싼 노동력 지역으로 이동하는 것은 흔한 흐름이다.
- 문제는 이제 고급 기술(high tech)과 소프트웨어 개발 자체가 점점 상품화되고 있다는 점이며, 바로 우리가 그 영향을 맞는다.

### 슬라이드 14

**향후 15년간 거의 100만 개의 IT 관련 일자리가 해외(offshore)로 이동한다**

노트:
- 이는 전체 해외 이전 일자리 약 300만 개 가운데 IT 관련 일자리만 거의 100만 개라는 뜻이다.

### 슬라이드 15

**왜? (WHY?)**

### 슬라이드 16

**이전하는 이유(Reasons to Move)**

- 때로는 정치적(political) 이유
- 때로는 비용(cost)
- 젊은 개발자가 더 저렴한 것과 같은 논리
- 종종 품질(quality) 때문이기도 함

노트:
- 특정 국가에서 팔고 싶다면 일정 비율을 그 나라에서 생산해야 하는 정치적 요구가 있다.
- 해외 기업은 오버헤드(overhead)가 낮다.
- 하지만 “싸니까 품질이 낮다(lower quality)”고 가정하는 건 큰 실수다.
- 어떤 경우에는 해외 위탁(outsource) 쪽이 오히려 품질이 더 높아서 일을 넘긴다.

### 슬라이드 17

**해외 개발자들(Overseas developers)도 좋은 코드(good code)를 쓸 수 있다**

노트:
- 모두가 다 잘 쓰는 건 아니지만, 7~10년 동안 아웃소싱(outsourcing)을 해온 나라들 중 많은 곳은 표준적인 상용 애플리케이션(standard commercial applications)을 높은 품질로 만들어낼 수 있다.

### 슬라이드 18

**CMM(Capability Maturity Model)**

- 소프트웨어 개발 조직(software development organizations)의 성숙도(sophistication)를 측정한다.
- 단계별 목표(targets) 집합처럼 작동한다.
- 다섯 개의 CMM 레벨(levels)이 있다.

노트:
- 청중에게 CMM을 들어본 적 있는지, 회사가 CMM 프로그램에 참여하는지 묻는다.
- 그 다음 “레벨(level)”이 무엇을 뜻하는지 설명한다.

### 슬라이드 19

**CMM 레벨(CMM Levels)**

- 레벨 1(initial): 규칙이 거의 없고 영웅적 노력(heroic effort)에 의존
- 레벨 2(repeatable): 기본적인 프로젝트 관리(project management)는 있지만 프로젝트마다 다름
- 레벨 3(defined): 조직 전반의 개발 방식이 같은 규칙을 따름

노트:
- 영웅적 노력(heroic effort)이란 개발자가 계속 불 끄기(fight fires)를 하며 프로젝트를 겨우 굴리는 상태다.
- CMM은 단순히 결과(outcome)만이 아니라 그 결과에 도달한 방식(process)도 본다.

### 슬라이드 20

**CMM 레벨(CMM Levels)**

- 레벨 4(managed): 정밀한 측정(measurements)으로 개발을 통제
- 레벨 5(optimizing): 이전 프로젝트의 정량적 피드백(quantitative feedback)으로 다음 프로젝트를 개선

노트:
- 여기서는 측정(measuring)을 통해 통제(control)하려는 시도가 시작된다.
- 마지막 단계에서는 그 정보를 다시 피드백(feedback)으로 써서 프로세스(process)를 개선한다.
- 진지하게 CMM을 도입한 회사는 보통 레벨을 하나 올리는 데 2년에서 2.5년 정도 걸린다.

### 슬라이드 21

**CMM 레벨 4**

노트:
- 2002년 8월 기준 SEI 조사에 따르면 레벨 4 회사는 82개이며, 미국(US)은 34개, 해외(overseas)는 48개다.

### 슬라이드 22

**CMM 레벨 5**

노트:
- 전 세계 CMM 레벨 5 회사는 76개이고, 그중 미국 기반은 13개뿐이다.
- 나머지 63개는 해외이며, 특히 인도(India)에 많다.
- 이게 해외 아웃소싱 회사들의 마케팅(marketing)일 수는 있다.
- 하지만 시급 40달러에 CMM 레벨 5 품질을 증명할 수 있는 회사와, 시급 200달러이면서 품질 표준도 입증하지 못하는 국내 회사 중 어디로 일이 갈지는 분명하다.
- 이건 미래가 아니라 현재(now)의 일이다.

### 슬라이드 23

> “이것이 새로운 세계(the new world)다. 이를 인정하지 않는 것은, IBM이 1980년대에 PC와 범용 하드웨어(commodity hardware)의 중요성을 인식하지 못했던 것과 다르지 않다.”

노트:
- 발표자는 이 문장을 읽고, 이어서 더 직설적인 다음 말을 소개한다.

### 슬라이드 24

> “문제의 상당 부분은 오만함(arrogance)이다. ‘그들(They)’이 ‘우리(us)’보다 더 나을 리 없다고 생각한다. 우리는 너무 똑똑하다고 믿는다.”

노트:
- 지금까지 본 위협은 세 가지다.
- 기술 노후화(technical obsolescence)
- 한 바구니에 모든 걸 담는 위험(eggs in one basket)
- 소프트웨어 개발의 상품화(commoditization)와 더 싼 나라로의 이전(migration)

### 슬라이드 25

**위협 요약(Threat Summary)**

- 손쉬운 호황(gravy train)은 이제 힘을 잃어가고 있다.

노트:
- 삶은 바뀔 것이다.
- 그러면 우리는 무엇을 할 수 있는가?

## 해법

### 슬라이드 26

**해결책들(Solutions)**

노트:
- 몇 가지 해법을 보자.
- 첫 두 가지는 실제로는 통하지 않는다.
- 마지막 한 가지가 사실상 유일한 희망이다.

### 슬라이드 27

**정부에 의존하기(Rely on Government)**

- 아웃소싱 금지 입법(legislate against outsourcing)
- H1B 상한(cap) 축소
- 어쩌면 수입 소프트웨어에 관세(tariffs)
- 또는 무작위 입법(legislate randomly)

노트:
- 뉴저지(NJ) 법안처럼 공공 프로젝트 예산은 미국 내 일자리로 이어져야 한다는 식의 논리가 있다.
- H1B 이슈도 자주 등장한다.
- 하지만 이런 접근은 경제학적으로는 보호무역(protectionism)이다.

### 슬라이드 28

**보호무역(Protectionism)**

- 통하지 않는다(doesn't work)
- 경제적 이유: 국가 전체로 보면 오히려 해롭다
- 실무적 이유:
- GE, EDS, IBM 같은 회사는 전 세계에 사무실이 있다
- 애초에 집행(enforcement)도 어렵다

노트:
- 소프트웨어 개발 1억 달러어치를 이메일(e-mail)이나 DVD 한 장으로 보내는 시대에 정보에 관세를 매긴다는 게 가능한가?
- 설령 가능하더라도 우리는 값싼 소프트웨어 접근(access)을 잃고, 다른 나라만 이익을 보게 된다.
- 개인 개발자의 고통보다 국가 전체의 경쟁력(competitiveness)이 더 큰 문제로 취급될 가능성이 높다.

### 슬라이드 29

**H1B 쿼터(H1B Quotas)**

- 2003년 H1B 비자 19만 5천 개
- 이후 6만 5천 개
- 그해에는 상한(cap)도 채우지 못함

노트:
- H1B는 숙련 인력(shortage of skilled workers) 부족을 메우려는 제도로 도입됐다.
- 다수의 H1B는 IT 분야에 있다.
- 학위(degree) 또는 상당한 경력(work experience)이 필요하고, 미국 회사의 스폰서(sponsorship)가 있어야 한다.
- 원래 법은 H1B가 미국 근로자(local workers)를 대체하지 못하게 하려는 장치다.
- 문제는 제도 자체보다 기업 차원의 부패(corruption)다.
- 급여를 속이고, 필요 인력을 과장하고, H1B 채용 뒤 90일 후 현지 인력을 해고하는 회사들은 처벌(prosecuted)해야 한다.
- 그렇다고 제도 전체를 없애는 건 해법이 아니다.

### 슬라이드 30

**H1B 쿼터(H1B Quotas): 대폭 줄이면?**

- 일자리는 해외(jobs move abroad)로 더 빨리 이동한다.
- 우리는 경험(experience)에 대한 접근(access)을 잃는다.

노트:
- H1B가 미국에 값싼 프로그래머를 제공한다는 사실을 인정한다면, 제도를 없애는 순간 기업은 통째로 프로젝트를 해외로 보내 버릴 가능성이 크다.
- 동시에 우리는 세계의 훌륭한 프로그래머들로부터 배울 기회도 잃는다.

### 슬라이드 31

**회사에 의존하기(Rely on our Companies)**

- 회사의 동기(motivation)는 무엇인가?
- 신입 졸업생(new graduates)이 더 싸고 더 오래 일함
- 해외 개발자(offshore programmers)가 더 싸고 품질도 괜찮음
- 심지어 도구(tools)가 사람들보다 더 믿을 만하다고 생각하기도 함

노트:
- 회사가 교육(training)을 제공하는 경우도 있지만, 그것은 결국 회사의 단기적 필요(short-term needs)를 위한 것이다.
- 개발자 개인에게 간접적인 도움은 되지만, 회사가 우리 장기 경력(long-term career)을 책임져주지는 않는다.

### 슬라이드 32

**결국 우리 스스로에게 달렸다(Rely on Ourselves)**

- 정부(government)는 해주지 않는다.
- 회사(companies)도 해주지 않는다.
- 각자(each of us)가 해야 한다.

노트:
- 누가 도와줄 것인가? 요약하면 다음 세 단어다.

### 슬라이드 33

**자기 자신에게 투자하라(Invest in Yourself)**

노트:
- 이 발표에서 딱 하나만 기억한다면 이 세 단어를 기억해 달라.
- 그렇다면 자기 투자(invest in yourself)는 구체적으로 무엇을 뜻하는가?
- 개인 재무(personal finance) 영역에서 힌트를 얻을 수 있다.

## 자기 투자

### 슬라이드 34

**개인 재무(Personal Finance)에서 배우는 교훈**

좋은 투자자(good investors)는:
- 계획(plan)이 있다
- 분산(diversify)한다
- 가치(value)를 본다
- 수동적(passive)이 아니라 능동적(active)이다
- 정기적으로 한다(do it regularly)

노트:
- 은퇴(retirement), 자녀 대학 등록금(college), 보트 구매처럼 목표(objective)에 따라 투자 방식이 달라진다.
- 엔론(Enron) 사례처럼 분산(diversification)은 필수다.
- 가치(value)는 펀더멘털(fundamentals)을 봐야지, 유행(hype)만 봐서는 안 된다.
- 능동적(active)이라는 건 계속 포트폴리오(portfolio)를 점검하고 필요하면 리밸런싱(rebalance)한다는 뜻이지, 무작정 들쑤신다는 뜻이 아니다.
- 정기적 투자(regular investing)는 습관(habit)이 되어야 한다.

### 슬라이드 35

**지식 포트폴리오(Knowledge Portfolio)**

- 가치(value)는 우리가 아는 것(what we know)과
- 그것을 적용하는 법(knowing how to apply it)에서 나온다.

노트:
- 금융 포트폴리오(finance portfolio)가 주식, 채권, 현금 등으로 구성되듯, 경력(career)에서의 포트폴리오는 우리가 아는 것과 그것을 적용하는 능력이다.
- 이 포트폴리오의 가치는 사람들이 “당신이 그것을 얼마나 잘 해낼 수 있는지”를 어떻게 판단하느냐에 달려 있다.

### 슬라이드 36

**계획을 가져라(Have a Plan)**

- 변화 속도(pace of change)를 고려하라.
- 현재 유행(current fads) 너머를 보라.

노트:
- 산업(industry)이 어디로 가는지 스스로 판단해야 한다.
- 조사(research)를 하고, 트렌드(trends)를 보고, 사람들과 이야기하고, 논문·잡지·책을 읽어야 한다.
- 유행(fad)이 아니라 탄탄한 흐름(solid trends)을 찾아야 한다.
- 그리고 그 안에서 자신이 어디에 들어갈지 정하고, 그 차이(gap)를 메우는 계획을 세워야 한다.

### 슬라이드 37

**계획 예시 1(Have a Plan: Example 1)**

당신이 믿는 것:
- 아웃소싱(outsourcing)은 계속 증가한다.
- 내 기술 역량(technical skills)은 가려질 수 있다.

### 슬라이드 38

**계획 예시 1: 실행 계획**

- 지금(Now): 분산 프로젝트 구현 도구(distributed project implementation tools)에 익숙해진다.
- 내년(Next Year): 외주 프로젝트 관리(outsourced project management)에 참여할 길을 본다.
- 앞으로 몇 년(Coming Years): 외국어(foreign language)를 배운다.

### 슬라이드 39

**계획 예시 2(Have a Plan: Example 2)**

당신이 믿는 것:
- 코딩(coding)은 점차 모델링(modeling)에 밀릴 수 있다.
- 나는 평균보다 커뮤니케이션 능력(communications skills)이 좋다.
- 변화가 다양한 일(varied job)을 좋아한다.

### 슬라이드 40

**계획 예시 2: 실행 계획**

- 지금(Now): MDA(Model Driven Architecture)에 대해 배우기 시작하고, 책을 읽고 메일링 리스트(ML)를 구독한다.
- 내년(Next Year): 자신만의 각도(angle)를 찾고, 관리층 대상 매체(management press)에 글을 쓰기 시작하며, 작은 시범 프로젝트(trial project)를 해본다.
- 앞으로 몇 년(Coming Years): 관리 컨퍼런스(management conferences)에서 MDA 발표를 하고, 고액 국제 컨설턴트(high-paid international consultant)가 된다.

### 슬라이드 41

**계획 예시 3(Have a Plan: Example 3)**

당신이 믿는 것:
- 나는 뛰어나고 직관적인(intuitive) 개발자다.
- 코딩 도전(coding challenges)을 즐긴다.
- 계속 기술적인 사람(technical)으로 남고 싶다.

### 슬라이드 42

**계획 예시 3: 실행 계획**

- 지금(Now): 아웃소싱되지 않을 영역(outsourced 되기 어려운 영역)을 찾는다.
- 예: 핵심 비즈니스(core business), 신기술(emerging technologies), 국방(defense), 임베디드(embedded), 인프라(infrastructure)
- 내년(Next Year): 그런 영역에서 코드를 쓰기 시작한다. 일자리가 없으면 오픈소스(open source)로 시작한다.
- 앞으로 몇 년(Coming Years): 글을 쓰고, 발표하고, 인정받는 전문가(recognized expert)가 된다.

### 슬라이드 43

**분산하라(Diversify)**

- 모든 달걀(all your eggs)을 하나의 기술 바구니(technology basket)에 담지 말라.
- 여러 차원(multiple dimensions)에 걸쳐 분산하라.
- 언어(languages)
- 기법(techniques)
- 산업(industries)
- 비기술(non-technical)

노트:
- 특정 몰락 기술(Enron technology)의 전문가만 되어 남고 싶지는 않을 것이다.
- 분산은 리스크(risk)를 줄이고, 동시에 일부 고위험·고수익(high risk/high reward) 지식을 포함해 수익(return)을 늘릴 수 있게 한다.

### 슬라이드 44

**분산하라(Diversify): 위험/수익 조합**

- 낮은 위험/낮은 수익(low risk, low return)도 일부 가져라.
- 예: .NET, 웹 서비스(Web Services), 모바일 기기(mobile devices), MDA
- 높은 위험/높은 수익(high risk, high return)도 일부 가져라.
- 예: AOP/애스펙트(Aspects), 의도적 프로그래밍(Intentional Programming), 함수형 프로그래밍(functional programming)
- 이런 흐름을 일찍 식별하고 가능한 한 초기에 참여하라.

노트:
- 파도(wave)를 잘 타면 경력을 크게 가속할 수 있다.
- 다만 당장 생업(day job)을 버리라는 뜻은 아니다.

### 슬라이드 45

**분산하라(Diversify): 기억할 점**

- 거의 모든 투자(investments)는 어느 정도 수익(return)이 있다.
- AOP, Haskell 같은 것을 배우는 일은 언제나 당신을 더 나은 개발자(better developer)로 만든다.
- 비기술 축(non-technical axis)도 잊지 말라.

노트:
- 금융 투자(financial investing)와 달리, 지식 포트폴리오(knowledge portfolio)는 거의 항상 어떤 형태로든 축적 수익이 있다.

### 슬라이드 46

**가치를 찾아라(Look for Value)**

- 가치(value)는 장기적(long term)이다.
- 시간(time)과 가치(value)는 같지 않다.
- 에버퀘스트 증후군(EverQuest syndrome): 시간을 많이 썼다고 가치가 생기는 건 아니다.
- 적용 가능성(applicability)을 보라.
- 그러나 분산(diversity)도 잊지 말라.
- 이론(theoretical)만으로 끝내지 말고, 적용하고 피드백(feedback)을 받아라.

노트:
- 금융에서는 돈을 써서 더 많은 돈을 만들고, 직업 포트폴리오(professional portfolio)에서는 시간을 써서 더 큰 지혜(wisdom)를 쌓는다.
- 단순히 시간을 들였다는 사실 자체는 가치(value)를 보장하지 않는다.
- 축적 중인 지식이 진짜 가치 있는지 확인하려면 피드백(feedback)을 찾아야 한다.
- 경력 초반 사람들에게는 급여(salary)보다 경험의 질(quality of experience)을 보라고 조언한다.

### 슬라이드 47

**능동적 투자자(Active Investor)**

- 주기적으로 자신의 지식 포트폴리오(knowledge portfolio)를 평가하라.
- 계획대로 작동하고 있는가?
- 외부 환경(external circumstances)이 바뀌었는가?
- 리밸런싱(rebalance)할 때인가?

노트:
- 피드백(feedback)은 모든 일에서 중요하다.
- 내 계획이 잘 되고 있는가?
- 아직도 유효한가?
- 내가 올바른 일을 하고 있는가?
- 올바른 방식으로 하고 있는가?
- 애초에 그 일을 할 필요가 있는가?

### 슬라이드 48

**정기적으로 투자하라(Invest Regularly)**

- 매달 최소한의 시간(minimum amount of time)을 투자하라.
- 의식(ritual)이 있으면 도움이 된다.
- 자신에게 맞는 방식이면 된다.
- 시간을 미리 계획(plan time in advance)하라.
- 그냥 앉아서 “오늘 뭘 하지?” 하지 말라.

노트:
- 자연스럽게 되지 않는 일을 습관으로 만들려면 의식(ritual)이 도움이 된다.
- 매달 최소 n시간은 반드시 투자하겠다고 약속(commitment)해야 한다.

### 슬라이드 49

**프래그매틱 투자 계획(Pragmatic Investment Plan, PIP)**

- 매주 최소 2시간(two hours each week) 투자하라.
- 좋을 때도, 나쁠 때도(good times and bad)
- 개인 학습(individual)과 그룹 학습(group)을 함께 섞어라.
- 점점 커지는 국가적 커뮤니티(national community)를 활용하라.

노트:
- “2시간을 어디서 찾느냐?”라는 질문이 나오겠지만, 지금 투자하지 않으면 나중에는 일자리를 잃고 정말 시간이 넘칠지도 모른다.
- 혼자 하지 말고 그룹과 개인 학습을 섞어라.

### 슬라이드 50

**PIP: 가능한 일정 예시(Possible Schedule) 1**

- 한 달에 1주(one week/month)는 사용자 그룹(user group) 모임에 쓴다.
- 2년에 한 번쯤 발표(talk)를 하도록 계획한다.
- 발표 준비를 위해 PIP 시간을 6~8주 정도 따로 잡는다.

노트:
- 단순 참석이 아니라 적극적 참여(active participation)를 고민하라.
- 아직 발표를 해본 적 없다면 진지하게 준비해보라.
- 예: 단위 테스트(unit testing), 자바 API(Java API), 데이터베이스(database), 설계 기법(design technique), 배포(deploying applications)

### 슬라이드 51

**PIP: 가능한 일정 예시 2**

- 한 달에 1주는 새로운 언어(language)나 환경(environment)을 배운다.
- 지금 하는 것과 다른 것으로 선택하라.
- 예: 자바(Java) 개발자라면 C#과 .NET을 배워본다.
- 많은 언어와 환경에는 무료 소프트웨어(free software)가 उपलब्ध하다.
- 가능하면 지역 스터디 그룹(local study group)을 만들어라.

### 슬라이드 52

**PIP: 가능한 일정 예시 3**

- 한 달에 1주는 수준 높은 책(high-quality book)을 읽는다.
- 저수준 레시피 책(low-level recipe books)은 피하라.
- 개념서(concept books)를 보라.
- 비기술 서적(non-technical books)도 잊지 말라.

### 슬라이드 53

**비기술 서적(Non-Technical Books)**

- 적용 가능한 정보(applicable information)의 금광(gold-mine)이다.
- 예:
- 《즉석 도구로 자물쇠 여는 법(How to Open Locks with Improvised Tools)》, Hans Conkel
- 《초보자에서 전문가로(From Novice to Expert)》, Patricia Benner
- 《선과 모터사이클 관리술(Zen and the Art of Motorcycle Maintenance)》, Robert M. Pirsig

### 슬라이드 54

**PIP: 가능한 일정 예시 4**

- 한 달에 1주는 자신의 개인 계획(personal plan)을 위해 쓴다.

노트:
- 자신이 세운 개별 계획(individual plan)의 목표(objective)를 향해 실제로 전진하라.

### 슬라이드 55

**프래그매틱 투자 계획(Pragmatic Investment Plan)**

- 다른 사람들과 함께하라(work with others).
- 4~6개월마다 계획(plan)을 되돌아보라(reflect).
- 시간이 많을수록 적은 것보다 낫다.
- 가능하다면 회사와 협의해서 격주 금요일 오후(alternate Friday afternoons)를 학습 시간(study time)으로 확보하라.
- 그러려면 계획(plan)을 보여줘야 한다.

## 장기 결론

### 슬라이드 56

**장기적으로(In The Long Term)**

- 상황은 계속 더 복잡해질 것이다.
- 일을 둘러싼 경쟁(competition for work)은 더 치열해질 것이다.
- 외부에서 강제로 imposed constraints를 주는 방식은 도움이 되지 않는다.

### 슬라이드 57

**장기적으로(In the Long Term)**

- 우리는 우리 자신을 스스로 챙겨야 한다(look out for ourselves).
- 우리는 우리 자신에게 투자해야 한다(invest in ourselves).
- 우리는 5~10년 앞을 보고 계획해야 한다(plan 5-10 years out).

### 슬라이드 58

**장기적으로(In the Long Term)**

- 우리에게는 통제권(control)이 있다.
- 우리에게는 책임(responsibility)이 있다.
- 우리에게는 기회(opportunity)가 있다.

## 한 줄 요약

이 발표의 핵심은 단순합니다. 정부(government)나 회사(company)가 개발자의 미래를 지켜주지 않으니, 개발자는 변화 속도(change), 기술 수명(obsolescence), 해외 이전(offshore), 경쟁 심화(competition)를 전제로 자기 자신에게 장기적으로 투자(invest in yourself)해야 한다는 주장입니다.
