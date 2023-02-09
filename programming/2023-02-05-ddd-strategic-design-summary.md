# 도메인 주도 설계(DDD) - 4부 전략적 설계 정리
에릭 에반스가 [직접 요약한 DDD문서](https://domainlanguage.com/wp-content/uploads/2016/05/DDD_Reference_2015-03.pdf)도 있다.

## 전략적 설계의 3가지 주제 
전략적 설계를 위한 3가지 주제(컨텍스트, 디스틸레이션, 대규모구조)는 여러가지 하위 항목(기법)을 가지고 있다.  
  
아래 내용은 내 나름대로 읽고 배운 것을 짧게 정리한 것이다. 나의 무지와 경험부족으로 잘 못 정리되어 있을 수 있다.

### 14. 모델의 무결성 유지(CONTEXT)
팀(BOUNDED CONTEXT)과 팀이 잘 협업하기 위한 기법들.
* BOUNDED CONTEXT: 의사소통하는 개인들의 집합(팀)으로 경계를 만들어라.
* CONTINUOUS INTEGRATION: 자동화된 테스트와 함께 모든 코드와 그 밖의 구현 산출물을 빈번하게 병합하는 프로세스를 수립하라.
* CONTEXT MAP: BOUNDED CONTEXT간의 관계를 설명하라.
* SHARED KERNEL: 두 컨텍스트 간에 공유하기로 한 코드의 부분집합을 명시하고 각별히 관리하라.  
* CUSTOMER/SUPPLIER DEVELOPMENT TEAM: 클라이언트와 서버를 구분하고 클라이언트 → 서버 단방향의존 하라.  
* CONFORMIST: 서버의 인터페이스를 미리 약속하고 변경하지마라.  
* ANTICORRUPTION LAYER: 다른 시스템을 직접의존하지 말고, 계층을 두어 격리하라.  
* SEPARATE WAYS: 반드시 통합되야 하는 것은 아니니, 다른 컨텍스트와 관계를 끊어라.  
* OPEN HOST SERVICE: 각 클라이언트 맞춤 인터페이스를 제공하지말고, 공통 인터페이스로 단순화해라.  
* PUBLISHED LANGUAGE: 컨텍스트간에 공통 언어를 사용해라.  

### 15. 디스틸레이션(distillation: 증류)
도메인 모델의 정수를 추출하는 기법들.
* CORE DOMAIN: 가장 가치 있고 전문화된 개념을 찾아 구분하고 부각시켜라.  
* GENERIC SUBDOMAIN: 일반적/부수적인/덜중요한 도메인을 core에서 분리하라.  
* DOMAIN VISION STATEMENT: core domain을 그것이 가져올 가치와 함께 짧게 기술하라.  
* HIGHLIGHTED CORE: DVS의 이해를 돕기위해 3~7page 분량의 문서를 작성하라.  
* COHESIVE MECHANISM: domain은 무엇(인터페이스)을 표현하는데 집중하고, 어떻게(구현)를 분리하라.  
* SEGREGATED CORE: core domain에서 지원요소(덜 핵심)를 찾고 분리하여, 응집력을 높여라.  
* ABSTRACT CORE: core domain에서 공통 인터페이스를 표현할 수 있는 경우, 다형성을 이용해 단순화해라.  

### 16. 대규모구조(Large-scale structure)
넓은 시각으로 시스템에 관해 토의하고 이해하게끔 돕는 기법들.  
대규모구조는 선택사항이다.
* EVOLVING ORDER: 설계가 애플리케이션과 함께 발전/변화할 수 있게 하라. 세부설계과 모델의 변화를 과도하게 제약말라.  
* SYSTEM METAPHOR: 팀원들의 이해를 돕는 비유가 나타나면, 공통언어로 삼아 일관성을 증진하라.  
* RESPONSIBILITY LAYER: 경험을 통해, 도메인 요소를 서로 다른 책임으로 구분할 수 있다면, 그에 맞게 설계를 변경하라.  
* KNOWLEDGE LEVEL: 문제를 단순화하기 위해, 객체를 속성과 행동에 따라 구분(타입)하라.  
* PLUGGABLE COMPONENT FRAMEWORK: 잘 정제된 core domain은 추상화를 통해 다양한 구현을 대체할 수 있다.

### 17. 전략의 종합
위 세 개 장의 원칙과 기법을 적재적소에 조합해야 한다.
다음 6가지가 필수적이다.
* 의사결정은 팀 전체에 퍼져야한다.
* 의사결정 프로세스는 피드백을 흡수해야 한다.
* 계획은 발전을 감안해야한다.
* 아키텍처 팀에서 가장 뛰어나고 똑똑한 사람들을 모두 데려가서는 안 된다.
* 전략적 설계에는 최소주의와 겸손이 필요하다.
* 객체는 전문가, 개발자는 다방면에 지식이 풍부한 사람.
  
  
그 외에 전략은 
* 개발팀에서 창발
* 아키텍트도 개발팀 중심
* 기술 프레임워크가 방해하지 말것
* 종합계획 조심
  
xp의 가치(의사소통, 단순성, 피드백, 용기, 존중)가 생각난다.

    
다시한번 위 내용들은 많이 요약했고, 잘 못 이해해서 틀린 부분이 있을 수 있다.


