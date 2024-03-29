# Alan Kay의 message oriented는 틀렸다고 말하는 Yegor Bugayenko에 대한 Alan의 반박
아래링크는 [엘레강트 오브젝트](https://product.kyobobook.co.kr/detail/S000001902572)의 저자 예고르의 글이다.  
https://www.yegor256.com/2017/12/12/alan-kay-was-wrong.html    
  
‘object’라는 용어는 오해의 소지가 있으니, ‘messaging'이라는 용어가 더 적절했다.  
라는 앨런 캐이의 말에, 예고르는 그렇지 않다고 했다.  
  
글을 요약해보자면,
## messaging, composition
객체 간 상호 작용에는 ‘messaging’과 ‘composition’이라는 두 수단이 있는데  
messaging
1. 객체들이 동등하고 독립적인 ‘모듈'로서 통신한다.
2. 다른객체와 ‘연결'되기 위해 불가피하게 많은 데이터를 노출해야된다. 캡슐화가 아니다.

composition
1. 통신해야하는 객체들을 더 큰 객체로 감싸서 통신한다.
2. 캡슐화보조 객체가 getter, printer등의 데이터 노출을 방지할 수 있다.  
  
따라서 객체에는 구성이, 모듈에는 메세징이 맞다고 주장한다. 그러므로 ‘object oriented’라는 이름이 맞단다.

## 본인 등판
흥미롭게도 [앨런 캐이가 댓글에 등장](https://disqus.com/home/discussion/yegor256/alan_kay_was_wrong_about_him_being_wrong/#comment-3658426409)했다. 깜짝놀랬다. 그가 말하길,
1. 객체와 모듈은 같다.
2. 가장좋은 메세지는 목표를 요청한다. 가장 좋은 객체는 ‘큰 목표’를 만족시킨다.
3. 보편적인 객체는 사용처가 많고, 더 포괄적인 객체는 의미론적으로 강해진다.(이해못함;)

tmi)앨런 캐이의 부인이 가끔 구글에서 남편을 찾아본다.

## 결론
나는 예고르의 OO을 좋아하고 배우고 써먹고 있었다. 앨런이 이야기하는 OO와도 일맥상통한 것으로 알고 있었다.  
하지만 꽤 핵심적인 부분이 차이가 있었다.  
  
코딩 관점에서 예고르와 앨런의 큰차이는 결국 getter 사용 유무인 것 같다.  

전부터 느꼈고, 이번에 [realworld](https://github.com/juniqlim/realworld-springboot-declarative-oop-style) 만들때도 느꼈는데,    
객체의 구성을 많이 사용했을때, 수정사항이 있으면 코드수정이 많았다. 객체들이 켜켜히 쌓여있을때, 깊숙히 손을 넣어서 뭔가 해야되면 일이 컸다.  
객체의 공개메소드(behavior/messaging)를 일반적으로 만들때, 유지보수가 쉽다고 느꼈다.  
  
앨런과 예고르의 이야기가, 코딩하는데 힌트가 될 것 같다.