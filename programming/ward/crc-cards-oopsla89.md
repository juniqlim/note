# 객체지향 사고를 가르치는 실험실 (A Laboratory For Teaching Object-Oriented Thinking)
https://c2.com/doc/oopsla89/paper.html
켄트 벡(Kent Beck)과 워드 커닝햄(Ward Cunningham)이 CRC 카드를 처음 소개한 OOPSLA'89 논문을 번역했습니다.

켄트 벡(Kent Beck), 애플 컴퓨터(Apple Computer, Inc.) · 워드 커닝햄(Ward Cunningham), 와이어트 소프트웨어 서비스(Wyatt Software Services, Inc.)

OOPSLA'89 학술대회 논문집(Conference Proceedings), 1989년 10월 1–6일, 루이지애나주 뉴올리언스  
SIGPLAN Notices 특별호, 24권 10호, 1989년 10월

## 목차 (Contents)

1. [문제 (Problem)](#1-문제-problem)
2. [관점 (Perspective)](#2-관점-perspective)
3. [CRC 카드 (CRC Cards)](#3-crc-카드-crc-cards)
4. [경험 (Experience)](#4-경험-experience)
5. [결론 (Conclusion)](#5-결론-conclusion)
6. [참고 문헌 (References)](#참고-문헌-references)
7. [부록 (Appendix)](#부록-appendix)

## 들어가며 (Introduction)

절차적(procedural) 프로그래머에게, 초보든 숙련자든, 객체지향 설계에 필요한 의인화된 관점(anthropomorphic perspective)을 심어 주기는 어렵다. 우리는 학습자가 객체를 직접 경험하게 하는 방법으로 CRC 카드를 소개한다. CRC 카드는 객체를 클래스 이름(class name), 책임(responsibilities), 협력자(collaborators)로 특징짓는다. 우리는 이 방법이 초보 프로그래머에게 객체의 개념을 가르치는 데에도, 숙련된 프로그래머에게 복잡한 기존 설계를 소개하는 데에도 효과가 있음을 확인했다.

## 1. 문제 (Problem)

객체지향 프로그래밍을 가르칠 때 가장 어려운 문제는, 학습자가 절차적 프로그램에서는 가능했던 제어에 대한 전역적 지식(global knowledge of control)을 내려놓고, 객체가 저마다 가진 지역적 지식(local knowledge)에 기대어 일을 해내게 만드는 것이다. 초보자의 설계에는 전역적 사고로 되돌아간 흔적이 널려 있다. 쓸데없는 전역 변수, 불필요한 포인터, 다른 객체의 구현에 대한 부적절한 의존 같은 것들이다.

객체를 배우려면 접근 방식 전체를 바꿔야 하므로, 객체를 가르치는 일은 결국 객체 설계를 가르치는 일이 된다. 초보자에게 기본 개념을 가르칠 때든, 숙련된 객체 프로그래머에게 복잡한 설계의 미묘한 점을 가르칠 때든 우리는 설계에 집중한다.

우리는 객체 설계를 최대한 절차적 설계처럼 보이게 하려 애쓰는 대신, 학습자를 소재의 "객체다움(object-ness)"에 푹 잠기게 하는 것이 객체로 생각하는 관용적 방식(idiomatic way)을 가르치는 가장 효과적인 방법임을 알게 되었다. 그러려면 익숙한 것을 가능한 한 많이 걷어 내야 한다. 문법이나 프로그래밍 환경 조작 같은 세부 사항은 기본을 철저히 이해하고 나면 금방 익힐 것이라고 기대한다.

이런 맥락에서 우리는 객체 설계에 대한 우리의 관점, 그 관점이 구체적으로 드러난 형태인 CRC(클래스 Class, 책임 Responsibility, 협력 Collaboration) 카드, 그리고 이 카드로 객체로 생각하는 법의 기본과 미묘한 점을 가르친 경험을 설명하겠다.

## 2. 관점 (Perspective)

절차적 설계는 구현 언어나 운영 환경과 상관없이, 추상적인 수준에서 프로세스(processes), 데이터 흐름(data flows), 데이터 저장소(data stores)로 특징지을 수 있다[1]. 우리는 객체 설계에도 이와 비슷한 기본 원리를 세우고 싶었다. 그래서 설계에서 객체의 역할(role)을 규정하는 세 가지 차원(dimensions)으로 정했다. 클래스 이름, 책임, 협력자다.

객체의 클래스 이름은 설계를 논의하기 위한 어휘(vocabulary)를 만든다. 실제로 많은 사람이 객체 설계는 절차적 프로그램 설계보다 언어 설계(language design)와 공통점이 더 많다고 말해 왔다. 우리는 학습자에게 객체를 설명할 딱 맞는 단어들을 찾으라고 권한다(우리 자신도 설계할 때 여기에 상당한 시간을 쓴다). 그 단어들은 서로 일관되면서, 더 큰 설계 환경의 맥락에서 의미를 환기(evocative)해야 한다.

책임은 풀어야 할 문제를 식별한다. 해법은 여러 버전과 개선(refinements)을 거치며 존재할 것이다. 책임은 가능한 해법을 논의하기 위한 손잡이(handle) 역할을 한다. 객체의 책임은 능동 동사(active verb)를 하나씩 담은 짧은 동사구 몇 개로 표현한다. 이 구절들로 더 많은 것을 표현할 수 있을수록 설계는 더 강력하고 간결해진다. 여기서도 딱 맞는 단어를 찾는 것은 설계하는 동안 시간을 들일 가치가 있는 일이다.

객체 설계를 구별 짓는 특징 하나는 어떤 객체도 섬이 아니라는 점이다(no object is an island). 모든 객체는 다른 객체와 관계를 맺고, 서비스와 제어를 그들에게 의존한다. 객체 설계를 특징짓는 마지막 차원은 객체의 협력자다. 책임을 수행하는 과정에서 메시지를 보내거나 받을 객체를 협력자라고 부른다. 협력이 꼭 대칭적인 관계는 아니다. 예를 들어 Smalltalk-80[2]에서 View와 Controller는 거의 대등하게 동작하지만(아래 예시 참고), OrderedCollection은 자기 클라이언트를 거의 신경 쓰지 않고, 심지어 알지도 못한 채 서비스를 제공한다.

이 논문 전체에서 우리는 일부러 클래스와 인스턴스의 구분을 흐린다. 이 비형식성(informality)은 보기만큼 혼란스럽지 않다. 우리 방법이 구체적이어서 인스턴스에 이름을 붙이는 일을 대신하기 때문이다. 이 덕분에 우리의 교수법은 클래스 기반 언어를 쓰든 프로토타입 기반(prototype-based) 언어를 쓰든 상관없이 적용된다.

## 3. CRC 카드 (CRC Cards)

CRC 카드는 두 번째 저자(워드 커닝햄)가 협력적 설계 결정(collaborative design decisions)을 문서화할 필요에 대응하여 고안했다. 카드는 처음에 협력자를 자동으로 색인해 주는 HyperCard[3] 스택(stack)으로 시작했지만, 이식성과 시스템 독립성 문제를 해결하려고 지금의 형태로 옮겨 왔다.

객체의 협력을 문서화한 우리의 이전 작업[4]처럼, CRC 카드는 여러 객체를 동시에 명시적으로 표현한다. 하지만 CRC 카드는 협력의 세부 사항을 메시지 전송의 형태로 추적하기만 하는 것이 아니라, (잠재적으로) 여러 메시지를 영어 문장 한 구절로 표현함으로써 설계자가 협력의 동기(motivation)에 집중하게 한다.

![그림 1](https://c2.com/doc/oopsla89/fig1.gif)

*그림 1. 클래스-책임-협력자(CRC) 인덱스 카드*

| *클래스 이름 (ClassName)* | 협력자 (Collaborators) |
|---|---|
| 책임 (Responsibilities) ... | ... |

지금 우리가 쓰는 방식에서는 객체 하나에 대한 모든 정보를 4×6인치 인덱스 카드 한 장에 적는다. 인덱스 카드는 싸고, 들고 다니기 쉽고, 쉽게 구할 수 있고, 익숙하다는 장점이 있다. 그림 1은 이상적인 카드를 보여 준다. 클래스 이름은 왼쪽 위 모서리에 밑줄을 그어 적고, 그 아래 카드의 왼쪽 3분의 2에 책임을 글머리 목록으로 적고, 오른쪽 3분의 1에 협력자 목록을 적는다.

![그림 2](https://c2.com/doc/oopsla89/fig2.gif)

*그림 2. Smalltalk의 Model, View, Controller의 책임과 협력을 기술한 CRC 카드*

| View | |
|---|---|
| 모델을 그린다 (Render the Model) | Controller |
| 좌표를 변환한다 (Transform coordinates) | Model |

| Controller | |
|---|---|
| 사용자 입력을 해석한다 (Interpret user input) | View |
| 제어를 분배한다 (Distribute control) | Model |

| Model | |
|---|---|
| 문제 관련 정보를 유지한다 (Maintain problem related info) | |
| 변경 알림을 방송한다 (Broadcast change notification) | |

그림 2는 Smalltalk-80 이미지(image)에서 가져온 예시로, 많이 오해받는 모델-뷰-컨트롤러(model-view-controller) 사용자 인터페이스 프레임워크다. 설명을 명확히 하려고 각 객체가 맡은 책임 중 일부만 일부러 보여 주었다. 카드 배치에 주목하라. View와 Controller는 겹쳐 놓았고(긴밀한 협력을 뜻한다) Model 위에 놓았다(감독을 뜻한다). 우리는 이런저런 비형식적인 무리 짓기(groupings)가 설계를 이해하는 데 도움이 된다는 것을 알게 되었다. 예를 들어 부분(parts)은 흔히 전체 아래에 놓는다. 마찬가지로 하나의 추상(abstraction)을 구체화한 것들(refinements)은 모아서 한 더미의 카드로 다룰 수 있고, 가장 추상적인 카드를 맨 위에 두어 나머지를 대표하게 할 수 있다.

인덱스 카드를 재빨리 정리하고 공간적으로 가리킬 수 있다는 점은 설계가 미완성이거나 잘 이해되지 않았을 때 가장 큰 가치를 발휘한다. 우리는 설계자들이 쓰려고 마음먹은 카드를, 완성되면 놓을 자리를 손가락으로 가리키며 거듭 언급하는 모습을 보았다.

카드로 하는 설계는 하향식(top-down)이나 상향식(bottom-up)이 아니라, 아는 것에서 모르는 것으로(from knowns to unknowns) 나아가는 경향이 있다. 우리는 두 팀이 거의 정반대 순서로, 한 팀은 장치 드라이버(device drivers)에서, 다른 팀은 상위 수준 모델에서 시작해서 본질적으로 같은 설계에 도달하는 것을 보았다. 문제가 일정한 능력들의 집합을 요구했고, 두 팀 모두 설계 요구 사항을 충족하는 과정에서 그것을 발견했다.

우리는 실행 시나리오(execution scenarios)의 도움을 받아 설계를 완성 쪽으로 몰아가기를 제안한다. 뻔한 카드 한두 장만 가지고 시작해서 "만약에(what-if)" 놀이를 한다. 상황이 기존 객체 어느 것도 맡지 않은 책임을 요구하면, 그 책임을 기존 객체 하나에 더하거나 그 책임을 다룰 새 객체를 만든다. 이 과정에서 객체 하나가 너무 어수선해지면, 그 카드의 정보를 새 카드로 옮겨 적으면서 객체가 하는 일을 더 간결하고 강력하게 말할 방법을 찾는다. 정보를 더 줄일 수 없는데도 객체가 여전히 너무 복잡하면, 책임 일부를 떠맡을 새 객체를 만든다.

우리는 학습자에게 시나리오를 "실행"하는 동안 자기가 맡은 역할의 카드를 집어 들라고 권한다. 설계자가 양손에 카드를 한 장씩 들고 흔들며, 객체에 강하게 동화되어 그들의 협력을 설명하는 모습은 드물지 않다.

우리는 신화 속 미래의 필요(mythical future needs)를 충족하려고 객체를 만들지 말고, 오직 지금 이 순간의 요구에 따라서만 만들라고 강조한다. 그래야 설계에는 설계자가 직접 경험한 만큼의 정보만 담기고, 때 이른 복잡성(premature complexity)을 피할 수 있다. 여기서 팀 작업이 도움이 된다. 걱정이 있는 설계자는 의심 가는 약점이나 누락을 겨냥한 시나리오를 제안해서 팀원들에게 영향을 줄 수 있기 때문이다.

## 4. 경험 (Experience)

우리가 CRC 카드를 사용한 맥락 하나는 "객체로 생각하기(Thinking with Objects)"라는 3시간짜리 수업이다. 이 수업은 프로그래밍을 해 본 적은 있지만 매일 프로그래밍을 하는 직무는 아닌 컴퓨팅 전문가를 대상으로 한다. 수업은 데이터 흐름 예제(교육과 행정 프로세스가 있는 학교)를 소개하고, 이를 책임과 협력자를 가진 객체(교사 Teacher, 수위 Janitor, 교장 Principal 등)로 다시 표현하는 순서로 진행된다. 그다음 수강생이 둘씩 짝을 지어 한 시간 동안 현금 자동 입출금기(automatic banking machine)의 객체를 설계한다. 이 연습 문제를 고른 이유는 누구나 이 애플리케이션에 익숙하고, 장치를 제어하는 객체, 중앙 은행 데이터베이스와 통신하는 객체, 사용자 인터페이스를 제어하는 객체로 쉽게 나뉘기 때문이다(예시 해답은 부록을 보라). 연습이 끝나면 "클래스(class)", "인스턴스(instance)", "메서드(method)", "메시지(message)"라는 용어를 정의하고, 여러 객체지향 프로그래밍 언어의 역사와 특징을 짧게 논의하며 수업을 마친다.

이 과정에서 백 명 넘는 학생을 가르쳤는데, 모두 도움 없이 연습을 끝냈다. 다만 반마다 대개 한 쌍은 시작할 때 힌트가 몇 개 필요하다. 후속 연구를 하지는 않았지만, 이 수업은 회사에서 가치 있는 자원으로 여겨지고, 개설된 지 거의 1년이 지났는데도 여전히 수강생이 많고 대기자 명단이 길다.

우리는 숙련된 객체 프로그래머에게도 CRC 카드를 써 보라고 요청했다. 우리의 개인적 경험으로는 소프트웨어 공학에서 카드가 할 역할이 있어 보이지만, 아직 완전한 방법론(methodology)이라고 주장할 수는 없다(다른 이들[5][6]은 CRC 방법을 활용할 수 있는 방법론을 더 온전히 발전시켰다). 완성된 카드를 (부분적인) 설계 문서로 고객에게 전달한 사례를 하나 알고 있다. 카드를 만든 팀은 설계에 꽤 만족했지만, 받은 쪽은 맥락에서 떨어진 카드를 이해하지 못했다.

또 다른 실험은 카드를 다루고 논의하면서 만들어지는 맥락이 얼마나 중요한지 보여 준다. 우리는 숙련된 설계자들이 은행 기계와 비슷한 문제를 풀어 가는 모습을 비디오로 녹화했다. 카메라 위치 때문에 카드와 설계자의 손은 보였지만 카드에 적힌 글씨는 보이지 않았다. 그런데도 녹화를 본 사람들은 개발 과정을 따라가는 데 아무 어려움이 없었고, 자기 의견을 말하려고 테이프를 멈춰 달라고 자주 요청했다. 가장 의미심장한 순간은, 어떤 시청자가 설명을 하다가 화면에 정지된 영상 속 흐릿한 카드를 손가락으로 가리켜야 했을 때였다.

마지막으로, 우리는 복잡한 설계를 설명할 때 CRC 카드를 유용하게 써 왔다. 몇 분의 소개만으로도 청중이 카드 기반 발표를 들을 준비가 된다. 카드는 미리 만들어 둘 수도 있고 그 자리에서 쓸 수도 있다. 그 자리에서 쓰면 설계의 복잡성을 천천히 드러낼 수 있는데, 이는 데이브 토머스(Dave Thomas)의 "거짓말 관리(lie management)"와 관련된 과정이다. 카드는 계산(computation)의 이야기를 들려주는 것을 돕는 소품(props)으로 쓰인다. 카드 덕분에 프로그래밍 언어의 문법이나 관용구(idiom)에 기대지 않고도 그 이야기를 들려줄 수 있다.

## 5. 결론 (Conclusion)

우리의 관점을 바탕으로, 우리는 초보자와 숙련된 프로그래머 모두에게 객체에 관해 가치 있는 무언가를 가르치는 학습 경험을 제공한다. CRC 카드는 객체를 접해 본 적 없는 학습자에게 객체다움을 몸으로 이해하게 하고(physical understanding), 특정 언어의 어휘와 세부 사항을 이해할 준비를 시켜 준다. 또한 객체의 메커니즘은 배웠지만 아직 그 가치를 알지 못하는 사람들에게도 객체에 대한 유용하고 설득력 있는 경험을 준다.

라구 라가반(Ragu Raghavan)[7]은 객체로 전환할 때 강한 프로그래머는 더 강해지지만 약한 프로그래머는 뒤처진다고 말했다. 그룹 환경에서 카드를 써 보니, 객체를 깊이 이해하지 못한 약한 프로그래머도 객체 설계에 기여할 수 있었다. 우리는 설계가 훨씬 더 구체적이고 객체 사이의 논리적 관계가 명시적이기 때문에, 설계를 이해하고 평가하고 수정하기가 더 쉬워진다고 추측한다.

우리는 카드를 물리적으로 옮기는 일의 가치에 놀랐다. 학습자가 객체를 집어 들면 그 객체에 더 쉽게 동화되는 것 같고, 나머지 설계를 그 객체의 관점에서 다룰 준비가 된다. 바로 이 물리적 상호작용의 가치 때문에 우리는 카드를 컴퓨터화하는 것을 거부해 왔다.

바로 이 문제, 즉 카드를 더 큰 설계 방법론과, 그리고 특정 언어 환경과 통합하는 문제가 미래에 가장 유망하다고 우리는 생각한다. 물리적 상호작용의 가치를 지켜야 한다는 필요는, 오늘날의 시스템이 과거의 도구 중심(tool-oriented) 환경을 넘어선 만큼이나 오늘날의 것을 훨씬 넘어서는, 새로운 종류의 사용자 인터페이스와 프로그래밍 환경이 필요함을 가리킨다.

## 참고 문헌 (References)

[1] DeMarco, T.: Structured Analysis and System Specification, Yourdon, 1978.

[2] Smalltalk-80 image, Xerox Corp, 1983.

[3] HyperCard manual, Apple Computer Inc.

[4] Cunningham, W. and Beck, K.: "A Diagram for Object-Oriented Programs," in Proceedings of OOPSLA-86, October 1986.

[5] Wirfs-Brock, R. and Wilkerson, B. "Object-Oriented Design: a Responsibility-Driven Approach," submitted to OOPSLA '89.

[6] Reenskaug, T.: "A Methodology for the Design and Description of Complex, Object-Oriented Systems," technical report, Center for Industrial Research, Oslo, Norway, November 1988.

[7] Raghavan, R.: "Panel: Experiences with Reusability," in the Proceedings of OOPSLA '88, October, 1988.

## 부록 (Appendix)

여기서는 4절에서 다룬 은행 기계 문제의 예시 해답을 제시한다.

Account와 Transaction은 은행 업무 모델을 제공한다. Transaction은 돈이 지급되는 동안에는 능동적인 역할을, 그 뒤에는 수동적인 역할을 맡는다는 점에 주목하라.

![그림 3](https://c2.com/doc/oopsla89/fig3.gif)

| Account | |
|---|---|
| 잔액과 거래 내역을 유지한다 (Keeps balance and traffic) | Transaction<br>RemoteDB |

| Transaction | |
|---|---|
| 송금을 검증하고 수행한다 (Validate & perform money transfer) | CardReader<br>Dispenser<br>RemoteDB |
| 감사 정보를 유지한다 (Keep audit info) | Action<br>Account |

Transaction은 장치 드라이버 역할을 하는 여러 객체의 도움을 받아 책임을 수행한다. 예를 들어 Dispenser 객체는 최종적으로 지급 장치를 작동시킨다.

CardReader 객체는 은행 카드의 마그네틱 띠에 담긴 정보를 읽고 해독한다. 흔한 실수는 은행 카드에 저장된 정보를 모두 항목별로 나열하는 것이다. 카드 인코딩 형식은 분명 잘 고민해서 문서화해야 한다. 하지만 객체를 설계하는 목적에서는, 그 지식이 프로그램의 어디에 놓일지만 식별하면 된다.

![그림 4](https://c2.com/doc/oopsla89/fig4.gif)

| CardReader | |
|---|---|
| 마그네틱 띠를 해독한다 (Decodes strip)<br>카드 삽입을 알린다 (Signals insertion) | Event<br>Transaction |

| Dispenser | |
|---|---|
| 현금을 내준다 (Emits cash)<br>성공과 현금 소진을 알린다 (Signals success and empty) | Event<br>Transaction |

| RemoteDataBase | |
|---|---|
| 계좌를 조회한다 (Retrieves Accounts)<br>거래를 기록한다 (Records Transactions)<br>통신 상태를 알린다 (Signals com status) | Event<br>Transaction<br>Account |

RemoteDataBase는 통신 회선을 구동하고 그 회선으로 전송된 데이터를 해석한다. Account 객체를 생성하고 Transaction 객체를 소비한다.

장치 드라이버들은 예외적이거나 비동기적인 사건을 공유 큐에 Event 객체를 추가하는 방식으로 알린다.

![그림 5](https://c2.com/doc/oopsla89/fig5.gif)

| Event | |
|---|---|
| 신호를 큐에 넣는다 (Queues Signals) | Screen<br>CardReader |
| 하드웨어를 사용자 인터페이스와 격리한다 (Isolates H/W from user-interface) | Dispenser<br>RemoteDB |

Event는 Screen들을 차례로 거쳐 가게 하는 Action을 촉발함으로써 사용자 인터페이스를 구동한다. 실제 화면의 형식과 순서는 사용자 인터페이스 설계에 따라 정해질 것이고, 아마 은행마다 다를 것이다. 우리는 상태 기계(state-machine) 같은 인터페이스를 만들 수 있는 객체들을 제시한다.

![그림 6](https://c2.com/doc/oopsla89/fig6.gif)

*인터페이스 FSM: 인사(Hello), 거래 선택(Select Transaction), 출금(Withdrawal), 입금(Deposit), 잠시 기다려 주세요(Please Wait), 다른 거래?(Another?) 상태가 이어진다.*

Screen 객체는 상태(states)에, Action 객체는 전이(transitions)에 대응한다. Screen은 Action을 디스패치(dispatch)하는 방식이 저마다 다를 수 있다. Action 자체는 이벤트를 처리하는 방식이 저마다 다를 것이다. Action은 최종적으로 Transaction을 구성하고, 이후의 은행 기계 작동은 그 Transaction에 위임한다.

![그림 7](https://c2.com/doc/oopsla89/fig7.gif)

| Screen | |
|---|---|
| 안내 문구를 표시한다 (Displays prompts)<br>Event를 Action에 디스패치한다 (Dispatches Events to Actions) | Event<br>Action |

| Action | |
|---|---|
| Screen을 순서대로 진행시킨다 (Sequences Screens)<br>Transaction을 조립한다 (Assembles Transactions) | Transaction<br>Screen |
