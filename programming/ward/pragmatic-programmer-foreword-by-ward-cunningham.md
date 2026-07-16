# The Pragmatic Programmer — 서문 (Foreword)

**저자**: 워드 커닝햄 (Ward Cunningham)
**원서**: Andrew Hunt & David Thomas, *The Pragmatic Programmer*
**출처(원문)**: https://c2.com/doc/pragmatic.html

---

## 번역

리뷰어(reviewer)로서 저는 여러분이 들고 있는 이 책을 일찍 읽을 기회를 얻었습니다. 초고(draft) 상태였는데도 훌륭했습니다. 데이브 토머스(Dave Thomas)와 앤디 헌트(Andy Hunt)는 할 말이 있고, 그것을 어떻게 말해야 하는지 압니다. 저는 그들이 무엇을 하고 있는지 보았고, 그것이 통하리라는 것을 알았습니다. 제가 이 서문을 쓰겠다고 자청한 것은 그 이유를 설명하고 싶었기 때문입니다.

간단히 말해, 이 책은 여러분이 따라 할 수 있는 방식으로 프로그래밍하는 법을 알려줍니다. 그게 뭐 어려운 일인가 싶겠지만, 어렵습니다. 왜일까요? 우선, 모든 프로그래밍 책이 프로그래머에 의해 쓰이는 것은 아닙니다. 많은 책이 언어 설계자(language designers)나, 그들의 창작물을 홍보하기 위해 함께 일하는 저널리스트들에 의해 엮입니다. 그런 책들은 프로그래밍 언어로 말하는 법을 알려줍니다. 물론 중요하지만, 그것은 프로그래머가 하는 일의 작은 부분일 뿐입니다.

프로그래밍 언어로 말하는 것 말고 프로그래머는 무엇을 할까요? 글쎄요, 그것은 더 깊은 문제입니다. 대부분의 프로그래머는 자신이 무엇을 하는지 설명하는 데 어려움을 겪을 것입니다. 프로그래밍은 세부사항(details)으로 가득 찬 일이고, 그 세부사항을 놓치지 않으려면 집중이 필요합니다. 몇 시간이 흘러가고 코드가 나타납니다. 고개를 들어보면 그 모든 문장(statements)이 있습니다. 신중하게 생각하지 않으면, 프로그래밍이란 그저 프로그래밍 언어로 문장을 타이핑하는 일이라고 생각할지도 모릅니다. 물론 틀린 생각이지만, 서점의 프로그래밍 코너를 둘러보는 것만으로는 그것을 알아챌 수 없을 것입니다.

『실용주의 프로그래머(The Pragmatic Programmer)』에서 데이브와 앤디는 우리가 따라 할 수 있는 방식으로 프로그래밍하는 법을 알려줍니다. 그들은 어떻게 그렇게 똑똑해졌을까요? 그들도 다른 프로그래머들처럼 세부사항에 몰두하지 않았을까요? 답은, 그들은 일을 하는 동안 자신이 무엇을 하고 있는지에 주의를 기울였고, 그런 다음 그것을 더 잘하려고 노력했다는 것입니다.

여러분이 회의에 앉아 있다고 상상해 보세요. 어쩌면 회의가 끝없이 이어질 것 같고, 차라리 프로그래밍을 하고 싶다고 생각할지도 모릅니다. 데이브와 앤디라면 왜 이 회의를 하고 있는지 생각하고, 회의를 대신할 수 있는 다른 무언가가 있는지 궁금해하고, 그 무언가를 자동화해서 회의가 하던 일이 앞으로는 저절로 일어나게 할 수 있을지 판단할 것입니다. 그리고 실제로 그렇게 할 것입니다.

데이브와 앤디는 그냥 그렇게 생각하는 사람들입니다. 그 회의는 프로그래밍을 방해하는 무언가가 아니었습니다. 그것이 곧 프로그래밍이었습니다. 그리고 개선할 수 있는 프로그래밍이었습니다. 제가 그들이 이렇게 생각한다는 것을 아는 이유는, 그것이 바로 팁 2번이기 때문입니다: "자신의 일에 대해 생각하라(Think About Your Work)."

이 사람들이 몇 년 동안 이런 식으로 생각한다고 상상해 보세요. 머지않아 해결책 모음을 갖게 될 것입니다. 이제 그들이 몇 년 더 그 해결책들을 업무에 사용하면서, 너무 어렵거나 항상 결과를 내지는 못하는 것들을 버린다고 상상해 보세요. 바로 이 접근이 '실용적(pragmatic)'이라는 말을 정의합니다. 이제 그들이 한두 해를 더 들여 그 해결책들을 글로 적는다고 상상해 보세요. 그 정보는 금광일 거라고 생각하겠지요. 맞습니다.

저자들은 자신들이 어떻게 프로그래밍하는지 알려줍니다. 그리고 우리가 따라 할 수 있는 방식으로 알려줍니다. 그런데 이 두 번째 문장에는 생각보다 많은 것이 담겨 있습니다. 설명해 보겠습니다.

저자들은 소프트웨어 개발 이론(theory)을 제안하지 않으려고 조심했습니다. 다행스러운 일입니다. 만약 이론을 제안했다면 각 장을 그 이론을 방어하도록 왜곡해야 했을 테니까요. 그런 왜곡은 이를테면 자연과학의 전통입니다. 자연과학에서 이론은 결국 법칙이 되거나 조용히 폐기됩니다. 반면 프로그래밍에는 법칙이 거의 (어쩌면 전혀) 없습니다. 그래서 법칙이 되고 싶어 하는 것들(wanna-be laws)을 중심으로 짜인 프로그래밍 조언은 글로는 그럴듯해 보여도 실전에서는 만족스럽지 못합니다. 수많은 방법론(methodology) 책들이 잘못되는 지점이 바로 여기입니다.

저는 이 문제를 십여 년간 연구했고, 패턴 랭귀지(pattern language)라는 장치에서 가장 큰 가능성을 발견했습니다. 짧게 말해, 패턴(pattern)은 해결책이고, 패턴 랭귀지는 서로를 강화하는 해결책들의 시스템입니다. 이런 시스템을 찾는 일을 중심으로 하나의 공동체 전체가 형성되었습니다.

이 책은 팁 모음집 그 이상입니다. 양의 탈을 쓴 패턴 랭귀지입니다. 제가 그렇게 말하는 이유는, 각 팁이 경험에서 나왔고, 구체적인 조언으로 이야기되며, 서로 연결되어 하나의 시스템을 이루기 때문입니다. 이것들이 바로 우리가 패턴 랭귀지를 배우고 따를 수 있게 해주는 특성입니다. 이 책에서도 똑같이 작동합니다.

이 책의 조언은 구체적이기 때문에 따라 할 수 있습니다. 모호한 추상론은 찾아볼 수 없습니다. 데이브와 앤디는 마치 각 팁이 여러분의 프로그래밍 경력에 활력을 불어넣는 필수 전략인 것처럼 여러분을 향해 직접 씁니다. 단순하게 만들고, 이야기를 들려주고, 가볍게 다가가고, 그런 다음 여러분이 시도할 때 떠오를 질문들에 대한 답으로 마무리합니다.

그리고 더 있습니다. 팁을 열 개나 열다섯 개쯤 읽고 나면 이 작업의 또 다른 차원이 보이기 시작할 것입니다. 우리는 그것을 때때로 QWAN, 즉 '이름 없는 품질(the quality without a name)'이라고 부릅니다. 이 책에는 여러분의 의식 속으로 스며들어 여러분 자신의 철학과 섞일 철학이 있습니다. 설교하지 않습니다. 그저 무엇이 통하는지 말할 뿐입니다. 하지만 그 말하기 속에서 더 많은 것이 전해집니다. 그것이 이 책의 아름다움입니다. 이 책은 자신의 철학을 몸소 구현하며, 그것도 잘난 체하지 않으면서 해냅니다.

자, 여기 있습니다. 읽기 쉽고 쓰기(활용하기) 쉬운, 프로그래밍이라는 실천 전체에 관한 책입니다. 왜 통하는지에 대해 길게 이야기했습니다만, 여러분은 아마 통한다는 사실에만 관심이 있겠지요. 통합니다. 곧 알게 될 것입니다.

— 워드 커닝햄 (Ward Cunningham)

---

## 원문 (English)

**The Pragmatic Programmer**
By Andrew Hunt and David Thomas
Foreword by Ward Cunningham

As a reviewer I got an early opportunity to read the book you are holding. It was great, even in draft form. Dave Thomas and Andy Hunt have something to say, and they know how to say it. I saw what they were doing and I knew it would work. I asked to write this foreword so that I could explain why.

Simply put, this book tells you how to program in a way that you can follow. You wouldn't think that that would be a hard thing to do, but it is. Why? For one thing, not all programming books are written by programmers. Many are compiled by language designers, or the journalists who work with them to promote their creations. Those books tell you how to talk in a programming language—which is certainly important, but that is only a small part of what a programmer does.

What does a programmer do besides talk in programming language? Well, that is a deeper issue. Most programmers would have trouble explaining what they do. Programming is a job filled with details, and keeping track of those details requires focus. Hours drift by and the code appears. You look up and there are all of those statements. If you don't think carefully, you might think that programming is just typing statements in a programming language. You would be wrong, of course, but you wouldn't be able to tell by looking around the programming section of the bookstore.

In The Pragmatic Programmer Dave and Andy tell us how to program in a way that we can follow. How did they get so smart? Aren't they just as focused on details as other programmers? The answer is that they paid attention to what they were doing while they were doing it—and then they tried to do it better.

Imagine that you are sitting in a meeting. Maybe you are thinking that the meeting could go on forever and that you would rather be programming. Dave and Andy would be thinking about why they were having the meeting, and wondering if there is something else they could do that would take the place of the meeting, and deciding if that something could be automated so that the work of the meeting just happens in the future. Then they would do it.

That is just the way Dave and Andy think. That meeting wasn't something keeping them from programming. It was programming. And it was programming that could be improved. I know they think this way because it is tip number two: Think About Your Work.

So imagine that these guys are thinking this way for a few years. Pretty soon they would have a collection of solutions. Now imagine them using their solutions in their work for a few more years, and discarding the ones that are too hard or don't always produce results. Well, that approach just about defines pragmatic. Now imagine them taking a year or two more to write their solutions down. You might think, That information would be a gold mine. And you would be right.

The authors tell us how they program. And they tell us in a way that we can follow. But there is more to this second statement than you might think. Let me explain.

The authors have been careful to avoid proposing a theory of software development. This is fortunate, because if they had they would be obliged to warp each chapter to defend their theory. Such warping is the tradition in, say, the physical sciences, where theories eventually become laws or are quietly discarded. Programming on the other hand has few (if any) laws. So programming advice shaped around wanna-be laws may sound good in writing, but it fails to satisfy in practice. This is what goes wrong with so many methodology books.

I've studied this problem for a dozen years and found the most promise in a device called a pattern language. In short, a pattern is a solution, and a pattern language is a system of solutions that reinforce each other. A whole community has formed around the search for these systems.

This book is more than a collection of tips. It is a pattern language in sheep's clothing. I say that because each tip is drawn from experience, told as concrete advice, and related to others to form a system. These are the characteristics that allow us to learn and follow a pattern language. They work the same way here.

You can follow the advice in this book because it is concrete. You won't find vague abstractions. Dave and Andy write directly for you, as if each tip was a vital strategy for energizing your programming career. They make it simple, they tell a story, they use a light touch, and then they follow that up with answers to questions that will come up when you try.

And there is more. After you read ten or fifteen tips you will begin to see an extra dimension to the work. We sometimes call it QWAN, short for the quality without a name. The book has a philosophy that will ooze into your consciousness and mix with your own. It doesn't preach. It just tells what works. But in the telling more comes through. That's the beauty of the book: It embodies its philosophy, and it does so unpretentiously.

So here it is: an easy to read—and use—book about the whole practice of programming. I've gone on and on about why it works. You probably only care that it does work. It does. You will see.
