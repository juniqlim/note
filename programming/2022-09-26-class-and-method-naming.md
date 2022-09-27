# 클래스, 메소드 이름 짓는법
제가 현재 사용하는 클래스/메소드를 네이밍하는 방법을 소개합니다.  
제 방법에 대한 의견/비판 환영합니다!

## 방법
1. 요구사항을 간결히 한다.
2. 요구사항을 템플릿으로 변경한다.
3. 구현한다.

### 요구사항 간추리기
* 50자가 넘지 않는 문장을 사용한다.
* 50자가 넘으면 문장을 나눈다.
* 1문장이 완성되면, 작업을 시작할 수 있다.
* 진행중에 먼저 작업해야할 요구사항(작업사항)이 생기면 그 것부터 한다.

### 템플릿
```java
Result result = new What(input1, input2).action();
```

What은 명사 or 명사구  
action은 동사(return 이 없으면) or 명사(뭔가 return하면)  
Result 명사 or 명사구  
로 하되 간결하게 한다.

## 예시
요구사항
```
쉼표(,) 또는 콜론(:)을 구분자로 가지는 문자열을 전달하는 경우 구분자를 기준으로
분리한 각 숫자의 합을 반환 (예: “” => 0, "1,2" => 3, "1,2,3" => 6, “1,2:3” => 6)

앞의 기본 구분자(쉼표, 콜론)외에 커스텀 구분자를 지정할 수 있다. 커스텀 구분자는
문자열 앞부분의 “//”와 “\n” 사이에 위치하는 문자를 커스텀 구분자로 사용한다. 
예를 들어 “//;\n1;2;3”과 같이 값을 입력할 경우 커스텀 구분자는 세미콜론(;)이며, 결과 값은 6이 반환되어야 한다.
```
### 방법1: 요구사항 간결화
문자열을 구분자(커스텀 가능)로 분리  
분리한 숫자의 합 반환

### 방법2: 템플릿으로 변경
```java
List<Integer> numbers = new SplitedNumbers("1;2;3", ";").value();
int sum = new NumbersSum(numbers).value();
```

### 방법3: 구현
```java
class SplitedNumbersTest {
    @Test
    void test() {
        List<Integer> numbers = new SplitedNumbers("1;2;3", ";").value();
        assertThat(numbers.get(1)).isEqualTo(2);
    }
}

class SplitedNumbers {
    private final String numbers;
    private final String separator;

    SplitedNumbers(String numbers, String Separator) {
        this.numbers = numbers;
        this.separator = Separator;
    }

    List<Integer> value() {
        return Arrays.stream(numbers.split(separator))
            .map(number -> Integer.parseInt(number))
            .collect(Collectors.toList());
    }
}


class NumbersSumTest {
    @Test
    void test() {
        int sum = new NumbersSum(Arrays.asList(1, 2, 3)).value();
        assertThat(sum).isEqualTo(6);
    }
}

class NumbersSum {
    private final List<Integer> numbers;

    public NumbersSum(List<Integer> numbers) {
        this.numbers = numbers;
    }

    int value() {
        return numbers.stream()
            .mapToInt(Integer::intValue)
            .sum();
    }
}
```

## 선언적?
1. 클래스 필드는 모두 final
2. void 메소드 사용금지
를 추가하면 불변객체가 만들어지고, 선언형 프로그래밍에 가까워지는 것 같다.

## 참조
https://www.yegor256.com/2022/06/14/principle-of-one.html
https://www.yegor256.com/2020/03/03/prefixed-naming.html