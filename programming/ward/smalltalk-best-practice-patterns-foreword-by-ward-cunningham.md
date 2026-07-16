# Smalltalk Best Practice Patterns — 서문 (Foreword)

**저자**: 워드 커닝햄 (Ward Cunningham)
**원서**: Kent Beck, *Smalltalk Best Practice Patterns, Volume 1: Coding*
**출처(원문)**: https://c2.com/doc/forewords/beck.html

---

## 번역

아, 코딩(Coding).

코딩은 이해의 궁극적 시험(the ultimate test of your understanding)입니다. 코딩은 여러분이 무엇을 알고 무엇을 모르는지 알려줄 것입니다. 코딩은 발견(discovery)과 발명(invention)과 의사결정(decision making)의 과정에 정점을 찍습니다. 코드가 제자리에 딱 들어맞을 때의 그 기쁨이란.

스몰토크(Smalltalk)는 이해를 추구하는 사람에게 보상을 줍니다. 순수한 객체들이 이루는 급진적 모듈성(radical modularity)은 복잡한 아이디어를 표현하고 시험하기에 완벽한 매체입니다. 물론 시험에는 실패의 가능성이 따릅니다. 어쩌면 여러분은 생각만큼 잘 이해하지 못하고 있을지도 모릅니다. 그러면 어떻게 할까요? 그러면 코드를 읽고, 코드에 대해 추론하고, 코드가 말하는 바를 곱씹어 봅니다. 귀 기울이기만 한다면, 코드는 무엇이 빠졌는지 알려줄 것입니다.

켄트(이 책의 저자)와 저는 80년대 초반에 우리가 상상할 수 있는 가장 어려운 문제들과 씨름하며 여러 달을 보냈습니다. 우리는 분석, 설계, 코딩이라는 모든 개발 단계를 함께 했습니다. 우리는 잠재력이 가득하다고 여긴 기계 앞에서 함께 문제를 풀었습니다. 우리는 스몰토크로 문제를 풀었습니다.

켄트와 저는 스몰토크가 우리를 따라올 수 있다는 것을 알게 되었습니다. 무언가를 발견하면 스몰토크에 넣었습니다. 무언가를 결정하면 그것이 우리의 스몰토크에 드러나도록 했습니다. 우리는 이해의 사다리(a ladder of understanding)를 오르고 있었습니다. 우리의 코드는 우리보다 겨우 한두 단(rung) 뒤에 있었습니다. 우리는 그 간격을 유지했습니다. 때로는 코드가 한 단 앞서기도 했습니다.

이 책은 코드 조각에게 말을 거는 법을 알려줍니다. 이 책의 패턴들은 여러분이 스몰토크 기계와 대화할 때 사용할 단어와 구절입니다. 이 패턴들을 사용해 여러분은 여러분의 의미, 생각, 이해를 표현하게 될 것입니다. 이 패턴들로 코딩할 때 스몰토크 기계가 여러분의 손가락을 지켜보고 있을 것입니다. 여러분이 명료하지 않을 때 경고해 줄 것입니다.

네, 코딩할 때 정말로 그런 느낌이 듭니다. 물론 개발의 사회적 맥락(social context)에서는 기계에 실제로 지시를 내리는 것 이상의 일들이 벌어집니다. 기계는 사실 여러분의 사고, 그리고 여러분 주변 사람들의 사고, 그리고 여러분이 사용하기로 한 코드에 자기 생각을 표현하는 시간을 들였던 앞선 사람들의 사고를 비추는 반사경(reflector)일 뿐입니다. 패턴이 작동하는 것은 사람들이 그것을 보고 사용하기 때문입니다. 패턴이 코드를 다루고 있지만, 이 책은 사람에 관한 책입니다.

이 책의 패턴들을 공부하세요. 패턴이 말하는 바와 그것이 작동하는 이유를 이해하세요. 여러분의 것으로 만드세요. 그런 다음 여러분의 가장 좋은 아이디어를 코드까지 밀어붙이세요(drive them through to code). 그 코드가 자라고 번성하는 것을 지켜보세요. 코드에서 배우고, 더 많은 아이디어를 얻고, 그 아이디어들도 코드까지 밀어붙이세요.

켄트와 저는 열다섯 달 동안 열다섯 개의 프레임워크를 만들었습니다. 각 작업은 앞선 작업들을 발판으로 삼았습니다. 전부 유용했습니다. 전부 사용되었습니다. 저는 15년 전에 얻은 그 경험을 지금도 계속 꺼내 씁니다. 그 경험의 가치가 지속되는 것은 우리가 우리의 생각을 코드까지 밀어붙였기 때문입니다. 우리는 아이디어를 실재하게 만들었고, 시험했고, 작동함을 보였습니다. 우리는 그때도 이 패턴들을 반사적으로(reflexively) 코딩에 사용했고 지금도 그렇습니다. 이것들이 스몰토크를 아이디어 기계(idea machine)로 바꾸는 패턴들입니다.

— 워드 커닝햄 (Ward Cunningham)

### 덧붙임: 켄트 벡의 이메일

원문 페이지 말미에 붙어 있는 이메일이다.

> 날짜: 1996년 8월 29일 14:36:56 EDT
> 보낸 사람: 켄트 벡 (Kent Beck)
> 받는 사람: 워드 커닝햄 (Ward Cunningham)
>
> 제작 과정의 실수(production screwup) 때문에 당신의 서문이 책의 첫 인쇄본에 실리지 못하게 됐습니다. OOPSLA에 책을 내놓는 것과 첫 인쇄본에 당신의 서문을 싣는 것 중 하나를 선택해야 했고, 저는 OOPSLA에 책을 내놓는 쪽을 택했습니다. 사과드립니다. 서문을 제때 보내주느라 특별히 애써주신 것을 생각하면 더욱 그렇습니다.

---

## 원문 (English)

**Foreword to Smalltalk Best Practice Patterns, Volume 1: Coding**
by Kent Beck
foreword by Ward Cunningham

Ahh Coding.

Coding is the ultimate test of your understanding. Coding will tell you what you know and what you do not. Coding caps a process of discovery, of invention, of decision making. Oh, what pleasure when code falls into place.

Smalltalk rewards those who seek understanding. The radical modularity of its pure objects makes a perfect medium for expressing complex ideas, and for testing them. Of course with tests come the possibility of failure. Perhaps you do not understand as well as you thought. Then what? Well, then you read the code and reason about it and reflect on what it says. The code will tell you what is missing if only you listen.

Kent (your author) and I spent many months in the early Eighties tackling the toughest problems we could imagine. We worked all development phases together: analysis, design and coding. We worked the problems together at a machine, a machine we recognized to be full of potential. We worked our problems in Smalltalk.

Kent and I found Smalltalk could keep up with us. As we discovered something, we put it into Smalltalk. When we decided something, we made sure it showed in our Smalltalk. We were climbing a ladder of understanding. Our code was only a rung or two behind us. We kept it that way. Sometimes it was a rung ahead.

This book tells how to talk to a piece of code. The patterns in this book are the words and phrases you will use in conversation with the Smalltalk machine. Using these patterns you will express your meaning, your thinking, your understanding. As you code with these patterns you will have the Smalltalk machine watching over your fingers. It will warn you when you are unclear.

Yes, it really feels like that when coding. Of course there is more going on in the social context of development than the actual instructing of the machine. The machine is really just a reflector for your thinking, and that of the people around you, and the people before you who took the time to express their thoughts in the code you choose to use. The patterns work because people see and use them. This book is about people even though the patters address code.

Study the patterns in this book. Understand what they say and why they work. Make them yours. Then take your best ideas and drive them through to code. Watch that code grow and flourish. Learn from it, have more ideas, then drive those ideas through to code too.

Kent and I produced fifteen frameworks in as many months. Each work played off the ones before it. They were all useful. They were all used. I continue to draw on the experience gained fifteen years ago. The value of the experience lasts because we drove our thoughts through to code. We made our ideas real, tested and showed to work. We used these patterns reflexively in our coding then and still do now. These are the patterns that turn Smalltalk into an idea machine.

> Date: 29 Aug 96 14:36:56 EDT
> From: Kent Beck
> To: Ward Cunningham
>
> Because of a production screwup, your foreword will not appear in the first printing of the book. I had to choose between having the book at OOPSLA and having your foreword in the first printing and I went with having the book at OOPSLA. I apologize, especially in light of your extra effort in getting it to me.
