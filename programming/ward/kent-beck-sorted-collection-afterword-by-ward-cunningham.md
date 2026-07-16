# Kent Beck: Sorted Collection — 후기 (Afterword)

**저자**: 워드 커닝햄 (Ward Cunningham), 1997
**출처(원문)**: https://c2.com/doc/forewords/beck2.html

---

## 번역

프로그램이 의도(intent)를 표현한다면, 그 의도에 생명을 불어넣는 것은 컴퓨터, 즉 하드웨어다. 프로그램이 표현하는 바를 온전히 통제하려면, 그것을 실행하는 컴퓨터를 통제해야 한다.

그러므로:

**플러그가 달린 컴퓨터를 위해 프로그램을 작성하라. 컴퓨터의 동작이 불만족스럽다면, 플러그를 뽑아라.**

지금 저는 기억에 의존해 쓰고 있습니다. 컴퓨터의 플러그를 뽑을 수 있다는 이 아이디어는 컴퓨터가 존재해 온 시간만큼이나 오랫동안 우리 문화 안팎을 드나든 아이디어입니다. 저는 이 아이디어를 패턴(pattern), 즉 문제와 그 해결책으로 표현했습니다. 제가 이 패턴을 떠올리는 것은 켄트와 함께한 프로그래밍이 생각나기 때문입니다.

이 패턴의 문구는 아직 딱 맞지 않습니다. 마치 제가 컴퓨터의 폭주를 두려워하는 듯한 인상을 주니까요. 미국 국방 컴퓨터가 소련 국방 컴퓨터와 이야기를 나누다가 자기들이 인간보다 세상을 더 잘 운영할 수 있겠다는 생각을 하게 되는 옛날 영화 「포빈 프로젝트(The Forbin Project)」를 기억하는 분 있나요? 그런 게 문제가 아닙니다.

제가 처음 "플러그를 뽑을 수 없는 컴퓨터는 프로그래밍하지 마라" 패턴을 쓴 것은 켄트와 제게 큰 규모(large scale)의 패턴이 필요했기 때문입니다. 우리는 새로운 종류의 개발자를 위한 큰 조언을 찾고 있었습니다. 우리는 평범한 사람들이 자신의 컴퓨팅 요구를 스스로 해결하는 모습을 상상했습니다. 이 사람들은 강력한 언어로 자신을 표현할 것입니다. 하지만 그 언어를 사용하는 데 대한 명확한 조언도 필요할 것입니다. "플러그 뽑기(unplug)" 패턴은 말합니다. 프로그램을 쓰기 시작하기 전에, 당신 자신의 목적을 위해 통제할 수 있는 컴퓨터를 구하라. 유리 방 안의 컴퓨터에 만족하지 마라. 시간을 빌려 쓰지 마라. 당신 자신의 컴퓨터를 가져라. 그것을 당신의 것으로 만들어라.

이 패턴에는 많은 역사가 있습니다. 켄트와 저는 컴퓨팅에 대한 비전을 공유했습니다. 우리는 샌드박스(sandbox) 방식으로 연구하는 연구소에서 일했습니다. 모든 연구자에게 10년 뒤에나 보편화될 컴퓨터를 주고 무슨 일이 일어나는지 지켜보는 식이죠. 우리는 책상마다 거대한 화면과 그래픽 가속기를 갖춘 듀얼 프로세서 워크스테이션을 두고 있었습니다. 그래서 무슨 일이 일어났을까요? 별로 없었습니다. 무슨 이유에선지 대부분의 사람들은 프로그램을 작성하려면 허가가 필요하다고 생각했습니다. 우리는 아니었습니다. 우리는 그 기계들을 우리 것으로 만들었습니다.

우리는 1년 반 동안 함께 프로그램을 썼습니다. 월요일에 커피를 마시며 문제를 만들어내고, 화요일에는 버둥거리는 프로토타입이 나오고, 금요일에는 결과를 보여주려고 사람들을 사무실로 끌고 왔습니다. 네, 그런 식이었습니다. 아닐 때만 빼면요. 가끔은 막혔습니다. 화요일쯤 되면 감당이 안 되고 아이디어도 바닥났습니다. 아무 데도 가지 못하는 프로그램만 남았죠. 그래서 우리는 플러그를 뽑았습니다.

켄트와 저는 미완성 프로그램에서 걸어 나올 수 있었습니다. 그럴 수 있었던 것은 우리가 그 프로그램들을 우리 자신을 위해 쓰고 있었기 때문입니다. 프로그램이 더 이상 돌려주는 게 없으면 우리에게도 더 이상 쓸모가 없었습니다. 달리 말하면, 우리는 창작 행위 그 자체(the mere act of authoring)가 우리에게 보상이 되기를 기대했고, 실제로 자주 그랬습니다.

그러다 우리는 패턴을 만났습니다. 우리 둘 다 책장에 크리스토퍼 알렉산더(Christopher Alexander)의 책이 있었습니다. 우리는 개발에 대한 우리의 가벼운(flip) 태도가 통하고 있다는 것을, 즉 사용되고 심지어 재사용되는 프로그램을 만들어내고 있다는 것을 알아차렸습니다. 알렉산더 덕분에 우리는 우리가 하고 있는 일을 담아내서(can) 나눌 수도 있겠다는 생각을 하게 되었습니다.

저는 알렉산더가 점진적 성장(piecemeal growth)을 강조했던 것을 기억합니다. 그것은 그의 모든 작업의 근본이었고 우리 작업의 근본이기도 했습니다. 하지만 알렉산더의 비전은 한 가지 중요한 점에서 우리의 비전을 넘어섰습니다. 그는 하나의 작업에 작용하는 힘들(forces)의 어마어마한 범위를 인식했습니다. 그는 집을 지으려면 도시를 만드는 법과 벽돌을 만드는 법도 알아야 한다는 것을 알았습니다. 그리고 그 노하우를 위에서 아래까지 연결하는 법을 우리에게 보여주었습니다. 경이로웠죠.

그렇게 해서 제가 컴퓨터 플러그 이야기를 하게 된 것입니다. 우리는 알렉산더에게서 조언은 구체적이어야 한다는 것을 배웠습니다. "프로그램을 친절하게 만들어라" 같은 조언에서 무언가를 배운 사람이 있던가요? 우리는 마침 "각 창(pane)마다 동사가 담긴 팝업 메뉴를 하나씩 두어라" 같은 더 구체적인 조언으로 더 나은 결과를 얻은 참이었습니다.

"플러그 뽑기" 패턴은 사실 플러그에 관한 것이 전혀 아니었습니다. 소유권과 통제(ownership and control)에 관한 것이었습니다. 프로그램을 작성하는 환경을 통제하라는 말이었습니다. 플러그의 요점은 그저 시험(test)이었습니다. 당신이 하는 일을 지나치게 제약하지 않으면서 올바른 방향으로 이끌어 줄 구체적인 무언가 말입니다.

좋은 패턴이지만 완전하지는 않습니다. 이 패턴은 실제로 필요한 소유권과 통제를 제공해 주는 다른 패턴들에 둘러싸여 있을 때에만 제대로 작동합니다. 켄트와 저는 그런 환경에 우연히 굴러들어갔습니다. 우리가 스스로 만든 것이 아닙니다. 하지만 우리는 우리가 그것을 가지고 있음을 알아보았고, 사용했습니다.

이 패턴은 오늘날에도 결코 낡지 않았습니다. 여러분은 아마 모든 소프트웨어의 99.9퍼센트가 플러그를 뽑을 수 있는 컴퓨터에서 작성된다고 생각할 것입니다. 하지만 정말 뽑을 수 있습니까? 10년 전 이 패턴을 처음 정식화했을 때 저는 워크스테이션을 생각하고 있었습니다. 우리는 워크스테이션이 권력의 중심(locus of power)이 될 거라고 생각했습니다. 하지만 지금 권력을 쥔 것은 서버로 드러났습니다. 여러분의 서버는 플러그를 뽑을 수 있습니까? 전화 연결이라도 됩니까?

저는 특별히 깨어 있는 프로바이더의 도움으로 구축한 인터넷 거점(presence)을 유지하고 있습니다. 제 구내에는 제가 소유한 플러그가 달린 서버가 있습니다. 연결 대역폭은 소박하지만 끊기지 않습니다. 저는 이 구성 전체의 성격이 더 단순한 방식들보다 범주적으로(categorically) 낫다는 것을 알게 되었습니다. 제 기계에서 저는 다른 곳에서는 환영받지 못하는 프로그램들을 돌립니다. 스스로 연결을 여는 프로그램, 멈추지 않고 계속 도는 프로그램 같은 것들요. 저는 허가를 구할 필요가 없습니다.

컴퓨터·통신 산업의 거대 기업들에게 우리는 그저 소비자일 뿐입니다. 그들은 물론 우리에게 팔고 싶어 하지만, 우리에게 필요한 모든 것을 팔지는 않을 것입니다. 즉, 우리가 고집하지 않는 한 우리를 강력하게 만들어주지 않을 것입니다. 이 패턴에 주의를 기울이세요. 우리 컴퓨터 사용자들이 켄트와 제가 누려온 종류의 소유권을 갖고 지키려면, 그 플러그들을 잘 지켜봐야 할 것입니다.

— © 1997, 워드 커닝햄 (Ward Cunningham)

---

## 원문 (English)

**Kent Beck: Sorted Collection**
Afterword by Ward Cunningham

While a program expresses intent, it is the computer, the hardware, that brings that intent to life. In order to have full control over your program's expression you must control the computer that runs it.

Therefore:

Write your program for a computer with a plug. Should you be dissatisfied with the behavior of the computer, unplug it.

I'm working from memory here. This idea, the idea that you could unplug a computer, is an idea that has run in and out of our culture for about as long as there have been computers. I've expressed the idea as a pattern, a problem and its solution. I'm thinking about this pattern because it reminds me of programming with Kent.

I haven't got the words to this pattern quite right. It gives the impression that I fear computers run amuck. Does anybody remember that old film, the Forbin Project, where the US defense computer gets to talking to the Soviet defense computer and they get the idea that they can run the world better than us? Well, that's not the problem.

I first wrote the "don't program a computer you can't unplug" pattern because Kent and I needed a pattern at a large scale. We were looking for big advice for a new kind of developer. We imagined ordinary people taking their computing needs into their own hands. These people would use powerful languages to express themselves. But they would also need clear advice about using them. The "unplug" pattern says, before you start writing a program, get a computer that you can control for your own purposes. It says: Don't settle for a computer in a glass room. Don't borrow time. Get your own computer. Make it yours.

There is a lot of history to this pattern. Kent and I shared a vision of computing. We worked in a lab that used the sandbox approach to research. You know, give all the researchers the kind of computer that will be the norm in a decade and see what happens. We had dual-processor workstations with huge screens and graphics accelerators on every desk. And what happened? Not too much. For some reason most people thought they needed permission to write programs. Not us. We made those machines our own.

We wrote programs together for a year and a half. We'd make up a problem over coffee on Monday, have a prototype struggling by Tuesday, and be dragging people into the office to see results by Friday. Yes, it was like that, except when it wasn't. Sometimes we'd get stuck. By Tuesday we would be over our heads and out of ideas. We had a program going nowhere. So we pulled the plug.

Kent and I could walk away from an undone program. We could because we were writing those programs for ourselves. We had no further use for them when they stopped giving back. Put another way, we expected the mere act of authoring to reward us, as it often did.

Then we found patterns. We both had Christopher Alexander on our bookshelves. We had noticed that our flip attitude about development was working, producing programs that were used, even reused. Alexander got us thinking that we could can what we were doing and share it too.

I remember Alexander's emphasis on piecemeal growth. It was fundamental to all of his work and to ours as well. Alexander's vision went beyond our vision, though, in one important way. He recognized the incredible range of forces that bear on one's work. He knew that to make a house one must also know how to make a city, and a brick. Then he showed us how to link that know-how together, top to bottom. Awesome.

So that is how I came to be talking about computer plugs. We learned from Alexander that our advice had to be concrete. Who ever learned anything from advice like: make your programs friendly? We had recently had better luck with more concrete advice like: have one pop-up menu, containing verbs, for each pane...

The "unplug" pattern wasn't about plugs at all. It was about ownership and control. It said take control of the environment in which you write programs. The point of plugs was just the test, something concrete, that would lead you in the right direction without overly constraining what you do.

It's a good pattern, but not complete. The pattern really only works when surrounded with other patterns that actually give you the ownership and control you'll need. Kent and I fell into that. We didn't make it for ourselves. But we recognized we had it, and used it.

The pattern is anything but obsolete today. You're probably thinking that 99.9 percent of all software written is written on computers that unplug. But can you unplug them? I was thinking about workstations when I first articulated the pattern a decade ago. We thought they would be the locus of power. But it's turned out servers hold the power now. Can you unplug yours? Can you even get it on the phone?

I maintain an internet presence that I set up with the help of a particularly enlightened provider. I have a server on my premises with a plug that I own. Although the bandwidth of my connection is modest, it is continuous. I've found the character of the whole configuration to be categorically better than simpler arrangements. On my machine I run programs that are unwelcome elsewhere: programs that open their own connections, or just run without stopping. I don't have to ask permission.

We are just consumers to the huge corporations of the computer and telecommunications industry. They want to sell to us all right, but they won't sell us everything we need; that is, they won't make us powerful, unless we insist. Pay attention to the pattern. If we computer users are to have and hold the kind of ownership Kent and I have known, we are going to have to watch those plugs.

© 1997, Ward Cunningham. All rights reserved.
