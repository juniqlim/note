# Alan Kay가 틀렸다고 하는 글에 남긴 Alan의 댓글들 
[Alan Kay가 틀렸다고 하는 글에 남긴 Alan 반박글](https://github.com/juniqlim/note/blob/master/programming/2023-06-01-alan-say-about-alan-kay-was-wrong-about-him-being-wrong.md)에서 소개한 [yegor의 글](https://www.yegor256.com/2017/12/12/alan-kay-was-wrong.html)에 앨런은 많은 댓글을 남겼다.  
인상적이었던 멘트들을 모아봤다.  

1. 객체간의 비명령적(non-command nature) 메세지는 자동으로 캡슐화를 제공한다.
2. 객체는 발신자가 누구냐 등의 이유로 서로 다른 응답을 할 수있다. 이건 인터넷의 컴퓨터(서버)와 같은 개념이다.
3. 다형성이란 용어는 우리가 만든거 아님. 우린 generic messages/methods라고 부름.
4. 상속방식은 싫어서 위임사용.
5. 좋은 동적 시스템을 설계/구현하는 것은 어렵지만, 그 방법이 hign level이라면 또 가능한 simple하면 좋겠다.
6. 코딩해본 어른보다 어린이가 OO 배우는데 어려움이 없다.
7. 객체간의 비명령적 메세지는 자동으로 느슨한 결합을 제공한다.
8. 시스템설계 관점에서 ‘명령’을 없애고 ‘서비스’로 대체할때 더 발전을 이룰수 있다.
9. 명령형 == setter == 보통/전통적 프로그래밍
10. 객체에 대한 두가지 핵심아이디어 - 캡슐화/메세징
11. 내가 객체를 사용하게된 동기는, 구조체+프로시저를 없애고, 명령적 조정을 줄이기 위해.
12. 객체의 내부또한 시스템이다. 시스템을 만들기 위해 재귀적 구성을 사용한다.

## 패턴
그는 질문에 대해, 비슷하지만 조금씩 다른 이야기로 성실하게 답해준다.  
나는 몇가지 패턴을 발견했다.  
  
명령형 & setter & 데이터 & ADT & data structure and procedure & (내부변수 설정을 위한)할당문 & 전통적 프로그래밍  
은 서로 의미가 비슷하다.  
  
비명령형(선언형) & messaging & 서비스 & 캡슐화 & 느슨한 결합 & (그가 만든)객체 & 모듈
은 서로 의미가 비슷하다.

## 마무리
그가 직접쓴 글들은 [quora](https://www.quora.com/profile/Alan-Kay-11)에 특히 많고(현재 609개의 답변), 여기 저기 의외에 곳에 많이 등장한다.  
[quora](https://www.quora.com/profile/Alan-Kay-11)에 질문 하면 대답도 해주는 것 같다. 대신 모든 질문에 답해주는 건 아닌듯하다.  
  
오래전 글부터, 최근 글까지 그의 주장은 일관성이 있다고 생각한다. 그리고 곱씹어볼 만한 가치가 있다고 생각한다.  
  
  
그리고 내 머리를 쳤던 그의 [문구](https://disqus.com/home/discussion/yegor256/alan_kay_was_wrong_about_him_being_wrong/#comment-3685409247)
>I don't want to confuse things here, but one of the motivations for this kind of thinking was the realization that even "a bit" is not a thing but a process that sustains what it means to "be a bit". This is somewhat anti-Indo-European language and epistemological practice, which is very noun-heavy and process-light (e.g. we think of rocks as "things" rather than "processes"). Similarly, biologists (and former ones like me) think in terms of processes, even at the atomic level.
  
'암석'은 그냥 암석이지만, 지금 이순간도 작용중이다.