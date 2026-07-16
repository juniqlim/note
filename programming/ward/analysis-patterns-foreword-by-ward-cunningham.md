# Analysis Patterns: Reusable Object Models — 추천사 (Foreword)

**저자**: 워드 커닝햄 (Ward Cunningham)
**원서**: Martin Fowler, *Analysis Patterns: Reusable Object Models*
**출처(원문)**: https://c2.com/doc/forewords/fowler.html

---

## 번역

제가 소프트웨어 개발 프로젝트를 볼 때 가장 먼저 찾는 것은 '경험(experience)'입니다. 개발 팀이 관련 업무를 수행한 경험이 있는가? 그 경험을 그들이 만드는 객체(objects)에 적용할 수 있는가? 불행하게도, 이 질문들에 대한 대답은 종종 "아니요"입니다.

객체지향 개발 커뮤니티의 점점 더 많은 사람들이 우리가 한동안 엉뚱한 곳에 집단적인 주의를 기울여왔다고 느끼고 있습니다. 우리는 더 이상 도구, 기법, 표기법, 심지어 코드 자체에 집중할 필요가 없습니다. 훌륭한 프로그램을 만들 수 있는 장치는 이미 우리 손안에 있습니다. 우리가 실패한다면, 그것은 경험이 부족하기 때문입니다.

마틴 파울러(Martin Fowler)는 우리에게 필요한 것, 바로 '책 형태로 된 경험'을 제공할 방법을 찾아냈습니다. 에릭 감마(Erich Gamma)와 그 동료들이 그들의 기념비적인 저서 *Design Patterns: Elements of Reusable Object-Oriented Software*에서 구현 객체(implementation objects)를 위해 했던 일을, 마틴은 도메인 객체(domain objects)를 위해 해냈습니다. 마틴은 우리 초기 커뮤니티의 익숙한 용어를 사용하지만, 그 방식은 사뭇 다릅니다. 예를 들어, 그가 "패턴(pattern)"이라는 단어를 사용하는 것은 감마의 책(또는 시장에 쏟아져 나오는 다른 신간들)을 복제하거나 확장하기 위함이 아닙니다. 그가 글로 옮긴 자신의 경험을 "패턴"이라 부르는 이유는 그것이 말 그대로 패턴이기 때문입니다. 그는 작업 과정에서 반복되는 문제들에 대한 해결책을 거듭 찾아냈고, 그 과정에서 패턴이라는 형식을 발견했습니다.

마틴 파울러는 객체지향 분석(이론)에 관한 책을 아주 쉽게 쓸 수도 있었을 것입니다. 다행히도, 그는 그러지 않았습니다. 대신 우리는 분석의 '결과'를 목록화한 책을 갖게 되었습니다. 각 장은 일반적인 비즈니스 문제에 적용된 그(와 그의 동료들)의 분석적 노력에 대한 결론을 담고 있습니다. 다루어지는 도메인은 의료 기록 관리에서부터 금융 파생상품 거래에 이르기까지 다양하며, 그 사이의 여러 분야들도 포함합니다. 이 중 어떤 장이 여러분에게 해당될까요? 놀랍게도, 모든 장이 그렇습니다. 마틴은 각 문제를 맥락(context) 속에 배치한 다음, 그 맥락에 맞는 해결책을 제안합니다. 여러분은 모든 맥락에서 익숙한 측면들을 보게 될 것입니다. 문제들을 알아볼 수 있을 것이고, 그 결과물의 진가를 알게 될 것입니다. 그리고 그곳에 바로 '경험'이 있습니다.

마지막으로, 마틴은 자신의 생각과 판단을 전달하며 개인적인 문체로 글을 씁니다. 우리는 그의 고객과 동료들에 대한 존중을 느낄 수 있는데, 그는 대부분의 통찰이 그들로부터 나온다고 인정합니다. 우리는 그가 구현의 변덕스러움(vagaries)과는 거리를 두면서도 여전히 구현 가능성(implementability)은 유지하는 모습을 지켜보게 되는데, 이는 말로 직접 설명하기 힘든 아슬아슬한 줄타기와 같습니다. 전문가 분석가의 마음속을 들여다봄으로써, 우리는 분석하는 방법에 대한 교훈을 얻고 우리 자신의 경험 저장소에 이를 더하게 됩니다.

— 워드 커닝햄 (Ward Cunningham)

---

## 원문 (English)

**Foreword to Analysis Patterns: Reusable Object Models**
by Martin Fowler
foreword by Ward Cunningham

When I look at a software development project I look for experience. Does the development team have experience doing relevant work? Can they apply their experience to the objects they build? Unfortunately, the answer to these questions is often "no."

A growing number of us in the object-oriented development community feel we have misplaced our collective attention for some time. We no longer need to focus on tools, techniques, notations or even code. We already have in our hands the machinery to build great programs. When we fail, we fail because we lack experience.

Martin Fowler has found a way to give us what we need: experience in book form. He has done for domain objects what Eric Gamma, et. al. did for implementation objects in their landmark work Design Patterns: Elements of Reusable Object-Oriented Software. Martin uses the familiar terminology of our nascent community, but in a different way. He uses the word "pattern," for example, not because he's duplicating or extending Gamma's book (or any of the other new titles bursting onto the market). He calls his written form of experience "patterns" simply because that is what they are. In his work, he repeatedly found solutions to recurring problems, and discovered the pattern form in the process.

Martin Fowler easily could have written a book on object-oriented analysis. Luckily, he didn't. Instead we have a book cataloging the result of analysis. Each chapter reports the conclusion of his (and his colleagues') analytic efforts applied to common business problems. The domains addressed vary from medical record keeping to financial derivative trading, with several stops in between. Which chapters apply to you? Amazingly, they all do. Martin places each problem in a context, then offers a solution for that context. You will see familiar aspects in every context. You will recognize the problems. You will appreciate the results. And there it is: experience.

Finally, Martin writes in a personal style, relaying his thoughts and judgments. We feel his respect for his clients and colleagues, from whom, he admits, most insights arise. We watch him keep his distance from the vagaries of implementation while still preserving implementability, a tightrope walk that defies direct explanation. As we see into the mind of an expert analyst, we gain a lesson in the how-to of analysis that adds to our own store of experience.
