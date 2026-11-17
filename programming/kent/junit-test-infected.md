# 테스트에 감염되다: 프로그래머는 테스트 작성을 사랑한다 (Test Infected: Programmers Love Writing Tests)
http://members.pingnet.ch/gamma/junit.htm
켄트 벡(Kent Beck)과 에리히 감마(Erich Gamma)가 JUnit으로 테스트를 작성하는 법을 소개한 글을 번역했습니다.

켄트 벡(Kent Beck), CSLife · 에리히 감마(Erich Gamma), OTI Zürich

후속 글: [JUnit 쿡스 투어](junit-cooks-tour.md)

테스트는 개발과 긴밀하게 통합되어 있지 않다. 그래서 개발의 진척을 측정할 수 없다. 무언가가 언제 동작하기 시작했는지, 언제 동작을 멈췄는지 알 수 없다. JUnit을 사용하면 적은 비용으로 점진적으로(incrementally) 테스트 스위트(test suite)를 만들 수 있고, 이 스위트는 진척을 측정하고, 의도치 않은 부작용(side effects)을 발견하고, 개발 노력을 집중하는 데 도움이 된다.

## 문제 (The Problem)

모든 프로그래머는 자기 코드에 테스트를 작성해야 한다는 것을 안다. 하지만 실제로 하는 사람은 드물다. "왜 안 하나요?"라는 질문에 대한 공통된 대답은 "너무 바빠서요"다. 이는 금세 악순환(vicious cycle)이 된다. 압박을 느낄수록 테스트를 덜 작성한다. 테스트를 덜 작성할수록 생산성은 떨어지고 코드는 불안정해진다. 생산성과 정확성이 떨어질수록 더 큰 압박을 느낀다.

프로그래머는 바로 이런 순환 때문에 지쳐 버린다(burn out). 여기서 벗어나려면 외부의 영향이 필요하다. 우리는 필요한 외부의 영향을, 작은 테스트로 큰 차이를 만들어 내는 단순한 테스트 프레임워크에서 찾았다.

직접 테스트를 작성하는 것의 가치를 당신에게 납득시키는 가장 좋은 방법은 당신과 함께 앉아 약간의 개발을 해 보는 것이다. 그 과정에서 새 버그를 만나고, 테스트로 잡고, 고치고, 버그가 다시 나타나면 또 고치는 일을 반복할 것이다. 그러면 직접 단위 테스트(unit tests)를 작성하고, 저장하고, 다시 실행하면서 얻는 즉각적인 피드백(immediate feedback)의 가치를 보게 될 것이다.

안타깝게도 이것은 글이지, 바깥에는 중세 상업의 북적임이 있고 아래층 레코드 가게에서는 테크노 음악이 쿵쿵 울리는, 매력적인 취리히 구시가지를 내려다보는 사무실이 아니다. 그러니 개발 과정을 흉내 내 볼 수밖에 없다. 간단한 프로그램과 그 테스트를 작성하고, 테스트를 실행한 결과를 보여주겠다. 이렇게 하면 우리를 직접 모셔 가는 비용을 치르지 않고도 우리가 사용하고 권하는 과정을 느껴 볼 수 있을 것이다.

## 예제 (Example)

읽는 동안 코드와 테스트가 주고받는 상호작용에 주목하라. 여기서의 방식은 코드 몇 줄을 쓰고 나서 통과해야 할 테스트를 쓰는 것이다. 더 좋은 방식은 통과하지 않을 테스트를 먼저 쓰고, 그다음 그 테스트를 통과시킬 코드를 쓰는 것이다.

우리가 작성할 프로그램은 여러 통화(multiple currencies)로 산술 연산을 표현하는 문제를 푼다. 단일 통화끼리의 산술은 사소하다. 두 금액을 더하기만 하면 된다. 단순한 숫자로 충분하다. 통화가 있다는 사실 자체를 무시해도 된다.

여러 통화가 얽히면 상황이 더 흥미로워진다. 산술을 하려고 한 통화를 다른 통화로 그냥 환산할 수는 없다. 단 하나의 환율(conversion rate)이란 없기 때문이다. 포트폴리오의 가치를 어제 환율과 오늘 환율로 비교해야 할 수도 있다.

간단하게 시작해서, 단일 통화의 값을 나타내는 Money 클래스를 정의하자. 금액은 단순한 int로 나타낸다. 완전한 정확도를 원한다면 임의 정밀도의 부호 있는 십진수를 저장하는 double이나 java.math.BigDecimal을 쓸 것이다. 통화는 ISO 세 글자 약어(USD, CHF 등)를 담은 문자열로 나타낸다. 더 복잡한 구현이라면 통화가 자신만의 객체를 가질 만하다.

```java
class Money {
    private int fAmount;
    private String fCurrency;

    public Money(int amount, String currency) {
        fAmount= amount;
        fCurrency= currency;
    }

    public int amount() {
        return fAmount;
    }

    public String currency() {
        return fCurrency;
    }
}
```

같은 통화의 Money 두 개를 더하면, 결과 Money의 금액은 두 금액의 합이다.

```java
public Money add(Money m) {
    return new Money(amount()+m.amount(), currency());
}
```

이제 계속 코딩만 하는 대신, 즉각적인 피드백을 받으며 "조금 코딩하고, 조금 테스트하고, 조금 코딩하고, 조금 테스트하기(code a little, test a little)"를 실천하고 싶다. 테스트를 구현하는 데에는 JUnit 프레임워크를 사용한다. 테스트를 작성하려면 JUnit 최신판을 받아야 한다(또는 직접 비슷한 것을 만들어도 된다. 그리 많은 일이 아니다).

JUnit은 테스트 케이스를 어떻게 구조화할지 정의하고 테스트를 실행할 도구를 제공한다. 테스트는 TestCase의 서브클래스에서 구현한다. 그래서 Money 구현을 테스트하려고 TestCase의 서브클래스로 MoneyTest를 정의한다. Java에서 클래스는 패키지에 들어가므로 MoneyTest를 어디에 둘지 정해야 한다. 우리가 현재 하는 방식은 MoneyTest를 테스트 대상 클래스와 같은 패키지에 두는 것이다. 이렇게 하면 테스트 케이스가 패키지 전용(package private) 메서드에 접근할 수 있다. 위에서 만든 단순한 버전의 Money.add()를 실행해 볼 테스트 메서드 testSimpleAdd를 추가한다. JUnit 테스트 메서드는 매개변수가 없는 평범한 메서드다.

```java
public class MoneyTest extends TestCase {
    //…
    public void testSimpleAdd() {
        Money m12CHF= new Money(12, "CHF");  // (1)
        Money m14CHF= new Money(14, "CHF");
        Money expected= new Money(26, "CHF");
        Money result= m12CHF.add(m14CHF);    // (2)
        assert(expected.equals(result));     // (3)
    }
}
```

testSimpleAdd() 테스트 케이스는 다음으로 구성된다.

1. 테스트하는 동안 상호작용할 객체를 만드는 코드. 이 테스트 맥락(testing context)을 흔히 테스트의 픽스처(fixture)라고 부른다. testSimpleAdd 테스트에 필요한 것은 Money 객체 몇 개뿐이다.
2. 픽스처의 객체를 실행해 보는(exercise) 코드.
3. 결과를 검증하는 코드.

결과를 검증하기 전에 잠깐 옆길로 새야 한다. 두 Money 객체가 같은지 테스트할 방법이 필요하기 때문이다. 이를 위한 Java 관용구(idiom)는 Object에 정의된 equals 메서드를 오버라이드하는 것이다. equals를 구현하기 전에 MoneyTest에 equals 테스트를 먼저 작성하자.

```java
public void testEquals() {
    Money m12CHF= new Money(12, "CHF");
    Money m14CHF= new Money(14, "CHF");

    assert(!m12CHF.equals(null));
    assert(m12CHF, m12CHF);
    assertEquals(m12CHF, new Money(12, "CHF")); // (1)
    assert(!m12CHF.equals(m14CHF));
}
```

Object의 equals 메서드는 두 객체가 동일한 객체일 때 true를 반환한다. 하지만 Money는 값 객체(value object)다. 두 Money는 통화와 값이 같으면 같다고 간주한다. 이 속성을 테스트하려고, 값은 같지만 동일한 객체는 아닌 Money들이 같은지 검증하는 테스트(1)를 추가했다.

다음으로 Money에 equals 메서드를 작성하자.

```java
public boolean equals(Object anObject) {
    if (! anObject instanceof Money)
        return false;
    Money aMoney= (Money)anObject;
    return aMoney.currency().equals(currency())
        && amount() == aMoney.amount();
}
```

equals는 어떤 종류의 객체든 인자로 받을 수 있으므로, Money로 캐스팅하기 전에 먼저 타입을 확인해야 한다. 여담으로, equals를 오버라이드할 때는 hashCode 메서드도 함께 오버라이드하는 것이 권장되는 관행이다. 하지만 우리는 테스트 케이스로 돌아가고 싶다.

equals 메서드가 생겼으니 testSimpleAdd의 결과를 검증할 수 있다. JUnit에서는 TestCase에서 상속받은 assert를 호출해 검증한다. assert는 인자가 참이 아니면 JUnit이 기록하는 실패(failure)를 일으킨다. 동등성 단언(assertions for equality)은 매우 흔하므로 TestCase는 assertEquals라는 편의 메서드도 정의한다. assertEquals는 equals로 동등성을 검사하는 것에 더해, 두 객체가 다를 경우 두 객체의 출력값을 기록한다. 그래서 JUnit 테스트 결과 보고서에서 테스트가 왜 실패했는지 바로 알 수 있다. 값은 toString 변환 메서드가 만든 문자열 표현으로 기록된다.

테스트 케이스 두 개를 구현하고 나니 테스트를 준비하는(setting-up) 코드에 중복이 보인다. 이 테스트 준비 코드를 재사용할 수 있으면 좋겠다. 다시 말해, 테스트를 실행할 공통 픽스처를 갖고 싶다. JUnit에서는 픽스처의 객체를 TestCase 클래스의 인스턴스 변수에 저장하고 setUp 메서드를 오버라이드해 초기화하면 된다. setUp과 대칭되는 연산은 tearDown이며, 테스트가 끝날 때 테스트 픽스처를 정리하도록 오버라이드할 수 있다. 각 테스트는 자기만의 픽스처에서 실행되고, JUnit은 테스트마다 setUp과 tearDown을 호출하므로 테스트 실행 간에 부작용이 생길 수 없다.

```java
public class MoneyTest extends TestCase {
    private Money f12CHF;
    private Money f14CHF;

    protected void setUp() {
        f12CHF= new Money(12, "CHF");
        f14CHF= new Money(14, "CHF");
    }
}
```

공통 준비 코드를 제거해 두 테스트 케이스 메서드를 다시 쓸 수 있다.

```java
public void testEquals() {
    assert(!f12CHF.equals(null));
    assertEquals(f12CHF, f12CHF);
    assertEquals(m12CHF, new Money(12, "CHF"));
    assert(!f12CHF.equals(f14CHF));
}

public void testSimpleAdd() {
    Money expected= new Money(26, "CHF");
    Money result= f12CHF.add(f14CHF);
    assert(expected.equals(result));
}
```

두 테스트 케이스를 실행하려면 두 단계가 더 필요하다.

1. 개별 테스트 케이스를 실행하는 방법을 정의한다.
2. 테스트 스위트를 실행하는 방법을 정의한다.

JUnit은 단일 테스트를 실행하는 두 가지 방법을 지원한다.

- 정적(static) 방법
- 동적(dynamic) 방법

정적 방법에서는 TestCase에서 상속받은 runTest 메서드를 오버라이드해 원하는 테스트 케이스를 호출한다. 편리한 방법은 익명 내부 클래스(anonymous inner class)를 쓰는 것이다. 테스트가 실패했을 때 식별할 수 있도록 각 테스트에 이름을 주어야 한다는 점에 유의하라.

```java
TestCase test= new MoneyTest("simple add") {
    public void runTest() {
        testSimpleAdd();
    }
};
```

슈퍼클래스의 템플릿 메서드(template method)[1]가 때가 되면 runTest가 실행되도록 보장한다.

실행할 테스트 케이스를 만드는 동적 방법은 리플렉션(reflection)으로 runTest를 구현한다. 테스트의 이름이 호출할 테스트 케이스 메서드의 이름이라고 가정한다. 테스트 메서드를 동적으로 찾아 호출한다. 그래서 testSimpleAdd 테스트를 호출하려면 아래와 같이 MoneyTest를 생성한다.

```java
TestCase = new MoneyTest("testSimpleAdd");
```

동적 방법은 더 간결하게 쓸 수 있지만 정적 타입 안전성(static type safe)이 떨어진다. 테스트 케이스 이름의 오류는 실행해서 NoSuchMethodException을 받기 전까지 드러나지 않는다. 두 방법 모두 장점이 있으므로 어느 쪽을 쓸지는 당신에게 맡기기로 했다.

두 테스트 케이스를 함께 실행하기 위한 마지막 단계로 테스트 스위트를 정의해야 한다. JUnit에서는 suite라는 정적 메서드를 정의해야 한다. suite 메서드는 테스트 실행에 특화된 main 메서드와 같다. suite 안에서 실행할 테스트를 TestSuite 객체에 추가하고 그것을 반환한다. TestSuite는 테스트 모음을 실행할 수 있다. TestSuite와 TestCase는 모두 테스트를 실행하는 메서드를 정의한 Test라는 인터페이스를 구현한다. 그래서 임의의 TestCase와 TestSuite를 조합해 테스트 스위트를 만들 수 있다. 요컨대 TestSuite는 컴포지트(Composite)[1]다. 아래 코드는 테스트를 실행하는 동적 방법으로 테스트 스위트를 만드는 예다.

```java
public static Test suite() {
    TestSuite suite= new TestSuite();
    suite.addTest(new MoneyTest("testMoneyEquals"));
    suite.addTest(new MoneyTest("testSimpleAdd"));
    return suite;
}
```

다음은 정적 방법으로 쓴 같은 코드다.

```java
public static Test suite() {
    TestSuite suite= new TestSuite();
    suite.addTest(
        new MoneyTest("money equals") {
            protected void runTest() { testMoneyEquals(); }
        }
    );

    suite.addTest(
        new MoneyTest("simple add") {
            protected void runTest() { testSimpleAdd(); }
        }
    );
    return suite;
}
```

이제 테스트를 실행할 준비가 되었다. JUnit에는 테스트를 실행하는 그래픽 인터페이스가 딸려 있다. 창 위쪽 입력란에 테스트 클래스 이름을 입력하고 Run 버튼을 누른다. 테스트가 실행되는 동안 JUnit은 입력란 아래 진행 막대(progress bar)로 진행 상황을 보여준다. 막대는 처음에는 초록색이지만 실패한 테스트가 하나라도 생기면 즉시 빨간색으로 바뀐다. 실패한 테스트는 아래쪽 목록에 표시된다. 그림 1은 우리의 사소한 테스트 스위트를 실행한 뒤의 TestRunner 창이다.

**그림 1** 성공한 실행 (원문에 이미지 없음)

단일 통화의 경우가 동작함을 검증했으니 여러 통화로 넘어간다. 앞서 말했듯 서로 다른 통화가 섞인 산술의 문제는 단 하나의 환율이 없다는 것이다. 이 문제를 피하려고 환율 환산을 뒤로 미루는 MoneyBag을 도입한다. 예를 들어 12 스위스 프랑에 14 미국 달러를 더한 것은 12 CHF와 14 USD 두 Money를 담은 가방(bag)으로 표현한다. 여기에 10 스위스 프랑을 더하면 22 CHF와 14 USD를 담은 가방이 된다. 나중에 MoneyBag을 다른 환율로 평가할 수 있다.

MoneyBag은 Money의 리스트로 표현되며, MoneyBag을 만드는 여러 생성자를 제공한다. 생성자들은 패키지 전용이라는 점에 유의하라. MoneyBag은 통화 산술을 할 때 보이지 않는 곳에서 생성되기 때문이다.

```java
class MoneyBag {
    private Vector fMonies= new Vector();

    MoneyBag(Money m1, Money m2) {
        appendMoney(m1);
        appendMoney(m2);
    }

    MoneyBag(Money bag[]) {
        for (int i= 0; i < bag.length; i++)
            appendMoney(bag[i]);
    }
}
```

appendMoney 메서드는 Money를 Money 리스트에 추가하고 같은 통화의 Money를 합치는 일을 맡는 내부 헬퍼 메서드다. MoneyBag에도 equals 메서드와 그에 대응하는 테스트가 필요하다. equals 구현은 건너뛰고 testBagEquals 메서드만 보여주겠다. 먼저 픽스처를 확장해 MoneyBag 두 개를 포함시킨다.

```java
protected void setUp() {
    f12CHF= new Money(12, "CHF");
    f14CHF= new Money(14, "CHF");
    f7USD=  new Money( 7, "USD");
    f21USD= new Money(21, "USD");
    fMB1= new MoneyBag(f12CHF, f7USD);
    fMB2= new MoneyBag(f14CHF, f21USD);
}
```

이 픽스처로 testBagEquals 테스트 케이스는 다음과 같이 된다.

```java
public void testBagEquals() {
    assert(!fMB1.equals(null));
    assertEquals(fMB1, fMB1);
    assert(!fMB1.equals(f12CHF));
    assert(!f12CHF.equals(fMB1));
    assert(!fMB1.equals(fMB2));
}
```

"조금 코딩하고, 조금 테스트하기"에 따라 확장한 테스트를 JUnit으로 실행해 여전히 문제가 없는지 검증한다. MoneyBag이 생겼으니 이제 Money의 add 메서드를 고칠 수 있다.

```java
public Money add(Money m) {
    if (m.currency().equals(currency()) )
        return new Money(amount()+m.amount(), currency());
    return new MoneyBag(this, m);
}
```

위처럼 정의하면 이 메서드는 컴파일되지 않는다. 반환값으로 MoneyBag이 아니라 Money를 기대하기 때문이다. MoneyBag을 도입하면서 이제 Money의 표현이 두 가지가 되었고, 우리는 이를 클라이언트 코드로부터 숨기고 싶다. 그래서 두 표현이 모두 구현하는 IMoney 인터페이스를 도입한다. 다음은 IMoney 인터페이스다.

```java
interface IMoney {
    public abstract IMoney add(IMoney aMoney);
    //…
}
```

서로 다른 표현을 클라이언트로부터 완전히 숨기려면 Money와 MoneyBag의 모든 조합 간 산술을 지원해야 한다. 그래서 코딩을 계속하기 전에 테스트 케이스를 몇 개 더 정의한다. 기대하는 MoneyBag 결과는 앞에서 본, 배열로 MoneyBag을 초기화하는 편의 생성자를 사용한다.

```java
public void testMixedSimpleAdd() {
    // [12 CHF] + [7 USD] == {[12 CHF][7 USD]}
    Money bag[]= { f12CHF, f7USD };
    MoneyBag expected= new MoneyBag(bag);
    assertEquals(expected, f12CHF.add(f7USD));
}
```

나머지 테스트도 같은 패턴을 따른다.

- testBagSimpleAdd — MoneyBag에 단순 Money를 더한다
- testSimpleBagAdd — 단순 Money에 MoneyBag을 더한다
- testBagBagAdd — 두 MoneyBag을 더한다

다음으로 테스트 스위트를 그에 맞게 확장한다.

```java
public static Test suite() {
    TestSuite suite= new TestSuite();
    suite.addTest(new MoneyTest("testMoneyEquals"));
    suite.addTest(new MoneyTest("testBagEquals"));
    suite.addTest(new MoneyTest("testSimpleAdd"));
    suite.addTest(new MoneyTest("testMixedSimpleAdd"));
    suite.addTest(new MoneyTest("testBagSimpleAdd"));
    suite.addTest(new MoneyTest("testSimpleBagAdd"));
    suite.addTest(new MoneyTest("testBagBagAdd"));
    return suite;
}
```

테스트 케이스를 정의했으니 구현을 시작할 수 있다. 여기서 구현의 어려움은 Money와 MoneyBag의 온갖 조합을 다루는 것이다. 이중 디스패치(Double dispatch)[2]는 이 문제를 푸는 우아한 방법이다. 이중 디스패치의 아이디어는 호출을 한 번 더 해서 우리가 다루는 인자의 종류를 알아내는 것이다. 원래 메서드 이름 뒤에 수신자(receiver)의 클래스 이름을 붙인 이름으로 인자의 메서드를 호출한다. Money와 MoneyBag의 add 메서드는 다음과 같이 된다.

```java
class Money implements IMoney {
    public IMoney add(IMoney m) {
        return m.addMoney(this);
    }
    //…
}

class MoneyBag implements IMoney {
    public IMoney MoneyBag.add(IMoney m) {
        return m.addMoneyBag(this);
    }
    //…
}
```

이것이 컴파일되려면 IMoney 인터페이스에 헬퍼 메서드 두 개를 추가해야 한다.

```java
interface IMoney {
//…
    IMoney addMoney(Money aMoney);
    IMoney addMoneyBag(MoneyBag aMoneyBag);
}
```

이중 디스패치 구현을 마무리하려면 Money와 MoneyBag에 이 메서드들을 구현해야 한다. 다음은 Money의 구현이다.

```java
public IMoney addMoney(Money m) {
    if (m.currency().equals(currency()) )
        return new Money(amount()+m.amount(), currency());
    return new MoneyBag(this, m);
}

public IMoney addMoneyBag(MoneyBag s) {
    return s.addMoney(this);
}
```

다음은 MoneyBag의 구현이다. Money와 MoneyBag으로, 그리고 두 MoneyBag으로 MoneyBag을 만드는 생성자가 추가로 있다고 가정한다.

```java
public IMoney addMoney(Money m) {
    return new MoneyBag(m, this);
}

public IMoney addMoneyBag(MoneyBag s) {
    return new MoneyBag(s, this);
}
```

테스트를 실행하면 통과한다. 그런데 구현을 되짚어 보다가 또 다른 흥미로운 경우를 발견한다. 덧셈의 결과로 MoneyBag이 Money 하나만 담은 가방이 되면 어떻게 될까? 예를 들어 7 USD와 12 CHF를 담은 MoneyBag에 -12 CHF를 더하면 7 USD만 담은 가방이 된다. 당연히 그런 가방은 7 USD짜리 단일 Money와 같아야 한다. 문제를 확인하려고 테스트 케이스를 구현해 실행해 보자.

```java
public void testSimplify() {
    // {[12 CHF][7 USD]} + [-12 CHF] == [7 USD]
    Money expected= new Money(7, "USD");
    assertEquals(expected, fMS1.add(new Money(-12, "CHF")));
}
```

이런 방식으로 개발하다 보면, 어떤 생각이 떠올랐을 때 곧장 코드로 가기보다 바로 테스트 작성으로 향하는 일이 잦아진다.

당연하게도 테스트 실행은 실패를 나타내는 빨간 진행 막대로 끝난다. 그래서 MoneyBag의 코드를 고쳐 초록 상태로 돌아간다.

```java
public IMoney addMoney(Money m) {
    return (new MoneyBag(m, this)).simplify();
}

public IMoney addMoneyBag(MoneyBag s) {
    return (new MoneyBag(s, this)).simplify();
}

private IMoney simplify() {
    if (fMonies.size() == 1)
        return (IMoney)fMonies.firstElement()
    return this;
}
```

이제 테스트를 다시 실행하면, 짜잔(voila), 초록색이 된다.

위 코드는 다중 통화 산술 문제의 작은 부분만 해결한다. 서로 다른 환율, 출력 형식, 다른 산술 연산을 표현해야 하고, 이 모두를 적당한 속도로 해내야 한다. 하지만 나머지 객체들도 한 번에 테스트 하나씩, 즉 조금 테스트하고, 조금 코딩하고, 조금 테스트하고, 조금 코딩하는 식으로 개발할 수 있다는 것을 알게 되었기를 바란다.

특히 위의 개발 과정에서 다음을 되짚어 보라.

- 첫 테스트 testSimpleAdd를 add()를 작성한 직후에 바로 작성했다. 일반적으로 개발하면서 테스트를 조금씩 작성하면 개발이 훨씬 순조롭다. 코딩하는 바로 그 순간에 당신은 그 코드가 어떻게 동작할지 상상하고 있다. 그때가 생각을 테스트로 붙잡아 두기에 완벽한 시점이다.
- 공통 setUp 코드를 도입하자마자 기존 테스트 testSimpleAdd와 testEqual을 리팩토링했다. 테스트 코드도 모델 코드와 마찬가지로 잘 정리(factored)되어 있을 때 가장 잘 동작한다. 같은 테스트 코드가 두 곳에 있는 것을 보면, 한 곳에만 나타나도록 리팩토링할 방법을 찾아라.
- suite 메서드를 만들고, 이중 디스패치를 적용할 때 확장했다. 오래된 테스트를 계속 통과시키는 것은 새 테스트를 통과시키는 것만큼 중요하다. 이상적인 것은 항상 모든 테스트를 실행하는 것이다. 한 시간에 열 번씩 하기에는 너무 느릴 때도 있을 것이다. 적어도 하루에 한 번은 모든 테스트를 실행하라.
- 원소가 하나뿐인 MoneyBag은 그 원소를 그대로 반환해야 한다는 요구사항이 떠오르자마자 새 테스트를 만들었다. 이렇게 기어를 바꾸는 법을 익히기는 어려울 수 있지만, 우리는 그것이 가치 있다는 것을 알게 되었다. 시스템이 무엇을 해야 하는지에 대한 아이디어가 떠오르면 구현에 대한 생각은 미뤄라. 대신 먼저 테스트를 작성하라. 그다음 실행하라(혹시 모른다, 이미 동작할 수도 있다). 그다음 구현을 작업하라.

## 쿡북 (Cookbook)

좋다, 당신은 단위 테스트가 정말 멋진 아이디어라고 완전히 확신하게 되었다. 직접 테스트를 작성하려면 어떻게 해야 할까? 다음은 JUnit으로 테스트를 작성하고 구성할 때 따를 수 있는 단계를 보여주는 짧은 쿡북이다.

- 단순한 테스트 케이스 (Simple Test Case)
- 픽스처 (Fixture)
- 테스트 케이스 (Test Case)
- 스위트 (Suite)
- TestRunner

### 단순한 테스트 케이스 (Simple Test Case)

테스트 코드는 어떻게 작성하는가?

가장 단순한 방법은 디버거의 표현식으로 작성하는 것이다. 디버그 표현식은 재컴파일 없이 바꿀 수 있고, 실행 중인 객체를 보고 나서 무엇을 쓸지 정할 수 있다. 테스트 표현식을 표준 출력 스트림에 출력하는 문장으로 쓸 수도 있다. 두 방식 모두 결과를 분석하는 데 사람의 판단이 필요하다는 한계가 있다. 또한 잘 조합되지 않는다. 디버그 표현식은 한 번에 하나만 실행할 수 있고, print 문이 너무 많은 프로그램은 끔찍한 "스크롤 맹목(Scroll Blindness)"을 일으킨다.

JUnit 테스트는 해석에 사람의 판단이 필요 없고, 여러 개를 동시에 실행하기 쉽다. 무언가를 테스트해야 할 때 할 일은 다음과 같다.

1. TestCase의 인스턴스를 만든다.
2. "runTest()" 메서드를 오버라이드한다.
3. 값을 확인하고 싶을 때 "assert()"를 호출하고, 테스트가 성공하면 참이 되는 boolean을 전달한다.

예를 들어 같은 통화의 두 Money를 더한 결과가 두 Money 값의 합을 담고 있는지 테스트하려면 다음과 같이 쓴다.

```java
public void testSimpleAdd() {
    Money m12CHF= new Money(12, "CHF");
    Money m14CHF= new Money(14, "CHF");
    Money expected= new Money(26, "CHF");
    Money result= m12CHF.add(m14CHF);
    assert(expected.equals(result));
}
```

이미 작성한 테스트와 비슷한 테스트를 쓰고 싶다면 대신 픽스처를 작성하라. 둘 이상의 테스트를 실행하고 싶다면 스위트를 만들어라.

### 픽스처 (Fixture)

같거나 비슷한 객체 집합을 대상으로 동작하는 테스트가 둘 이상이라면 어떻게 할까?

테스트는 알려진 객체 집합을 배경으로 실행되어야 한다. 이 객체 집합을 테스트 픽스처(test fixture)라고 부른다. 테스트를 작성하다 보면 실제로 값을 테스트하는 것보다 픽스처를 준비하는 코드를 작성하는 데 더 많은 시간을 쓴다는 것을 자주 알게 된다.

어느 정도는 생성자를 신경 써서 작성하면 픽스처 코드 작성이 쉬워진다. 하지만 훨씬 큰 절약은 픽스처 코드를 공유하는 데서 온다. 여러 다른 테스트에 같은 픽스처를 사용할 수 있는 경우가 많다. 각 케이스는 픽스처에 조금씩 다른 메시지나 매개변수를 보내고 서로 다른 결과를 확인한다.

공통 픽스처가 있을 때 할 일은 다음과 같다.

1. TestCase의 서브클래스를 만든다.
2. 픽스처의 각 부분마다 인스턴스 변수를 추가한다.
3. "setUp()"을 오버라이드해 변수를 초기화한다.
4. "tearDown()"을 오버라이드해 setUp에서 할당한 영구 자원(permanent resources)을 해제한다.

예를 들어 12 스위스 프랑, 14 스위스 프랑, 28 미국 달러의 여러 조합으로 동작하는 테스트 케이스를 여러 개 작성하려면 먼저 픽스처를 만든다.

```java
public class MoneyTest extends TestCase {
    private Money f12CHF;
    private Money f14CHF;
    private Money f28USD;

    protected void setUp() {
        f12CHF= new Money(12, "CHF");
        f14CHF= new Money(14, "CHF");
        f28USD= new Money(28, "USD");
    }
}
```

픽스처가 갖춰지면 테스트 케이스를 원하는 만큼 작성할 수 있다.

### 테스트 케이스 (Test Case)

픽스처가 있을 때 개별 테스트 케이스는 어떻게 작성하고 호출하는가?

픽스처 없이 테스트 케이스를 작성하는 것은 간단하다. TestCase의 익명 서브클래스에서 runTest()를 오버라이드하면 된다. 픽스처용 테스트 케이스도 같은 방식으로 작성한다. 준비 코드를 위해 TestCase의 서브클래스를 만들고, 개별 테스트 케이스마다 익명 서브클래스를 만든다. 하지만 이런 테스트를 몇 개 작성하고 나면 코드 줄의 상당 부분이 문법(syntax)에 희생된다는 것을 알게 될 것이다.

JUnit은 픽스처에 대한 테스트를 더 간결하게 작성하는 방법을 제공한다. 할 일은 다음과 같다.

1. 픽스처 클래스에 테스트 케이스 메서드를 작성한다. 반드시 public으로 만들어라. 그렇지 않으면 리플렉션으로 호출할 수 없다.
2. TestCase 클래스의 인스턴스를 만들고 테스트 케이스 메서드의 이름을 생성자에 전달한다.

예를 들어 Money와 MoneyBag의 덧셈을 테스트하려면 다음과 같이 쓴다.

```java
public void testMoneyMoneyBag() {
    // [12 CHF] + [14 CHF] + [28 USD] == {[26 CHF][28 USD]}
    Money bag[]= { f26CHF, f28USD };
    MoneyBag expected= new MoneyBag(bag);
    assertEquals(expected, f12CHF.add(f28USD.add(f14CHF)));
}
```

이 테스트 케이스를 실행할 MoneyTest 인스턴스는 다음과 같이 만든다.

```java
new MoneyTest("testMoneyMoneyBag")
```

테스트가 실행될 때 테스트의 이름으로 실행할 메서드를 찾는다.

테스트가 여러 개 생기면 스위트로 정리하라.

### 스위트 (Suite)

여러 테스트를 한 번에 어떻게 실행하는가?

테스트가 두 개만 되어도 함께 실행하고 싶어질 것이다. 테스트를 하나씩 직접 실행할 수도 있지만 금세 지칠 것이다. 대신 JUnit은 TestCase를 몇 개든 함께 실행하는 TestSuite 객체를 제공한다.

예를 들어 테스트 케이스 하나를 실행하려면 다음을 실행한다.

```java
TestResult result= (new MoneyTest("testMoneyMoneyBag")).run();
```

테스트 케이스 두 개로 스위트를 만들어 함께 실행하려면 다음을 실행한다.

```java
TestSuite suite= new TestSuite();
suite.addTest(new MoneyTest("testMoneyEquals"));
suite.addTest(new MoneyTest("testSimpleAdd"));
TestResult result= suite.run();
```

TestSuite가 TestCase만 담을 수 있는 것은 아니다. Test 인터페이스를 구현하는 객체라면 무엇이든 담을 수 있다. 예를 들어 당신이 당신의 코드에 TestSuite를 만들고 내가 내 코드에 하나를 만들면, 둘을 모두 담은 TestSuite를 만들어 함께 실행할 수 있다.

```java
TestSuite suite= new TestSuite();
suite.addTest(Kent.suite());
suite.addTest(Erich.suite());
TestResult result= suite.run();
```

### TestRunner

테스트를 어떻게 실행하고 결과를 수집하는가?

테스트 스위트가 생기면 실행하고 싶을 것이다. JUnit은 실행할 스위트를 정의하고 그 결과를 표시하는 도구를 제공한다. 테스트 스위트를 반환하는 정적 메서드 suite로 스위트를 TestRunner 도구에서 접근할 수 있게 한다. 예를 들어 MoneyTest 스위트를 TestRunner에서 쓸 수 있게 하려면 MoneyTest에 다음 코드를 추가한다.

```java
public static Test suite() {
    TestSuite suite= new TestSuite();
    suite.addTest(new MoneyTest("testMoneyEquals"));
    suite.addTest(new MoneyTest("testSimpleAdd"));
    return suite;
}
```

JUnit은 TestRunner 도구의 그래픽 버전과 텍스트 버전을 모두 제공한다. `java test.ui.TestRunner`를 입력해 시작한다. 그래픽 사용자 인터페이스는 다음을 갖춘 창을 보여준다.

- suite 메서드가 있는 클래스의 이름을 입력하는 입력란
- 테스트를 시작하는 Run 버튼
- 테스트가 실패하면 초록에서 빨강으로 바뀌는 진행 표시기 (원문은 "빨강에서 초록으로(from red to green)"라고 적었지만, 앞의 설명과 맞추면 초록에서 빨강이다)
- 실패한 테스트 목록

테스트가 실패하면 JUnit은 실패한 테스트를 아래쪽 목록에 보고한다. JUnit은 실패(failures)와 오류(errors)를 구분한다. 실패는 예상된 것이며 단언(assertions)으로 검사한다. 오류는 ArrayIndexOutOfBoundsException 같은 예상치 못한 문제다. 그림 2는 실패한 테스트의 예다.

**그림 2** 실패한 실행 (원문에 이미지 없음)

실패나 오류에 대해 더 알고 싶으면 목록에서 선택하고 Show를 누른다. 그러면 실패의 스택 트레이스(stack trace)를 보여준다(그림 3).

**그림 3** 실패 상세 (원문에 이미지 없음)

JUnit 창은 항상 띄워 두어도 된다는 점에 유의하라. 컴파일할 때마다 Run을 누르면 JUnit이 테스트 클래스의 최신 버전을 불러온다.

JUnit에는 배치 인터페이스(batch interface)도 있다. 운영체제 프롬프트에서 `java test.textui.TestRunner` 뒤에 suite 메서드가 있는 클래스 이름을 입력해 사용한다. 배치 인터페이스는 결과를 텍스트로 출력한다. 배치 인터페이스를 호출하는 다른 방법은 TestCase 클래스에 main 메서드를 정의하는 것이다.

예를 들어 MoneyTest용 배치 TestRunner를 시작하려면 다음과 같이 쓴다.

```java
public static void main(String args[]) {
    test.textui.TestRunner.run(suite());
}
```

main을 이렇게 정의하면 운영체제 프롬프트에서 `java MoneyTest`만 입력해도 테스트를 실행할 수 있다.

그래픽 버전이든 텍스트 버전이든 사용하려면 test.jar 파일이 CLASSPATH에 있는지 확인하라.

## 테스트 실천법 (Testing Practices)

마틴 파울러(Martin Fowler)가 이것을 쉽게 만들어 준다. 그는 이렇게 말한다. "print 문이나 디버거 표현식에 무언가를 입력하고 싶어질 때마다, 대신 테스트로 작성하라." 처음에는 늘 새 픽스처를 만들어야 하고 테스트 때문에 조금 느려지는 것 같을 것이다. 하지만 곧 픽스처 라이브러리를 재사용하기 시작할 것이고, 새 테스트는 대개 기존 TestCase 서브클래스에 메서드 하나를 추가하는 것만큼 간단해질 것이다.

테스트는 언제든 더 작성할 수 있다. 하지만 상상할 수 있는 테스트 중 실제로 유용한 것은 일부뿐이라는 것을 금방 알게 될 것이다. 당신이 원하는 것은 동작해야 한다고 생각하는데 실패하는 테스트, 또는 실패해야 한다고 생각하는데 성공하는 테스트다. 비용/편익(cost/benefit)의 관점에서 생각할 수도 있다. 정보로 보답해 줄 테스트를 작성하고 싶은 것이다.

테스트 투자에서 적절한 수익을 얻을 수 있는 때가 몇 가지 있다.

- 개발하는 동안 — 시스템에 새 기능을 추가해야 할 때 테스트를 먼저 작성하라. 그러면 테스트가 통과할 때 개발이 끝난 것이다.
- 디버깅하는 동안 — 누군가 코드에서 결함을 발견하면, 먼저 코드가 동작하면 성공할 테스트를 작성하라. 그다음 그 테스트가 성공할 때까지 디버깅하라.

테스트에 관해 주의할 점 하나. 테스트가 통과하게 되었다면 계속 통과하도록 유지하라. 스위트가 통과하는 상태와 깨진 상태는 하늘과 땅 차이다. 이상적으로는 메서드를 바꿀 때마다 스위트의 모든 테스트를 실행할 것이다. 현실적으로는 스위트가 금방 너무 커져서 항상 다 실행할 수는 없을 것이다. 모든 테스트를 실행할 수 있도록 준비 코드를 최적화하라. 아니면 적어도 현재 개발에 영향을 받을 수 있는 모든 테스트를 담은 특별한 스위트를 만들어라. 그리고 컴파일할 때마다 그 스위트를 실행하라. 그리고 모든 테스트를 적어도 하루에 한 번은 실행하라. 밤사이에, 점심시간에, 그 긴 회의 중 하나가 열리는 동안에….

## 결론 (Conclusion)

이 글은 테스트의 겉만 핥았을 뿐이다. 하지만 놀랍도록 작은 투자로 당신을 더 빠르고, 더 생산적이고, 더 예측 가능하고, 스트레스를 덜 받는 개발자로 만들어 줄 테스트 방식에 초점을 맞췄다.

일단 테스트에 감염되면(test infected) 개발을 대하는 태도가 바뀔 가능성이 크다. 우리가 알아차린 변화는 다음과 같다.

모든 테스트가 올바르게 통과하는 것과 그렇지 않은 것은 하늘과 땅 차이다. 테스트에 감염되었다는 것의 일부는 테스트가 100%가 아니면 집에 갈 수 없다는 것이다. 하지만 스위트를 한 시간에 열 번이나 백 번씩 실행한다면, 저녁 식사에 늦을 만큼 큰 혼란을 만들어 낼 수는 없을 것이다.

특히 처음에는 테스트를 작성하고 싶지 않을 때가 있을 것이다. 그럴 땐 쓰지 마라. 다만 테스트가 없을 때 얼마나 더 곤란해지는지, 디버깅에 얼마나 더 많은 시간을 쓰는지, 얼마나 더 많은 스트레스를 받는지 주의 깊게 보라. 우리는 테스트의 뒷받침을 받을 때 프로그래밍이 얼마나 더 재미있는지, 얼마나 더 과감해질 수 있는지, 스트레스를 얼마나 덜 받는지에 놀랐다. 그 차이가 너무 극적이어서, 쓰고 싶지 않을 때조차 우리는 계속 테스트를 작성한다.

테스트가 생기면 훨씬 더 과감하게 리팩토링할 수 있다. 처음에는 얼마나 많은 것을 할 수 있는지 실감하지 못하겠지만 말이다. "아, 이제 알겠다. 이걸 이러저러하게 설계했어야 했어. 지금은 바꿀 수 없어. 아무것도 망가뜨리고 싶지 않아."라고 말하는 자신을 붙잡아 보라. 그렇게 말할 때 현재 코드의 사본을 저장하고, 정리할 시간을 두어 시간 줘라. (이 부분은 작업하는 동안 동료가 어깨 너머로 봐 줄 때 가장 효과가 좋다.) 계속 테스트를 실행하면서 변경하라. 매 순간 무엇을 망가뜨릴지 걱정하지 않으면 두어 시간 동안 얼마나 많은 일을 해낼 수 있는지 놀랄 것이다.

예를 들어 우리는 MoneyBag의 Vector 기반 구현을 HashTable 기반 구현으로 바꿨다. 기댈 테스트가 아주 많았기 때문에 매우 빠르고 자신 있게 전환할 수 있었다. 테스트가 모두 통과한다면 시스템이 내놓는 답을 전혀 바꾸지 않았다고 확신할 수 있었다.

팀의 다른 사람들도 테스트를 작성하게 하고 싶어질 것이다. 우리가 찾은, 테스트 감염을 퍼뜨리는 가장 좋은 방법은 직접 접촉이다. 다음에 누군가 디버깅을 도와 달라고 하면, 그 문제를 픽스처와 기대 결과의 관점에서 말하게 하라. 그리고 이렇게 말하라. "방금 말해 준 걸 우리가 쓸 수 있는 형태로 적어 보고 싶어요." 당신이 작은 테스트 하나를 쓰는 동안 지켜보게 하라. 실행하라. 고쳐라. 하나 더 써라. 머지않아 그들도 직접 테스트를 쓰고 있을 것이다.

그러니 JUnit을 한번 써 보라. 더 낫게 만든다면 변경 사항을 우리에게 보내 달라. 널리 퍼뜨릴 수 있도록. 다음 글에서는 JUnit 프레임워크 자체를 더블 클릭해 들여다볼 것이다. 어떻게 만들어졌는지 보여주고, 프레임워크 개발에 대한 우리의 철학을 조금 이야기하겠다.

어느 분석가가 바랄 수 있는 만큼이나 훌륭한 프로그래머인 마틴 파울러에게 감사한다. 그는 초기 버전의 JUnit에 시달리면서도 도움이 되는 의견을 주었다.

## 참고 문헌 (References)

1. Gamma, E., et al. Design Patterns: Elements of Reusable Object-Oriented Software, Addison-Wesley, Reading, MA, 1995
2. Beck, K. Smalltalk Best Practice Patterns, Prentice Hall, 1996
