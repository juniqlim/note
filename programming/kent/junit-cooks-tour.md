# JUnit 쿡스 투어 (JUnit A Cook's Tour)
https://curlunit.sourceforge.net/doc/cookstour/cookstour.htm
에리히 감마(Erich Gamma)와 켄트 벡(Kent Beck)이 JUnit의 설계를 패턴으로 설명한 글을 번역했습니다.

## 1. 소개 (Introduction)

이전 글(Test Infected: Programmers Love Writing Tests, Java Report, 1998년 7월, 3권 7호 참고)에서 우리는 간단한 프레임워크를 사용해 반복 가능한 테스트(repeatable tests)를 작성하는 방법을 설명했다. 이번 글에서는 그 내부를 들여다보고 프레임워크 자체가 어떻게 만들어졌는지 보여주려 한다.

우리는 JUnit 프레임워크를 꼼꼼히 연구하고 우리가 그것을 어떻게 구성했는지 되돌아보았다. 그 결과 여러 다른 수준에서 교훈을 얻었다. 이 글에서는 그 모든 교훈을 한꺼번에 전달해 보려 한다. 가망 없는 작업이지만, 적어도 가치가 입증된 소프트웨어의 설계와 구축 과정을 보여주는 맥락 안에서 그렇게 할 것이다.

먼저 프레임워크의 목표(goals)를 논의하는 것으로 시작한다. 이 목표들은 프레임워크 자체를 소개하는 동안 여러 작은 세부 사항에서 다시 등장할 것이다. 이어서 프레임워크의 설계와 구현을 제시한다. 설계는 패턴(patterns)으로 설명하고(놀랍게도!), 구현은 문학적 프로그램(literate program) 형태로 설명한다. 마지막으로 프레임워크 개발에 대한 몇 가지 엄선된 생각으로 마무리한다.

## 2. 목표 (Goals)

JUnit의 목표는 무엇인가?

먼저 개발의 전제(assumptions)로 돌아가야 한다. 어떤 프로그램 기능에 자동화된 테스트(automated test)가 없다면, 우리는 그 기능이 동작하지 않는다고 가정한다. 이는 "개발자가 기능이 동작한다고 보장하면 그것은 지금도, 앞으로도 영원히 동작한다"는 지배적인 가정보다 훨씬 안전해 보인다.

이 관점에서 보면, 개발자는 코드를 작성하고 디버깅했다고 일이 끝난 것이 아니다. 프로그램이 동작함을 입증하는 테스트도 작성해야 한다. 하지만 모두가 너무 바쁘고, 할 일이 너무 많고, 테스트나 만지작거릴 시간이 없다. "이미 작성할 코드가 산더미인데, 테스트 코드까지 어떻게 작성하라는 겁니까? 대답해 보시죠, 깐깐한 프로젝트 매니저님(Mr. Hard-case Project Manager)."

그래서 첫 번째 목표는, 개발자가 실제로 테스트를 작성할 것이라는 희미한 희망이라도 가질 수 있는 프레임워크를 만드는 것이다. 프레임워크는 익숙한 도구를 사용해야 하므로 새로 배울 것이 거의 없어야 한다. 새 테스트를 작성하는 데 꼭 필요한 것 이상의 작업을 요구해서는 안 된다. 중복된 노력(duplicated effort)을 없애야 한다.

테스트가 해야 할 일이 이것뿐이라면, 디버거에서 표현식을 작성하는 것만으로 충분할 것이다. 하지만 그것만으로는 테스트에 충분하지 않다. 당신의 프로그램이 지금 동작한다고 말해주는 것은 내게 도움이 되지 않는다. 내가 통합(integrate)한 1분 뒤에도 동작할 것이라는 보장이 없고, 당신이 떠나고 없을 5년 뒤에도 여전히 동작할 것이라는 보장도 없기 때문이다.

그래서 테스트의 두 번째 목표는 시간이 지나도 가치를 유지하는 테스트를 만드는 것이다. 원래 작성자가 아닌 다른 사람도 테스트를 실행하고 결과를 해석할 수 있어야 한다. 여러 작성자의 테스트를 결합해 서로 간섭할 걱정 없이 함께 실행할 수 있어야 한다.

마지막으로, 기존 테스트를 활용(leverage)해 새 테스트를 만들 수 있어야 한다. 셋업(setup) 또는 픽스처(fixture)를 만드는 일은 비용이 크므로, 프레임워크는 픽스처를 재사용해 서로 다른 테스트를 실행할 수 있게 해야 한다. 아, 그게 전부냐고?

## 3. JUnit의 설계 (The Design of JUnit)

JUnit의 설계는 "Patterns Generate Architectures"(Kent Beck, Ralph Johnson, ECOOP 94)에서 처음 사용된 방식으로 제시한다. 아무것도 없는 상태에서 시작해 시스템의 아키텍처가 완성될 때까지 패턴을 하나씩 적용하며 시스템 설계를 설명하는 방식이다. 해결해야 할 아키텍처 문제를 제시하고, 그 문제를 해결하는 패턴을 요약한 뒤, 그 패턴이 JUnit에 어떻게 적용되었는지 보여줄 것이다.

### 3.1 시작하기 — TestCase (Getting started)

먼저 우리의 기본 개념인 TestCase를 표현하는 객체를 만들어야 한다. 개발자들은 흔히 테스트 케이스를 머릿속에 가지고 있지만, 그것을 다양한 방식으로 실현한다.

- print 문(print statements)
- 디버거 표현식(debugger expressions)
- 테스트 스크립트(test scripts)

테스트를 쉽게 다루고 싶다면 테스트를 객체로 만들어야 한다. 그러면 개발자의 머릿속에만 암묵적으로 있던 테스트가 구체화되며, 이는 시간이 지나도 가치를 유지하는 테스트를 만든다는 목표를 뒷받침한다. 동시에 객체 개발자들은, 말하자면, 객체로 개발하는 데 익숙하므로 테스트를 객체로 만들기로 한 결정은 테스트 작성을 더 매력적으로(적어도 덜 부담스럽게) 만든다는 목표도 뒷받침한다.

커맨드 패턴(Command pattern)(Gamma, E. 외, Design Patterns: Elements of Reusable Object-Oriented Software, Addison-Wesley, 1995 참고)은 우리의 필요에 아주 잘 맞는다. 그 의도(intent)를 인용하면 "요청을 객체로 캡슐화(encapsulate)하여 요청을 큐에 넣거나 로그로 남길 수 있게 한다…". 커맨드는 연산(operation)을 위한 객체를 만들고 그 객체에 "execute" 메서드를 부여하라고 말한다. 다음은 TestCase의 클래스 정의 코드다.

```java
public abstract class TestCase implements Test {
    …
}
```

이 클래스는 상속(inheritance)을 통해 재사용될 것으로 예상하므로 "public abstract"로 선언한다. 지금은 Test 인터페이스를 구현한다는 사실은 무시하자. 현재 설계 단계에서는 TestCase를 독립된 클래스로 생각해도 된다.

모든 TestCase는 이름을 가지고 생성되므로, 테스트가 실패하면 어떤 테스트가 실패했는지 식별할 수 있다.

```java
public abstract class TestCase implements Test {
    private final String fName;

    public TestCase(String name) {
        fName= name;
    }

    public abstract void run();
        …
}
```

JUnit의 진화를 설명하기 위해 아키텍처의 스냅숏(snapshot)을 보여주는 다이어그램을 사용한다. 표기법은 단순하다. 관련 패턴이 적힌 음영 상자로 클래스에 주석을 단다. 패턴에서 클래스의 역할(role)이 명확하면 패턴 이름만 표시한다. 역할이 명확하지 않으면 음영 상자에 이 클래스에 해당하는 참여자(participant)의 이름을 덧붙인다. 이 표기법은 다이어그램의 어수선함을 최소화하며, "Applying Design Patterns in Java"(Gamma, E., Java Gems, SIGS Reference Library, 1997)에서 처음 소개되었다. 그림 1은 이 표기법을 TestCase에 적용한 것이다. 단일 클래스를 다루고 있어 모호함이 있을 수 없으므로 패턴 이름만 표시했다.

![그림 1 TestCase에 Command 적용](https://curlunit.sourceforge.net/doc/cookstour/Image1.gif)

**그림 1** TestCase에 Command 적용

### 3.2 채워 넣을 빈칸 — run() (Blanks to fill in)

다음으로 풀어야 할 문제는 개발자가 픽스처 코드와 테스트 코드를 넣을 편리한 "장소"를 제공하는 것이다. TestCase를 abstract로 선언했다는 것은 개발자가 서브클래싱(subclassing)으로 TestCase를 재사용할 것이라는 뜻이다. 하지만 변수 하나에 동작은 없는 슈퍼클래스만 제공할 수 있다면, 테스트를 쉽게 작성하게 한다는 첫 번째 목표를 충족하는 데 별 도움이 되지 않을 것이다.

다행히 모든 테스트에는 공통 구조가 있다. 테스트 픽스처를 준비(set up)하고, 픽스처에 대해 어떤 코드를 실행하고, 결과를 확인하고, 픽스처를 정리(clean up)한다. 이는 각 테스트가 새 픽스처로 실행되며 한 테스트의 결과가 다른 테스트의 결과에 영향을 줄 수 없다는 뜻이다. 이것은 테스트의 가치를 극대화한다는 목표를 뒷받침한다.

템플릿 메서드(Template Method)가 우리 문제를 아주 잘 해결한다. 그 의도를 인용하면 "연산에서 알고리즘의 뼈대(skeleton)를 정의하고 일부 단계를 서브클래스로 미룬다. 템플릿 메서드는 알고리즘의 구조를 바꾸지 않고 서브클래스가 알고리즘의 특정 단계를 재정의할 수 있게 한다." 정확히 맞다. 우리는 개발자가 픽스처(set up과 tear down) 코드를 작성하는 방법과 테스트 코드를 작성하는 방법을 따로 고민할 수 있기를 원한다. 하지만 이 순서의 실행은 픽스처 코드나 테스트 코드를 어떻게 작성하든 모든 테스트에서 동일하게 유지된다.

다음은 템플릿 메서드다.

```java
public void run() {
    setUp();
    runTest();
    tearDown();
}
```

이 메서드들의 기본 구현은 아무것도 하지 않는다.

```java
protected void runTest() {
}

protected void setUp() {
}

protected void tearDown() {
}
```

setUp과 tearDown은 오버라이드되도록 의도되었지만 프레임워크가 호출하므로 protected로 선언한다. 투어의 두 번째 스냅숏은 그림 2와 같다.

![그림 2 TestCase.run()에 Template Method 적용](https://curlunit.sourceforge.net/doc/cookstour/Image2.gif)

**그림 2** TestCase.run()에 Template Method 적용

### 3.3 결과 보고 — TestResult (Reporting results)

숲속에서 TestCase가 실행된다면, 누가 그 결과에 신경 쓸까? 물론 신경 쓴다. 테스트는 그것이 통과하는지 확인하려고 실행하는 것이니까. 테스트를 실행한 뒤에는 무엇이 동작했고 무엇이 동작하지 않았는지에 대한 기록, 즉 요약을 원한다.

테스트가 성공하거나 실패할 확률이 같다면, 혹은 테스트를 하나만 실행한다면, TestCase 객체에 플래그를 설정해 두고 테스트가 끝났을 때 그 플래그를 보면 된다. 하지만 테스트는 (의도적으로) 매우 비대칭적(asymmetric)이다. 대개는 통과한다. 그러므로 실패만 기록하고 성공은 아주 압축된 요약만 남기고 싶다.

Smalltalk Best Practice Patterns(Beck, K., Prentice Hall, 1996 참고)에 적용할 만한 패턴이 있다. *수집 매개변수(Collecting Parameter)*라는 패턴이다. 여러 메서드에 걸쳐 결과를 수집해야 할 때, 메서드에 매개변수를 추가하고 결과를 대신 수집해 줄 객체를 전달하라고 제안한다. 우리는 테스트 실행 결과를 수집할 새 객체 TestResult를 만든다.

```java
public class TestResult extends Object {
    protected int fRunTests;

    public TestResult() {
        fRunTests= 0;
    }
}
```

이 단순한 버전의 TestResult는 실행된 테스트 수만 센다. 이를 사용하려면 TestCase.run() 메서드에 매개변수를 추가하고 테스트가 실행 중임을 TestResult에 알려야 한다.

```java
public void run(TestResult result) {
    result.startTest(this);
    setUp();
    runTest();
    tearDown();
}
```

그리고 TestResult는 실행된 테스트 수를 추적해야 한다.

```java
public synchronized void startTest(Test test) {
    fRunTests++;
}
```

TestResult의 startTest 메서드를 synchronized로 선언해, 테스트가 여러 스레드에서 실행될 때도 하나의 TestResult가 안전하게 결과를 수집할 수 있게 한다. 마지막으로, TestCase의 단순한 외부 인터페이스를 유지하고 싶으므로 자체적으로 TestResult를 생성하는 매개변수 없는 run()을 만든다.

```java
public TestResult run() {
    TestResult result= createResult();
    run(result);
    return result;
}

protected TestResult createResult() {
    return new TestResult();
}
```

그림 3은 다음 설계 스냅숏이다.

![그림 3 TestResult에 Collecting Parameter 적용](https://curlunit.sourceforge.net/doc/cookstour/Image3.gif)

**그림 3** TestResult에 Collecting Parameter 적용

테스트가 항상 올바르게 통과한다면 굳이 작성할 필요가 없을 것이다. 테스트는 실패할 때, 특히 실패를 예상하지 못했을 때 흥미롭다. 게다가 테스트는 예상한 방식으로, 예를 들어 잘못된 결과를 계산해서 실패할 수도 있고, 배열 범위 밖에 쓰는 것처럼 더 극적인 방식으로 실패할 수도 있다. 테스트가 어떻게 실패하든 우리는 이어지는 테스트들을 계속 실행하고 싶다.

JUnit은 *실패(failures)*와 *오류(errors)*를 구분한다. 실패는 그 가능성이 예상된 것이며 단언(assertions)으로 검사한다. 오류는 ArrayIndexOutOfBoundsException 같은 예상치 못한 문제다. 실패는 AssertionFailedError 오류로 신호를 보낸다. 예상치 못한 오류와 실패를 구분하기 위해, 실패는 별도의 catch 절(1)에서 잡는다. 두 번째 절(2)은 나머지 모든 예외를 잡아 테스트 실행이 계속되도록 보장한다.

```java
public void run(TestResult result) {
    result.startTest(this);
    setUp();
    try {
        runTest();
    }
    catch (AssertionFailedError e) { //1
        result.addFailure(this, e);
    }

    catch (Throwable e) { // 2
        result.addError(this, e);
    }
    finally {
        tearDown();
    }
}
```

AssertionFailedError는 TestCase가 제공하는 assert 메서드에 의해 발생한다. JUnit은 다양한 용도의 assert 메서드 세트를 제공한다. 가장 단순한 것은 다음과 같다.

```java
protected void assert(boolean condition) {
    if (!condition)
        throw new AssertionFailedError();
}
```

AssertionFailedError는 클라이언트(TestCase 안의 테스트 메서드)가 잡도록 의도된 것이 아니라 템플릿 메서드인 TestCase.run() 안에서 잡도록 의도되었다. 그래서 AssertionFailedError를 Error에서 파생시킨다.

```java
public class AssertionFailedError extends Error {
    public AssertionFailedError () {}
}
```

TestResult에서 오류를 수집하는 메서드는 다음과 같다.

```java
public synchronized void addError(Test test, Throwable t) {
    fErrors.addElement(new TestFailure(test, t));
}

public synchronized void addFailure(Test test, Throwable t) {
    fFailures.addElement(new TestFailure(test, t));
}
```

TestFailure는 나중에 보고할 수 있도록 실패한 테스트와 발생한 예외를 묶어주는 작은 프레임워크 내부 헬퍼 클래스다.

```java
public class TestFailure extends Object {
    protected Test fFailedTest;
    protected Throwable fThrownException;
}
```

수집 매개변수의 정석적인 형태(canonical form)는 수집 매개변수를 각 메서드에 전달하도록 요구한다. 이 조언을 따른다면 각 테스트 메서드마다 TestResult 매개변수가 필요할 것이다. 이는 메서드 시그니처의 "오염(pollution)"을 낳는다. 실패를 알리는 데 예외를 사용한 덕분에 생긴 반가운 부수 효과로, 이런 시그니처 오염을 피할 수 있다. 테스트 케이스 메서드나 거기서 호출되는 헬퍼 메서드는 TestResult에 대해 알 필요 없이 예외를 던질 수 있다. 복습 삼아 MoneyTest 스위트의 테스트 메서드 예시를 보자. 테스트 메서드가 TestResult에 대해 아무것도 알 필요가 없음을 보여준다.

```java
public void testMoneyEquals() {
    assert(!f12CHF.equals(null));
    assertEquals(f12CHF, f12CHF);
    assertEquals(f12CHF, new Money(12, "CHF"));
    assert(!f12CHF.equals(f14CHF));
}
```

JUnit에는 여러 TestResult 구현이 함께 제공된다. 기본 구현은 실패와 오류의 수를 세고 결과를 수집한다. TextTestResult는 결과를 수집해 텍스트 형태로 보여준다. 마지막으로 UITestResult는 그래픽 버전의 JUnit Test Runner가 그래픽 테스트 상태를 갱신하는 데 사용한다.

TestResult는 프레임워크의 확장 지점(extension point)이다. 클라이언트는 자신만의 TestResult 클래스를 정의할 수 있다. 예를 들어 HTMLTestResult는 결과를 HTML 문서로 보고한다.

### 3.4 어리석은 서브클래스는 그만 — 다시 TestCase (No stupid subclasses)

우리는 테스트를 표현하기 위해 커맨드를 적용했다. 커맨드는 execute()(TestCase에서는 run()) 같은 단일 메서드로 호출된다. 이 단순한 인터페이스 덕분에 같은 인터페이스를 통해 커맨드의 서로 다른 구현을 호출할 수 있다.

테스트를 범용적으로 실행할 인터페이스가 필요하다. 그런데 모든 테스트 케이스는 같은 클래스 안의 서로 다른 메서드로 구현된다. 이렇게 하면 불필요한 클래스 증식을 피할 수 있다. 어떤 테스트 케이스 클래스는 여러 메서드를 구현할 수 있고, 각 메서드가 하나의 테스트 케이스를 정의한다. 각 테스트 케이스는 testMoneyEquals나 testMoneyAdd 같은 서술적인 이름을 가진다. 이 테스트 케이스들은 단순한 커맨드 인터페이스에 들어맞지 않는다. 같은 Command 클래스의 서로 다른 인스턴스가 서로 다른 메서드로 호출되어야 한다. 따라서 다음 문제는 테스트를 호출하는 쪽(invoker)의 관점에서 모든 테스트 케이스를 똑같이 보이게 만드는 것이다.

사용 가능한 디자인 패턴들이 다루는 문제를 살펴보면 어댑터 패턴(Adapter pattern)이 떠오른다. 어댑터의 의도는 "클래스의 인터페이스를 클라이언트가 기대하는 다른 인터페이스로 변환한다"이다. 잘 맞아 보인다. 어댑터는 이를 위한 여러 방법을 알려준다. 그중 하나는 서브클래싱으로 인터페이스를 맞추는 클래스 어댑터(class adapter)다. 예를 들어 testMoneyEquals를 runTest에 맞추려면 MoneyTest의 서브클래스를 구현하고 runTest를 오버라이드해 testMoneyEquals를 호출하게 한다.

```java
public class TestMoneyEquals extends MoneyTest {
    public TestMoneyEquals() { super("testMoneyEquals"); }
    protected void runTest () { testMoneyEquals(); }
}
```

서브클래싱을 사용하면 테스트 케이스마다 서브클래스를 구현해야 한다. 이는 테스트 작성자에게 추가 부담을 준다. 테스트 케이스를 최대한 간단하게 추가할 수 있어야 한다는 JUnit의 목표에 어긋난다. 게다가 테스트 메서드마다 서브클래스를 만들면 클래스가 비대해진다(class bloat). 메서드가 하나뿐인 클래스가 많으면 비용 대비 가치가 없고, 의미 있는 이름을 짓기도 어렵다.

Java는 익명 내부 클래스(anonymous inner classes)를 제공하는데, 이는 클래스 이름 짓기 문제에 대한 흥미로운 Java 고유의 해결책이 된다. 익명 내부 클래스를 사용하면 클래스 이름을 지어내지 않고도 어댑터를 만들 수 있다.

```java
TestCase test= new MoneyTest("testMoneyEquals ") {
    protected void runTest() { testMoneyEquals(); }
};
```

이는 완전한 서브클래싱보다 훨씬 편리하다. 개발자에게 약간의 부담을 주는 대신 컴파일 타임 타입 검사를 유지한다. Smalltalk Best Practice Patterns는 서로 다른 인스턴스가 서로 다르게 동작하는 문제에 대해 *플러그 가능한 동작(pluggable behavior)*이라는 공통 제목 아래 또 다른 해결책을 설명한다. 서브클래싱 없이 다른 로직을 수행하도록 매개변수화할 수 있는 단일 클래스를 사용한다는 아이디어다.

플러그 가능한 동작의 가장 단순한 형태는 *플러그 가능한 셀렉터(Pluggable Selector)*다. 플러그 가능한 셀렉터는 Smalltalk 메서드 셀렉터를 인스턴스 변수에 저장한다. 이 아이디어는 Smalltalk에만 국한되지 않으며 Java에도 적용할 수 있다. Java에는 메서드 셀렉터라는 개념이 없다. 하지만 Java 리플렉션 API(reflection API)를 사용하면 메서드 이름을 나타내는 문자열로 메서드를 호출할 수 있다. 이 기능으로 Java에서 플러그 가능한 셀렉터를 구현할 수 있다. 여담이지만, 우리는 일반 애플리케이션 코드에서는 보통 리플렉션을 사용하지 않는다. 여기서는 인프라 프레임워크를 다루고 있으므로 리플렉션 모자를 써도 괜찮다.

JUnit은 클라이언트에게 플러그 가능한 셀렉터를 사용하거나 위와 같이 익명 어댑터 클래스를 구현하는 선택지를 준다. 이를 위해 runTest 메서드의 기본 구현으로 플러그 가능한 셀렉터를 제공한다. 이 경우 테스트 케이스의 이름은 테스트 메서드의 이름과 일치해야 한다. 아래와 같이 리플렉션으로 메서드를 호출한다. 먼저 Method 객체를 찾는다. Method 객체를 얻으면 인자를 전달해 호출할 수 있다. 테스트 메서드는 인자를 받지 않으므로 빈 인자 배열을 전달하면 된다.

```java
protected void runTest() throws Throwable {
    Method runMethod= null;
    try {
        runMethod= getClass().getMethod(fName, new Class[0]);
    } catch (NoSuchMethodException e) {
        assert("Method \""+fName+"\" not found", false);
    }
    try {
        runMethod.invoke(this, new Class[0]);
    }
    // catch InvocationTargetException and IllegalAccessException
}
```

JDK 1.1 리플렉션 API는 public 메서드만 찾을 수 있다. 그래서 테스트 메서드를 public으로 선언해야 하며, 그렇지 않으면 NoSuchMethodException이 발생한다.

다음은 어댑터와 플러그 가능한 셀렉터가 추가된 다음 설계 스냅숏이다.

![그림 4 TestCase에 익명 내부 클래스를 이용한 Adapter 또는 Pluggable Selector 적용](https://curlunit.sourceforge.net/doc/cookstour/Image4.gif)

**그림 4** TestCase에 익명 내부 클래스를 이용한 Adapter 또는 Pluggable Selector 적용

### 3.5 하나든 여럿이든 상관없다 — TestSuite (Don't care about one or many)

시스템 상태에 확신을 가지려면 많은 테스트를 실행해야 한다. 지금까지 JUnit은 단일 테스트 케이스를 실행하고 그 결과를 TestResult에 보고할 수 있다. 다음 과제는 여러 테스트를 실행할 수 있도록 확장하는 것이다. 테스트를 호출하는 쪽이 하나를 실행하든 여러 개를 실행하든 신경 쓰지 않아도 된다면 이 문제는 쉽게 풀린다. 이런 상황에서 흔히 꺼내 드는 패턴이 컴포지트(Composite)다. 그 의도를 인용하면 "객체를 트리 구조로 구성해 부분-전체 계층(part-whole hierarchies)을 표현한다. 컴포지트는 클라이언트가 개별 객체와 객체의 조합을 동일하게 다룰 수 있게 한다." 여기서 관심 있는 것은 부분-전체 계층이다. 우리는 테스트 스위트의 스위트의 스위트를 지원하고 싶다.

컴포지트는 다음 참여자를 도입한다.

- Component: 테스트와 상호작용하는 데 사용할 인터페이스를 선언한다.
- Composite: 이 인터페이스를 구현하고 테스트 컬렉션을 유지한다.
- Leaf: Component 인터페이스를 따르는, 조합 내의 테스트 케이스를 나타낸다.

이 패턴은 단일 객체와 복합 객체의 공통 인터페이스를 정의하는 추상 클래스를 도입하라고 말한다. 이 클래스의 주된 목적은 인터페이스를 정의하는 것이다. Java에서 컴포지트를 적용할 때 우리는 추상 클래스가 아닌 인터페이스를 정의하는 것을 선호한다. 인터페이스를 사용하면 JUnit이 테스트를 위한 특정 기반 클래스에 묶이지 않는다. 테스트가 이 인터페이스를 따르기만 하면 된다. 그래서 패턴 설명을 조금 비틀어 Test 인터페이스를 도입한다.

```java
public interface Test {
    public abstract void run(TestResult result);
}
```

TestCase는 컴포지트의 Leaf에 해당하며, 앞서 본 것처럼 이 인터페이스를 구현한다.

다음으로 Composite 참여자를 도입한다. 클래스 이름은 TestSuite로 한다. TestSuite는 자식 테스트들을 Vector에 보관한다.

```java
public class TestSuite implements Test {
    private Vector fTests= new Vector();
}
```

run() 메서드는 자식들에게 위임(delegate)한다.

```java
public void run(TestResult result) {
    for (Enumeration e= fTests.elements(); e.hasMoreElements(); ) {
        Test test= (Test)e.nextElement();
        test.run(result);
    }
}
```

![그림 5 TestSuite에 Composite 적용](https://curlunit.sourceforge.net/doc/cookstour/Image5.gif)

**그림 5** TestSuite에 Composite 적용

마지막으로 클라이언트가 스위트에 테스트를 추가할 수 있어야 한다. addTest 메서드로 할 수 있다.

```java
public void addTest(Test test) {
    fTests.addElement(test);
}
```

위 코드가 모두 Test 인터페이스에만 의존한다는 점에 주목하라. TestCase와 TestSuite가 모두 Test 인터페이스를 따르므로 테스트 스위트들의 스위트를 재귀적으로 구성할 수 있다. 모든 개발자가 자신만의 TestSuite를 만들 수 있다. 그 스위트들로 구성된 TestSuite를 만들면 전부를 한꺼번에 실행할 수 있다.

다음은 TestSuite를 만드는 예시다.

```java
public static Test suite() {
    TestSuite suite= new TestSuite();
    suite.addTest(new MoneyTest("testMoneyEquals"));
    suite.addTest(new MoneyTest("testSimpleAdd"));
}
```

잘 동작하지만 모든 테스트를 스위트에 수동으로 추가해야 한다. JUnit 초기 사용자들은 이게 바보 같다고 말했다. 새 테스트 케이스를 작성할 때마다 정적 suite() 메서드에 추가하는 것을 기억해야 하고, 그렇지 않으면 실행되지 않는다. 그래서 테스트 케이스 클래스를 인자로 받는 편의 생성자(convenience constructor)를 TestSuite에 추가했다. 이 생성자의 목적은 테스트 메서드를 추출해 그것들을 담은 스위트를 만드는 것이다. 테스트 메서드는 "test" 접두사로 시작하고 인자를 받지 않는다는 단순한 규약(convention)을 따라야 한다. 편의 생성자는 이 규약을 이용해 리플렉션으로 테스트 메서드를 찾아 테스트 객체를 생성한다. 이 생성자를 사용하면 위 코드는 다음과 같이 단순해진다.

```java
public static Test suite() {
    return new TestSuite(MoneyTest.class);
}
```

원래 방식은 테스트 케이스의 일부만 실행하고 싶을 때 여전히 유용하다.

### 3.6 요약 (Summary)

JUnit 쿡스 투어의 끝에 도달했다. 다음 그림은 패턴으로 설명한 JUnit의 설계를 한눈에 보여준다.

![그림 6 JUnit 패턴 요약](https://curlunit.sourceforge.net/doc/cookstour/Image6.gif)

**그림 6** JUnit 패턴 요약

프레임워크의 핵심 추상화(central abstraction)인 TestCase가 네 개의 패턴에 관여한다는 점에 주목하라. 성숙한 객체 설계의 그림에서는 이와 같은 "패턴 밀도(pattern density)"가 나타난다. 설계의 주인공은 조연들과 풍부한 관계를 맺는다.

JUnit의 모든 패턴을 바라보는 또 다른 방법이 있다. 이 스토리보드(storyboard)에서는 각 패턴의 효과를 차례로 추상적으로 표현한 것을 볼 수 있다. 커맨드 패턴이 TestCase 클래스를 만들고, 템플릿 메서드 패턴이 run 메서드를 만드는 식이다. (스토리보드의 표기법은 그림 6의 표기법에서 모든 텍스트를 지운 것이다.)

![그림 7 JUnit 패턴 스토리보드](https://curlunit.sourceforge.net/doc/cookstour/Image7.gif)

**그림 7** JUnit 패턴 스토리보드

스토리보드에서 주목할 점은 컴포지트를 적용할 때 그림의 복잡도가 급격히 뛴다는 것이다. 이는 컴포지트가 강력한 패턴이지만 "그림을 복잡하게 만든다"는 우리의 직관을 시각적으로 뒷받침한다. 따라서 신중하게 사용해야 한다.

## 4. 결론 (Conclusion)

마지막으로 몇 가지 일반적인 관찰을 정리해 보자.

- *패턴 (Patterns)* —  설계를 패턴으로 논의하는 것은 프레임워크를 개발할 때나 다른 사람에게 설명하려 할 때나 모두 매우 귀중했다. 이제 당신은 패턴으로 프레임워크를 설명하는 것이 효과적인지 판단하기에 완벽한 위치에 있다. 위 논의가 마음에 들었다면 당신의 시스템에도 같은 방식의 설명을 시도해 보라.
- *패턴 밀도 (Pattern density)* —  JUnit의 핵심 추상화인 TestCase 주변에는 패턴 "밀도"가 높다. 패턴 밀도가 높은 설계는 사용하기는 쉽지만 변경하기는 어렵다. 우리는 핵심 추상화 주변의 이런 높은 패턴 밀도가 성숙한 프레임워크에서 흔하다는 것을 발견했다. 미성숙한 프레임워크는 그 반대여야 한다. 즉 패턴 밀도가 낮아야 한다. 실제로 풀고 있는 문제가 무엇인지 발견하고 나면, 해결책을 "압축(compress)"하기 시작할 수 있고, 그러면 패턴이 지렛대(leverage) 역할을 하는 곳에서 점점 더 밀도 높은 패턴의 장(field)이 만들어진다.
- *자기가 만든 개밥 먹기 (Eat your own dog food)* —  기본 단위 테스트 기능을 구현하자마자 우리는 그것을 직접 적용했다. TestTest는 프레임워크가 오류, 성공, 실패에 대해 올바른 결과를 보고하는지 검증한다. 프레임워크 설계를 계속 발전시키는 동안 이것은 매우 귀중했다. JUnit을 적용하기 가장 어려웠던 대상은 JUnit 자신의 동작을 테스트하는 것이었다.
- *합집합이 아니라 교집합 (Intersection, not union)* —  프레임워크 개발에는 넣을 수 있는 모든 기능을 넣고 싶은 유혹이 있다. 결국 프레임워크를 최대한 가치 있게 만들고 싶으니까. 하지만 반대 방향의 힘이 있다. 개발자가 당신의 프레임워크를 사용하기로 결정해야 한다는 것이다. 프레임워크의 기능이 적을수록 배우기 쉽고, 개발자가 사용할 가능성이 커진다. JUnit은 이런 방식으로 작성되었다. 테스트 실행에 절대적으로 필요한 기능, 즉 테스트 스위트 실행, 테스트 실행 간의 격리(isolating), 테스트 자동 실행만 구현한다. 물론 몇 가지 기능을 추가하고 싶은 유혹을 참지 못했지만, 그것들은 별도의 확장 패키지(test.extensions)에 신중하게 넣었다. 이 패키지의 주목할 만한 멤버로, 테스트 전후에 추가 코드를 실행할 수 있게 해주는 TestDecorator가 있다.
- *프레임워크 작성자는 자기 코드를 읽는다 (Framework writers read their code)* —  우리는 JUnit 코드를 작성하는 데보다 읽는 데 훨씬 더 많은 시간을 썼고, 새 기능을 추가하는 데 쓴 시간만큼이나 중복된 기능을 제거하는 데 시간을 썼다. 새 클래스를 추가하고 책임(responsibility)을 상상할 수 있는 온갖 방식으로 옮겨 보며 설계를 공격적으로 실험했다. 그 편집증(monomania)에 대한 보상으로 우리는 JUnit, 테스트, 객체 설계, 프레임워크 개발에 대한 통찰과 추가 글을 쓸 기회를 끊임없이 얻었다(그리고 지금도 얻고 있다).

JUnit 최신 버전은 ftp://www.armaties.com/D/home/armaties/ftp/TestingFramework/JUnit/ 에서 내려받을 수 있다.

## 5. 감사의 글 (Acknowledgements)

꼼꼼히 읽고 친절하게 교정해 준 John Vlissides, Ralph Johnson, Nick Edgar에게 감사드린다.

