# Alan Kay의 OOP를 Java code에 적용해보기
## Alan Kay's OOP Pratices in Java
(내 나름대로, 내가 이해한)앨런 캐이의 객체지향을 자바코드에 적용해보자.  
  
[Smalltalk와 LISP에서만 가능하다](https://github.com/juniqlim/note/blob/master/programming/2023-03-17-alan-kay-oop.md)고 했지만, 가능한 부분만 시도해보자.

## Pratices
1. [setter 금지](https://www.quora.com/In-object-oriented-programming-why-is-it-bad-practice-to-make-data-members-public-when-the-get-set-public-members-modify-it-anyway/answer/Alan-Kay-11)
2. [인스턴스 필드는 final](https://www.quora.com/Why-is-functional-programming-seen-as-the-opposite-of-OOP-rather-than-an-addition-to-it/answer/Alan-Kay-11)
3. [공개메소드의 요청/응답을 단순하게](https://disqus.com/home/discussion/yegor256/alan_kay_was_wrong_about_him_being_wrong/#comment-3851868732)

## 예제
먼저 간단한 코드를 준비했다.  
[RealWorld라는 블로그 애플리케이션은 글을 만들때](https://realworld-docs.netlify.app/docs/specs/backend-specs/endpoints#create-article) 제목으로 slug를 만들어야한다.  
'How to train your dragon' -> 'how-to-train-your-dragon'  
이 요구사항을 코드로 만들어 보았다.
```java
    DataStructureArticle makeDataStructureArticle(String title, String content) {
        String lowerCase = title.toLowerCase();
        String slug = lowerCase.replace(" ", "-");
    
        DataStructureArticle article = new DataStructureArticle();
        article.setTitle(title);
        article.setContent(content);
        article.setSlug(slug);
    
        return article;
    }
    
    class DataStructureArticle {
        private String title;
        private String content;
        private String slug;
    
        public void setSlug(String slug) {
            this.slug = slug;
        }
    
        public void setTitle(String title) {
        }
    
        public void setContent(String content) {
        }
    
        public String getSlug() {
            return slug;
        }
    }
```
구조체+프로시저 스타일의 코드다.  
  
이 코드는 아래의 테스트 코드처럼 사용되어진다.
```java
    @Test
    void makeDataStructureArticle() {
        MakeArticle.DataStructureArticle article = makeArticle.makeDataStructureArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.getSlug());
    }
```
### 1.'setter 금지' 실천방법을 적용해본다.
```java
    MutableObjectArticle makeMutableObjectArticle(String title, String content) {
        MutableObjectArticle article = new MutableObjectArticle(title, content);
        article.setSlug();

        return article;
    }

    class MutableObjectArticle {
        private String title;
        private String content;
        private String slug;

        public MutableObjectArticle(String title, String content) {
            this.title = title;
            this.content = content;
        }

        public void setSlug() {
            String lowerCase = title.toLowerCase();
            String slug = lowerCase.replace(" ", "-");
            this.slug = slug;
        }

        public String getSlug() {
            return slug;
        }
    }
```
가변객체 스타일의 코드다.  
slug를 만드는 명령적인 로직부분이 데이터가 위치한 객체 안으로 들어갔다. '글' 객체를 만드는 코드가 작아졌다.  
'글'객체는 변경가능한 상태를 가지고 있다. '글'객체의 참조가 다른 곳에서 사용되거나, 멀티 스레드 환경이라면 경쟁상태가 된다.  
코드 실행시 의도하지 않은 결과가 나올수 있다.  
  
이 코드는 아래의 테스트 코드처럼 사용되어진다.
```java
    @Test
    void makeMutableObjectArticle() {
        MakeArticle.MutableObjectArticle article = makeArticle.makeMutableObjectArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.getSlug());
    }
```  
### 2.'인스턴스 필드는 final' 실천방법을 적용해본다.
```java
    ImmutableObjectArticle immutableObjectArticle(String title, String content) {
        return new ImmutableObjectArticle(title, content, new SluggedString(title));
    }

    class ImmutableObjectArticle {
        private final String title;
        private final String content;
        private final SluggedString sluggedString;

        public ImmutableObjectArticle(String title, String content, SluggedString sluggedString) {
            this.title = title;
            this.content = content;
            this.sluggedString = sluggedString;
        }

        public SluggedString slug() {
            return sluggedString;
        }
    }

    static class SluggedString {
        private final String raw;

        public SluggedString(String raw) {
            this.raw = raw;
        }

        String value() {
            return raw.toLowerCase().replace(" ", "-");
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) return true;
            if (o == null || getClass() != o.getClass()) return false;
            SluggedString slug = (SluggedString) o;
            return Objects.equals(raw, slug.raw);
        }

        @Override
        public int hashCode() {
            return Objects.hash(raw);
        }
    }
```
불변객체 스타일의 코드다.  
slug를 만드는 로직이 객체로 분리되었다. '글'객체는 'slug'객체를 가지고 있다(Composition).  
객체는 변경가능한 상태가 없기 때문에 다루기 쉽다.

이 코드는 아래의 테스트 코드처럼 사용되어진다.
```java
    @Test
    void immutableObjectArticle() {
        MakeArticle.ImmutableObjectArticle article = makeArticle.immutableObjectArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.slug().value());
        assertEquals(new MakeArticle.SluggedString("How to train your dragon"), article.slug());
    }
```
메소드의 리턴값이 'slug'객체이다. 다른 코드에서 'slug'객체를 알게(의존하게)된다.  

### 3.'공개메소드의 요청/응답을 단순하게' 실천방법을 적용해본다.
```java
    ImmutableObjectDependencyFreeArticle immutableObjectDependencyFreeArticle(String title, String content) {
        return new ImmutableObjectDependencyFreeArticle(title, content, new Slugging().text(title));
    }

    class ImmutableObjectDependencyFreeArticle {
        private final String title;
        private final String content;
        private final String slug;

        public ImmutableObjectDependencyFreeArticle(String title, String content, String slug) {
            this.title = title;
            this.content = content;
            this.slug = slug;
        }

        public String slug() {
            return slug;
        }
    }

    static class Slugging {
        String text(String text) {
            return text.toLowerCase().replace(" ", "-");
        }
    }
```
불변객체 스타일의 코드다.  
객체를 모듈처럼 서버처럼 생각하고 구현해보았다.  
[데이터와 계산이 분리된 함수](https://www.yes24.com/Product/Goods/110253986) 처럼 보이기도 한다.  
> both OOP and functional computation can be completely compatible (and should be!)

OOP와 함수형 계산이 완벽하게 호환 가능해야된다는 앨런 선생님의 말씀에 가까워 졌는지도 모르겠다.  
  
이 코드는 아래의 테스트 코드처럼 사용되어진다.
```java
    @Test
    void immutableObjectDependencyFreeArticle() {
        MakeArticle.ImmutableObjectDependencyFreeArticle article = makeArticle.immutableObjectDependencyFreeArticle("How to train your dragon", "Ever wonder how?");
        assertEquals("how-to-train-your-dragon", article.slug());
    }
```
사용법이 다시 간단해 졌다.

전체 코드는 [여기](https://github.com/juniqlim/code-for-article/tree/master/aoop)에서 확인할 수 있다.
## Etc
Kent Beck의 XP가 그랬던 것 처럼, 가치와 원칙도 만들어 보았다.
### Principles
1. 'data structure and procedure' 구조를 없애기
2. 명령형 구문을 줄이기

### Values
확장성, 깔끔함, 시뮬레이션, 쉽게 정의(scalable, cleaner, simulation, easily define)

## 결론
앨런 캐이가
>[Better and perfect are the two enemies of 'what is actually needed'](https://www.quora.com/What-are-examples-of-Perfect-and-Better-in-regards-to-Alan-Kays-Sweet-Spot)

라고 말한 것 처럼, 무엇보다 '실제로 필요한 것'에 집중해야할 것이다.  
그리고 위 실천방법은 현재 나의 생각이기 때문에, 틀릴 수도 있고, 앞으로 생각이 바뀔수도 있겠다.

