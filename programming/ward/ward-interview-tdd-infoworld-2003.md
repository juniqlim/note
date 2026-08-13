https://www.infoworld.com/article/2235746/interview-xp-pioneer-stumps-for-test-driven-development.html
인터뷰: XP 개척자가 테스트 주도 개발을 옹호하다 (Interview: XP pioneer stumps for test-driven development)
글: 존 유델 (Jon Udell, InfoWorld 테스트 센터 수석 분석가) 2003년 8월 1일

# 테스트 우선 접근법에 내재된 긍정적 강화

부제: 워드 커닝햄이 프로그래밍에 대한 테스트 우선(test-first) 접근법에 내재된 긍정적 강화(positive reinforcement)를 설명한다.

익스트림 프로그래밍(Extreme Programming)과 테스트 주도 개발(test-driven development)의 개척자인 워드 커닝햄은 웹 기반 협업 도구인 위키(Wiki)의 발명가이기도 합니다. InfoWorld 테스트 센터 수석 분석가 존 유델이 그에게 TDD 실천가로서 배운 교훈을 되돌아봐 달라고, 그리고 FIT(Framework for Integrated Test, 통합 테스트 프레임워크)이 어떻게 프로그래머와 비즈니스 분석가가 업무 시나리오 테스트에서 협업할 수 있게 하는지 설명해 달라고 청했습니다.

---

## 테스트 우선의 동기

**InfoWorld:** 테스트 우선(test first)의 원동력이 되는 동기는 무엇입니까?

**커닝햄:** 마지막 버그 하나를 찾아내는 것이라기보다는, **세부 사항(details)에 많은 주의를 기울이지 않아도 되는 방식으로 개발을 이끌어 가는 것**입니다. 그렇게 되면 전략적으로 생각하고 행동할 수 있습니다. 최고의 개발자들은 이제 테스팅에 매우 관심이 많지만, 그들이 원하는 것은 자신에게 즉각적으로 이득이 되는 테스팅입니다.

## 무엇이 테스트 우선을 가능하게 했는가

**InfoWorld:** 무엇이 테스트 우선을 실현 가능하게(feasible) 만듭니까?

**커닝햄:** 우리는 테스트 작성이 쉽다고 전제하지만, 언제나 그랬던 것은 아닙니다. 코볼(Cobol)에서는 프로그램 한복판으로 손을 뻗을 방법이 없었습니다. 이제는 여러분의 프로그램이 객체들의 네트워크(a network of objects)일 가능성이 훨씬 높습니다. 손을 뻗어 그중 아무거나 붙잡을 수 있습니다.

## 테스트 우선의 사회적 함의

**InfoWorld:** 테스트 우선의 사회적 함의(social implications)는 무엇입니까?

**커닝햄:** 개발자들은 테스트를 다른 개발자와 소통하는 데 사용합니다. 사회적 계약(social contract)은 이렇게 말합니다. **"여기 내 코드가 있다. 내 테스트를 가지고 있고 그것을 돌리기만 한다면, 이 코드로 무엇을 하든 좋다. 그 테스트들을 계속 통과시키는 한 여러분이 나를 다치게 할 일은 없을 것이다. 만약 테스트를 실패시켰다면, 나에게 와서 이야기하라."**

## 순서를 정하는 일

**InfoWorld:** 어떤 이들은 테스트 우선이 지속 가능한 이유가 프로그래머들이 좋아하는 일, 즉 문서가 아니라 코드를 쓰게 해주기 때문이라고 말합니다.

**커닝햄:** 어느 정도 사실일 수 있습니다. 하지만 코드를 쓸 때 여러분은 **하나의** 목표에 집중하고 있습니다. 반면 테스트를 쓸 때 여러분은 **"내가 가지고 있다고 아는 모든 목표 중에서, 다음에 어떤 목표에 집중할 것인가?"를 결정하는 것**입니다. 이것은 **순서를 정하는 일(a sequencing thing)**입니다. 작은 걸음을 뗄 것인가, 큰 걸음을 뗄 것인가? 그리고 그 걸음을 어떻게 확인할 것인가?

## 초록 막대의 긍정적 강화

**InfoWorld:** 사람들은 끊임없는 긍정적 강화 — 테스트가 통과했음을 뜻하는 초록 막대(green bar) — 가 강력한 동기 부여 요인이라고 이야기합니다.

**커닝햄:** 사실입니다. 한 걸음 내딛습니다. 작아 보이지만 그 강화를 받습니다 — 끝났다는 것 말이죠. **우리가 지난 수년간 몇 주, 몇 달씩 코딩을 해오면서 얼마나 적은 강화만을 받아왔는지 놀라울 정도입니다. 거의 절망(despair) 속으로 빠져들 수도 있습니다.**

## FIT — 아직 존재하지 않는 프로그램에 대해 대화하기

**InfoWorld:** FIT은 어디에 들어옵니까?

**커닝햄:** **아직 존재하지도 않는 프로그램에 대해 어떻게 풍부한 대화를 나눌 수 있을까요?** 요즘 우리는 UI에 초점을 맞추지만, 복잡한 업무 시나리오 — 예컨대 보험 계약에서 순서가 어긋난 배서(an out-of-sequence endorsement on an insurance contract) 같은 것 — 는 화면에 나타나지 않습니다. 다행히도 그런 문제를 고민하는 사람들은 이런 사례들을 스프레드시트에서 풀어보는 경향이 있습니다. FIT을 사용하면 그 스프레드시트를, 소프트웨어 테스트가 읽고 갱신하는 웹 페이지로 바꿀 수 있습니다.

**InfoWorld:** 그러면 프로그래머와 비즈니스 분석가가 말 그대로 같은 페이지 위에 있게 되는 것이군요?

**커닝햄:** 그렇습니다. 사람과 사람 사이의 의사소통은 여전히 무엇이 요구되는지에 대한 가장 풍부한 통찰의 원천입니다. 하지만 어느 시점에는 그것을 적어두고 싶어집니다. 이렇게 말하고 싶어지는 것이죠. **"여기 도메인 전문가인 내 언어로 된 사례들이 있다. 당신이 일을 하면서 이것들을 기계적으로 확인해 달라. 그래야 당신의 이해관계가 보호되는 것과 같은 방식으로 내 이해관계도 보호된다."**

---

## 원문 핵심 인용

> "Not so much finding that last bug, but guiding the development in a way that doesn't require a lot of attention to details. Then you can think and act strategically."

> "With Cobol, there was no way to reach into the middle of your program. Now it's much more likely that your program is a network of objects. You can reach in and grab any one of them."

> "Developers use tests to communicate with other developers. The social contract says, 'Here's my code, do anything you want with it so long as you have and run my tests. You're unlikely to hurt me if you continue to pass those tests. If you do fail a test, come talk to me.'"

> "When you're writing code, you're focused on a single goal. When you're writing a test, you're deciding, 'Of all the goals I know I have, what goal will I focus on next?' It's a sequencing thing. Do I take a little step or a big one? And how am I going to check that step?"

> "You take a step, it seems small, but you get that reinforcement — it's done. It's amazing how little reinforcement we've gotten over the years as we've gone through weeks and months of coding; you can get almost into despair."

> "How do you have a rich conversation about a program that doesn't yet exist?"

> "Here are some examples in my language as a domain expert, please check them mechanically, as you do your work, so that my interests are protected in the same way yours are."

---

## 메모

- 워드가 TDD를 정면으로 답한 드문 자료. `ward-interview-extreme.md`에서는 인터뷰어가 TDD를 화두로 던졌을 때 기법이 아니라 "내일 일은 내일" 이라는 태도로 답했다.
- 널리 워드의 말로 인용되는 "Test-first coding is not a testing technique"는 **출처가 확인되지 않는다.** c2 위키 [TestFirstDesign](https://wiki.c2.com/?TestFirstDesign)에서 한 기여자가 "내 기억이 맞다면 WardCunningham이 어딘가에서 그런 말을 했다"고 적은 것이 근원으로 보인다. 다만 이 인터뷰의 "순서를 정하는 일" 답변이 정확히 같은 취지다.
- FIT 관련 워드 본인의 글: c2 위키 [FrameworkForIntegratedTest](https://wiki.c2.com/?FrameworkForIntegratedTest). 테스트 개발이 **명세와 통합**되고(마틴 파울러가 SpecificationByExample이라 이름 붙인 것), 테스트 실행이 **개발자가 프로그래밍하며 쓰는 바로 그 인터페이스**와 통합된다는 두 층위의 통합.
