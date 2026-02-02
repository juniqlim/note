# 에이전틱 코딩 잘하기 - 병목을 없애자

## 에이전틱 코딩
에이전틱 코딩(Agentic Coding)은 AI 에이전트가 코드 작성의 주체가 되는 개발 방식이다.  
개발자가 직접 한 줄씩 코드를 타이핑하는(자동완성 보조를 받아) 대신, AI에게 의도와 맥락을 전달하고 AI가 코드를 생성한다.  
개발자는 생성된 코드를 검토하고, 피드백을 주고, 방향을 조정한다.

## 새로운 병목
전통적인 개발에서 병목은 코드 작성이었다. 구현과 테스트 코드를 타이핑하는 데 시간이 걸렸다.  
에이전틱 코딩에선 검증이 병목이다. 테스트, 코드리뷰는 물론 목적이 제대로 달성되었는지 확인하는 시간이 훨씬 오래걸린다.   

## 루프 닫기
이제 코드를 직접 작성하지 않는다고 하는 Peter Steinberger(OpenClaw 개발자)는 [인터뷰](https://github.com/juniqlim/note/blob/master/programming/interview-iship-code-idont-read.md)에서 루프닫기(closing the loop)를 강조한다.  
에이전트가 스스로 디버깅하고 테스트 할 수 있어야 한다. 에이전트에게 자신의 작업을 검증할 방법을 제공해야한다.

마찬가지로 [AI가 자신의 코드 100%를 작성한다](https://x.com/bcherny/status/2015979257038831967)고 말한 Boris Cherny(Claude Code 개발자)도, [X에 자신의 Claude Code 설정](https://github.com/juniqlim/note/blob/master/programming/boris-claude-code-guide.md)을 이야기하며 에이전트에게 검증(Verification)할 방법을 제공하고 피드백 루프를 갖게 하라고 조언한다. 

