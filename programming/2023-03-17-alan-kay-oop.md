# Alan Kay가 OOP를 만든 이유
Alan Kay는 Object Oriented이란 용어를 처음 만들었다.   
Alan Kay의 OO에 대해 [좋은](https://velog.io/@eddy_song/alan-kay-OOP) [글](https://medium.com/javascript-scene/the-forgotten-history-of-oop-88d71b9b2d9f)[들](https://wiki.c2.com/?AlanKaysDefinitionOfObjectOriented)이 있다.  

## Alan Kay의 OOP
>(I'm not against types, but I don't know of any type systems that aren't a complete pain, so I still like dynamic typing.)  
OOP to me means only messaging, local retention and protection and hiding of state-process, and extreme late-binding of all things.  
It can be done in Smalltalk and in LISP.  
There are possibly other systems in which this is possible, but I'm not aware of them.  
(저는 타입에 대해 적대적이지는 않습니다만 완벽하게 고통이 없는 타입시스템은 본적이 없습니다. 그래서 여전히 다이나믹 타이핑을 좋아합니다.)  
저에게 있어서 OOP는 오직 메시징, 지역보존 및 보호, 상태-처리의 은닉, 모든것들에 대한 최후의 late-biding(Dynamic Binding)입니다.  
스몰토크와 LISP에서 가능합니다.  
이러한 것들이 가능한 다른 시스템들이 있을수 있지만 저는 그러한 시스템을 모릅니다.  

2003년에 작성된 그의 [글](http://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_en)(메일링)의 일부다. [번역본](http://everdeenoop.blogspot.com/2017/01/alan-kay-oop.html)도 있다.

Alan Kay의 OOP를 이야기 할때 많이 인용되는데, 스몰토크와 LISP에서 가능하다고 하는 말은 잘 인용이 되지 않는 듯 하다.

>The early one (just by accident) was the bio/net non-data-procedure route that I took.  
The other one, which came a little later as an object of study was abstract data types, and this got much more play.  
하나는(단지 우연에 의해) 제가 했던 생물학/네트워크 비데이터-프로시저 갈래였습니다.  
또 다른 갈래는, 객체에 대한 연구로서 좀 나중에 떠올랐던 것은 추상데이터 타입이었으며, 이것이 훨씬 더 많은 주목을 받았습니다.  

현재 일반적인 객체지향의 모습이, OO 용어를 처음만든 Alan Kay의 OO와 다른 이유가 조금 나온다.  
  
또 글을보면, 상속 좋아하지 않고 '다형성'이라는 용어는 타당하지 않다는 내용도 나온다.

## OOP를 만든 이유
Alan Kay는 1966년에 Object Oriented Programming란 용어를 만들었다고 한다.  
66년이면 현대의 컴퓨팅환경과 너무 많은 차이가 있다. 천공카드를 쓰던 시절이다. 그래서 그때 OOP의 필요성과 지금 OOP의 필요성은 다를 수 있겠다.  
다행히 Alan Kay는 2020년 3월 22일에 [어떤 생각이 객체 지향 프로그래밍을 발명하도록 이끌까요?](https://www.quora.com/What-thought-process-would-lead-one-to-invent-object-oriented-programming/answer/Alan-Kay-11)에 대한 답글을 썼다.  
  
현대에 그가 쓴 글을 보면,
> So, the thought processes that led to this were basically “systems thought processes” that were about being able to easily define systems of processes: any kinds of systems of any kinds of processes.  
> 따라서 이를 이끈 사고 프로세스는 기본적으로 프로세스의 시스템을 쉽게 정의할 수 있는 '시스템 사고 프로세스'였습니다: 모든 종류의 프로세스의 모든 종류의 시스템.  

프로세스의 시스템을 쉽게 정의하려고 하다가 OOP를 생각했다고 한다.

> Putting aside the practical difficulties this was very attractive as an idea, because it scaled much better than the traditional ideas of procedures and data structures as building blocks.  
> And it was so much cleaner, and so much more amenable to whole systems designs.  
> And so amenable to thinking in terms of “designing and programming simulations”.  
> 현실적인 어려움은 제쳐두고, 프로시저와 데이터 스트럭처를 빌딩 블록으로 사용하는 기존의 아이디어보다 훨씬 더 잘 확장할 수 있었기 때문에 아이디어로서 매우 매력적이었습니다.  
> 그리고 훨씬 더 깔끔하고 전체 시스템 설계에 훨씬 더 적합했습니다.  
> 그리고 '설계 및 프로그래밍 시뮬레이션'이라는 관점에서 생각하기에도 매우 용이했습니다.  

기존의 프로시저 & 데이터 스트럭처 보다 OOP는   
확장성이 좋고, 깔끔하고, 전체 시스템 설계에 적합하다고 한다.

> Another very attractive feature of having everything being made from “semantic software computers intercommunicating via messaging” is that some ugly properties of “data” could not only be fixed, but even eliminated.  
> 모든 것이 "메시징을 통해 상호 통신하는 시맨틱 소프트웨어 컴퓨터"로 만들어지는 것의 또 다른 매력적인 특징은 '데이터'의 일부 추악한 속성을 수정할 수 있을 뿐만 아니라 제거할 수도 있다는 점입니다.

OOP는 데이터를 제거할 수 있다고 한다.

> The data idea was always a bad one, and this new semantic building block would allow objects to progress through time — and “learn” etc. — but would be much safer.  
> 데이터 아이디어는 항상 나쁜 아이디어였으며, 이 새로운 시맨틱 빌딩 블록은 객체가 시간이 지남에 따라 발전하고 "학습" 등을 할 수 있게 해주지만 훨씬 더 안전할 것입니다.

[여기에서도](http://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_en) 데이터를 제거한다는 이야기를 한다. 프로시저와 함께하는 데이터를 나쁘게 생각하는 것 같다.      
시간이 지나면서 발전/학습한다는 것은 xp, ddd를 생각나게 한다.

> What hit me in Nov 1966 was ridiculously, absurdly simple:  
> “that, if you can have enough computers which can intercommunicate, this is all you need to define anything that can be done on a computer by any other means”.   
> This is because each computer is universal, etc.  
> 1966년 11월에 저를 강타한 것은 터무니없을 정도로 단순한 것이었습니다.  
> "너에게 상호 통신할 수 있는 컴퓨터들이 충분하다면, 이것은 다른 방식으로, (컴퓨터로 할수있는)무엇이든 정의하는데 필요한 전부이다." 이었습니다.   
> 각 컴퓨터가 범용적이기 때문입니다.  

객체를 상호 통신할 수 있는 작은 컴퓨터처럼 생각하는 것 같다.

나름대로 종합해보자면 OOP는,  
1. 시스템을 쉽게 정의
2. 좋은 확장성, 깔끔함
3. 데이터(프로시저&구조체)를 제거
하기 위해 탄생한 것 같다.

## no data
> C++ and Java etc. use objects mainly to define new things that are very like data structures, and the programming that is done is generally very data structure like (e.g. “setters” turn any kind of entity back into a data structure that can be imperatively munged by anyone).   
> Technically, this is actually “Abstract Data Structures” and though a subset of what can be done with objects, is a divergence from the intent.  
> C++과 Java 등은 주로 데이터 구조와 매우 유사한 새로운 것을 정의하는 데 객체를 사용하며, 이렇게 수행되는 프로그래밍은 일반적으로 데이터 구조와 매우 유사합니다(예: "세터"는 모든 종류의 엔티티를 누구나 필수적으로 뭉뚱그릴 수 있는 데이터 구조로 다시 전환합니다).   
> 엄밀히 말하면 이것은 "추상 데이터 구조"이며 객체로 할 수 있는 일의 하위 집합이지만, 의도와는 다른 것입니다.

구조체에 대해 Alan Kay는 특히 나쁘게 생각하는 것 같다.   
하지만 일반적인 애플리케이션이라면 데이터(구조체)의 입력/출력은 필수적이다.  
구조체를 최대한 덜 쓰고, 객체를 최대한 많이 사용한다면, 그가 원하는 OOP에 가까워지지 않을까?

## object가 아니고 messaging
이 [글](http://lists.squeakfoundation.org/pipermail/squeak-dev/1998-October/017019.html)에서 다소 충격적인 얘기가 나온다.
> I'm sorry that I long ago coined the term "objects" for this topic because it gets many people to focus on the lesser idea.
> The big idea is "messaging" -- that is what the kernal of Smalltalk/Squeak is all about
> The key in making great and growable systems is much more to design how its modules communicate rather than what their internal properties and behaviors should be.
> 제가 오래 전에 이 주제에 대해 "객체"라는 용어를 사용한 것에 대해 유감스럽게 생각합니다. 많은 사람들이 덜 중요한 아이디어에 집중하기 때문입니다.
> 큰 아이디어는 "메시징"입니다. 이것이 바로 Smalltalk/Squeak의 핵심입니다.
> 훌륭하고 성장 가능한 시스템을 만드는 데 있어 핵심은 모듈의 내부 속성과 동작보다는 모듈이 통신하는 방식을 설계하는 것입니다.
 
> If you focus on just messaging -- and realize that a good metasystem can late bind the various 2nd level architectures used in objects -- then much of the language-, UI-, and OS based discussions on this thread are really quite moot.
> 메시징에만 집중한다면 -- 좋은 메타시스템은 객체에 사용되는 다양한 2차 수준 아키텍처(구현 상세)를 뒤늦게 바인딩할 수 있다는 사실을 깨닫는다면 -- 이 스레드에서 언어, UI, OS에 기반한 논의의 상당 부분이 실제로는 상당히 무의미해집니다.

객체라는 용어를 사용한것이 후회된다는 듯하다.  
핵심은 object가 아니라 messaging이라고 한다. 
[여기](https://www.quora.com/Why-is-object-oriented-programming-more-about-messaging-than-objects/answer/Alan-Kay-11)에서 좀 더 설명해준다.

> 1. '무언가'에게 메시지를 보내는 경우 어떤 종류의 메시지를 보내고 싶으신가요? 예를 들어, 명령하는 건가요, 요청하는 건가요, 제안하는 건가요, 협상하는 건가요?
> 2. '무언가'에게 메시지를 보낼 수 있다면 영원히 묶여 있지 않고 마음이 바뀔 수 있으며 상대방도 바뀔 수 있습니다.
> 3. 메시지를 보낼 수 있다면 정말 특정 대상에게만 메시지를 보내고 싶으신가요? 필요에 따라 요청을 보내는 것이 더 나을 수 있으며, 또한 공동체에 X, Y, Z를 공급할 수 있다고 시스템에 알려주는 것이 나을 수 있습니다.

'무언가'가 어떻게 동작하는지에 집중하기 보다, '무언가'에게 어떤 메세지를 보낼지에 집중하라고 하는 것 같다.
객체를 만들때 또 네이밍할때, 어떻게 보다 무엇이 들어나야된다는 이야기와도 통하는 것 같다.

[헐퀴](https://softwareengineering.stackexchange.com/questions/46592/so-what-did-alan-kay-really-mean-by-the-term-object-oriented)
>I was too blythe about the term back in the 60s and should have chosen something like "message oriented"  
>Alan Kay Jun 8, 2011 at 16:27

## 그래서 어떻게 해야되지?

그가 작성한 [세](http://userpage.fu-berlin.de/~ram/pub/pub_jf47ht81Ht/doc_kay_oop_en)[개](https://www.quora.com/What-thought-process-would-lead-one-to-invent-object-oriented-programming/answer/Alan-Kay-11)[의 글](http://lists.squeakfoundation.org/pipermail/squeak-dev/1998-October/017019.html)을 종합하여, 실천할 수 있는 방법을 내가 도출해본다면.
1. 메세징을 사용한다. '어떻게' 보다 '무엇'에 집중한다.(what to build, not how to work)
2. 데이터(구조체)를 지양한다.(no getter, setter)
3. 늦은 바인딩을 사용한다.(use interface)
4. 상속을 지양한다.(no extends)
인 것 같다.

> The flaw in how things have played out is that very few in computing actually put in the effort to grok the implications of “universal scalable systems of processes”, and instead have clung to very old and poorly scalable ways to program.  
> 상황이 이렇게 흘러온 데에는 컴퓨팅 업계에서 '보편적으로 확장 가능한 프로세스 시스템'의 의미를 파악하려는 노력을 기울이는 사람이 거의 없고, 대신 매우 오래되고 확장성이 떨어지는 프로그래밍 방식에 집착해 왔다는 결함이 있습니다.

2020년에 그가 한 이야기이다. 1960년대부터 현재까지, OOP는 왜곡되어 온 것일까?  
