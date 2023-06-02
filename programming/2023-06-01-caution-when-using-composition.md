# 상속보다 구성이 좋다. 그런데 구성할때 생각해볼 점.

상속보다 구성이 좋는 것은, 많은 사람들이 공감하는 주류의견인 것 같다.
나 또한 상속을 멀리하고 구성을 좋아하고 즐겨썼다.

그런데 [Alan Kay가 틀렸다고 하는 글에 남긴 Alan 반박글](https://github.com/juniqlim/note/blob/master/programming/2023-06-01-alan-say-about-alan-kay-was-wrong-about-him-being-wrong.md)에서 소개한 [yegor의 글](https://www.yegor256.com/2017/12/12/alan-kay-was-wrong.html)에 있는 [댓글](https://disqus.com/home/discussion/yegor256/alan_kay_was_wrong_about_him_being_wrong/#comment-3718437603)을 보고 생각이 많아졌다.  

요약해보면,
1. [David West](https://www.amazon.com/Object-Thinking-Developer-Reference-David/dp/0735619654) 아이디어의 핵심은, 문제공간(problem space)의 객체분해(object decomposition)다. 메세지의 핵심은 분해가 일어나도록 하는 것.
2. 객체는 명령/제어 관계에서 벗어나지 않으면 독립적으로 행동할 수 없다. 한 곳에서 문제를 처리할 뿐이다.
3. 객체는 문제 공간에서 스스로 작동할 수 있는 의인화된 개념. 메세지는 이를 가능하게 하는 체계. 
4. 메세징이 시스템에서 필요로하는 상태 변경을 허용하고, 객체들이 상태를 캡슐화하여 객체들 스스로 분배하기 때문에 작동함.
5. OOP 관점에서 문제를 해결하는 방법은, 문제 공간의 개념을 객체로 모델링하고, 원하는 대로 동작하도록 배열하는것. 이를 위해서 객체는 서로 동등해야되는데 예고르는 그걸 [잘 못 됬다고](https://github.com/juniqlim/note/blob/master/programming/2023-06-01-alan-say-about-alan-kay-was-wrong-about-him-being-wrong.md) 함. 그는 OO의 근본 개념인 decomposition에 반대하고 있는 것.
6. decomposition되지 못한 객체는 여전히 절차적 프로그래밍이다.
7. 그의 코드는 작고, 촘촘하고, 캡슐화 된 객체로 이루어져 우아하게 보이지만, 여전히 프로시저/데이터 가방이다.

나는 엘레강트 오브젝트 책을 보고, 예고르의 생각에 동의했다. 그래서 그의 블로그 글도 읽어보고, 그의 스타일대로 코드를 작성하려고 노력했다.
그런데 위의 글은 나에게 설득력 있게 다가온다. 그 동안 좀 이상하다 생각되는 부분이 풀린 것 같다.  
그렇다고 그의 글 모두를 부정하는 것은 절대 아니다.  

객체들의 구성(composition)으로 문제를 해결할때, 변경사항이 있으면 고쳐야할 코드가 너무 많을때가 있다.  
위 글대로 문제 공간의 분리가 이루어지지 않았기 때문이 아닐까?  
나는 상속은 OO 스럽지 못해서 구성을 선택했는데, 여전히 절차지향적이진 않았나?