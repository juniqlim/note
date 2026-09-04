# Best Practices for Claude Code
https://code.claude.com/docs/en/best-practices  

> **문서 인덱스**
>
> 전체 문서 인덱스 가져오기: https://code.claude.com/docs/llms.txt
>
> 더 자세히 살펴보기 전에 이 파일을 사용하여 사용 가능한 모든 페이지를 확인하세요.

> **소개**
>
> 환경 설정부터 병렬 세션을 통한 확장까지, Claude Code를 최대한 활용하기 위한 팁과 패턴을 소개합니다.

Claude Code는 에이전트형 코딩 환경입니다. 질문에 답하고 기다리는 챗봇과 달리, Claude Code는 파일을 읽고, 명령어를 실행하고, 변경 사항을 만들고, 사용자가 지켜보거나 방향을 제시하거나 완전히 자리를 비운 사이에도 자율적으로 문제를 해결할 수 있습니다.

이는 작업 방식을 변화시킵니다. 직접 코드를 작성하고 Claude에게 검토를 요청하는 대신, 원하는 바를 설명하면 Claude가 이를 구축하는 방법을 알아냅니다. Claude는 탐색하고, 계획하고, 구현합니다.

하지만 이러한 자율성에는 학습 곡선이 따릅니다. Claude는 사용자가 이해해야 할 특정 제약 조건 내에서 작동합니다.

이 가이드는 Anthropic 내부 팀들과 다양한 코드베이스, 언어, 환경에서 Claude Code를 사용하는 엔지니어들에게 효과적인 것으로 입증된 패턴들을 다룹니다. 에이전트 루프가 내부적으로 어떻게 작동하는지 보려면 [Claude Code 작동 방식](/en/how-claude-code-works)을 참조하세요.

---

대부분의 모범 사례는 하나의 제약 조건을 기반으로 합니다: **Claude의 컨텍스트 윈도우(context window)는 빠르게 채워지며, 채워질수록 성능이 저하된다는 것입니다.**

Claude의 컨텍스트 윈도우는 모든 메시지, Claude가 읽은 모든 파일, 모든 명령어 출력을 포함한 전체 대화를 담습니다. 하지만 이는 빠르게 찰 수 있습니다. 단일 디버깅 세션이나 코드베이스 탐색만으로도 수만 개의 토큰이 생성되고 소비될 수 있습니다.

컨텍스트가 채워질수록 LLM 성능이 저하되기 때문에 이는 중요합니다. 컨텍스트 윈도우가 거의 꽉 차면 Claude는 이전 지시 사항을 "잊어버리거나" 더 많은 실수를 할 수 있습니다. 컨텍스트 윈도우는 관리해야 할 가장 중요한 자원입니다. 토큰 사용량을 줄이는 자세한 전략은 [토큰 사용량 줄이기](/en/costs#reduce-token-usage)를 참조하세요.

---

## Claude가 작업을 스스로 검증할 수 있게 하세요

> 💡 **Tip**
>
> 테스트, 스크린샷 또는 예상 출력을 포함하여 Claude가 스스로 확인할 수 있게 하세요. 이것이 여러분이 할 수 있는 가장 효과적인 단일 조치입니다.

Claude는 테스트 실행, 스크린샷 비교, 출력 검증 등 자신의 작업을 직접 확인할 수 있을 때 훨씬 더 나은 성능을 발휘합니다.

명확한 성공 기준이 없다면, 겉보기엔 맞아 보이지만 실제로는 작동하지 않는 결과물을 만들 수 있습니다. 그러면 사용자가 유일한 피드백 루프가 되며, 모든 실수마다 사용자의 주의가 필요하게 됩니다.

| 전략 | 이전 (Before) | 이후 (After) |
| :--- | :--- | :--- |
| **검증 기준 제공** | *"이메일 주소를 검증하는 함수를 구현해"* | *"validateEmail 함수를 작성해. 예시 테스트 케이스: `user@example.com`은 true, invalid는 false, `user@.com`은 false여야 함. 구현 후 테스트를 실행해."* |
| **UI 변경 사항 시각적 검증** | *"대시보드를 더 보기 좋게 만들어"* | *"\[스크린샷 붙여넣기] 이 디자인을 구현해. 결과물의 스크린샷을 찍어 원본과 비교해. 차이점을 나열하고 수정해."* |
| **증상이 아닌 근본 원인 해결** | *"빌드가 실패했어"* | *"이 오류로 빌드가 실패함: \[오류 붙여넣기]. 이를 수정하고 빌드가 성공하는지 검증해. 오류를 억제하지 말고 근본 원인을 해결해."* |

UI 변경 사항은 [Claude in Chrome 확장 프로그램](/en/chrome)을 사용하여 검증할 수 있습니다. 브라우저를 열고 UI를 테스트하며 코드가 작동할 때까지 반복합니다.

검증 수단은 테스트 스위트, 린터(linter), 또는 출력을 확인하는 Bash 명령어가 될 수도 있습니다. 검증 과정을 견고하게 만드는 데 투자하세요.

---

## 먼저 탐색하고, 계획한 다음, 코딩하세요

> 💡 **Tip**
>
> 엉뚱한 문제를 해결하는 것을 방지하기 위해 조사 및 계획 단계를 구현 단계와 분리하세요.

Claude가 바로 코딩에 뛰어들게 하면 잘못된 문제를 해결하는 코드를 생성할 수 있습니다. [계획 모드(Plan Mode)](/en/common-workflows#use-plan-mode-for-safe-code-analysis)를 사용하여 탐색과 실행을 분리하세요.

권장되는 워크플로우는 4단계입니다:

### 1. 탐색 (Explore)
계획 모드로 진입합니다. Claude는 변경 사항을 만들지 않고 파일을 읽고 질문에 답합니다.

```text
read /src/auth and understand how we handle sessions and login.
also look at how we manage environment variables for secrets.
```
*(해석: /src/auth를 읽고 세션과 로그인을 어떻게 처리하는지 파악해. 또한 비밀 환경 변수를 어떻게 관리하는지도 살펴봐.)*

### 2. 계획 (Plan)
Claude에게 상세한 구현 계획을 세우도록 요청합니다.

```text
I want to add Google OAuth. What files need to change?
What's the session flow? Create a plan.
```
*(해석: 구글 OAuth를 추가하고 싶어. 어떤 파일들을 변경해야 해? 세션 흐름은 어떻게 돼? 계획을 세워줘.)*

### 3. 구현 (Implement)
일반 모드(Normal Mode)로 전환하여 Claude가 계획에 따라 코딩하고 검증하게 합니다.

```text
implement the OAuth flow from your plan. write tests for the
callback handler, run the test suite and fix any failures.
```
*(해석: 계획에 따라 OAuth 흐름을 구현해. 콜백 핸들러에 대한 테스트를 작성하고, 테스트 스위트를 실행한 뒤 실패하는 부분을 수정해.)*

### 4. 커밋 (Commit)
Claude에게 설명이 포함된 메시지로 커밋하고 PR을 생성하도록 요청합니다.

```text
commit with a descriptive message and open a PR
```
*(해석: 설명이 포함된 메시지로 커밋하고 PR을 열어줘.)*

> **참고 (Callout)**
>
> 계획 모드는 유용하지만 오버헤드도 추가됩니다.
>
> 범위가 명확하고 수정 사항이 작은 작업(예: 오타 수정, 로그 라인 추가, 변수 이름 변경)의 경우 Claude에게 바로 수행하도록 요청하세요.
>
> 계획은 접근 방식이 불확실하거나, 변경 사항이 여러 파일을 수정하거나, 수정하려는 코드에 익숙하지 않을 때 가장 유용합니다. 변경 사항(diff)을 한 문장으로 설명할 수 있다면 계획 단계를 건너뛰세요.

---

## 프롬프트에 구체적인 컨텍스트 제공하기

> 💡 **Tip**
>
> 지시가 정확할수록 수정이 줄어듭니다.

Claude는 의도를 추론할 수 있지만 독심술을 할 수는 없습니다. 구체적인 파일을 참조하고, 제약 조건을 언급하고, 예시 패턴을 가리키세요.

| 전략 | 이전 (Before) | 이후 (After) |
| :--- | :--- | :--- |
| **작업 범위 지정.**<br>어떤 파일, 어떤 시나리오, 테스트 선호도를 명시하세요. | *"foo.py에 테스트 추가해"* | *"사용자가 로그아웃된 엣지 케이스를 다루는 foo.py 테스트를 작성해. mock 사용은 피해줘."* |
| **소스 지정.**<br>질문에 답할 수 있는 소스로 Claude를 안내하세요. | *"ExecutionFactory API는 왜 이렇게 이상해?"* | *"ExecutionFactory의 git 기록을 살펴보고 이 API가 어떻게 생겨났는지 요약해줘."* |
| **기존 패턴 참조.**<br>코드베이스 내의 패턴을 가리키세요. | *"달력 위젯 추가해"* | *"홈 페이지에 기존 위젯들이 어떻게 구현되어 있는지 살펴보고 패턴을 파악해. `HotDogWidget.php`가 좋은 예시야. 이 패턴을 따르면서 사용자가 월을 선택하고 앞뒤로 넘기며 연도를 고를 수 있는 새 달력 위젯을 구현해. 코드베이스에 이미 사용된 라이브러리 외에는 사용하지 말고 처음부터 만들어."* |
| **증상 설명.**<br>증상, 예상 위치, "수정됨"의 정의를 제공하세요. | *"로그인 버그 고쳐"* | *"세션 타임아웃 후 로그인이 실패한다는 사용자 보고가 있어. `src/auth/`의 인증 흐름, 특히 토큰 갱신 부분을 확인해. 문제를 재현하는 실패 테스트를 작성한 다음 수정해."* |

막연한 프롬프트는 탐색 중이거나 수정 과정을 감당할 수 있을 때 유용할 수 있습니다. `"이 파일에서 무엇을 개선하겠어?"`와 같은 프롬프트는 생각지도 못한 개선점을 발견하게 해 줄 수 있습니다.

### 풍부한 콘텐츠 제공

> 💡 **Tip**
>
> `@`를 사용하여 파일을 참조하거나, 스크린샷/이미지를 붙여넣거나, 데이터를 파이프(`|`)로 직접 전달하세요.

여러 가지 방법으로 Claude에게 풍부한 데이터를 제공할 수 있습니다:

* **코드가 있는 위치를 설명하는 대신 `@`로 파일 참조**: Claude는 응답하기 전에 파일을 읽습니다.
* **이미지 직접 붙여넣기**: 이미지를 복사/붙여넣기 하거나 프롬프트로 드래그 앤 드롭하세요.
* **문서 및 API 참조를 위한 URL 제공**: `/permissions`를 사용하여 자주 사용하는 도메인을 허용 목록에 추가하세요.
* **데이터 파이핑**: `cat error.log | claude`와 같이 실행하여 파일 내용을 직접 전송하세요.
* **필요한 정보 가져오게 하기**: Claude에게 Bash 명령어나 MCP 도구를 사용하거나 파일을 읽어서 컨텍스트를 직접 가져오라고 지시하세요.

---

## 환경 구성하기

몇 가지 설정 단계를 거치면 모든 세션에서 Claude Code가 훨씬 더 효과적으로 작동합니다. 확장 기능에 대한 전체 개요와 사용 시점은 [Claude Code 확장하기](/en/features-overview)를 참조하세요.

### 효과적인 CLAUDE.md 작성

> 💡 **Tip**
>
> `/init`을 실행하여 현재 프로젝트 구조를 기반으로 초기 `CLAUDE.md` 파일을 생성한 다음, 시간이 지남에 따라 다듬으세요.

`CLAUDE.md`는 Claude가 모든 대화 시작 시 읽는 특수 파일입니다. Bash 명령어, 코드 스타일, 워크플로우 규칙을 포함하세요. 이는 **코드만으로는 추론할 수 없는** 지속적인 컨텍스트를 제공합니다.

`/init` 명령어는 코드베이스를 분석하여 빌드 시스템, 테스트 프레임워크, 코드 패턴을 감지하고, 이를 다듬을 수 있는 견고한 기초를 제공합니다.

`CLAUDE.md` 파일에 정해진 형식은 없지만, 짧고 사람이 읽기 쉽게 유지하세요. 예:

```markdown
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

`CLAUDE.md`는 매 세션마다 로드되므로 광범위하게 적용되는 내용만 포함하세요. 가끔씩만 관련된 도메인 지식이나 워크플로우는 대신 [스킬(skills)](/en/skills)을 사용하세요. 스킬은 모든 대화를 부풀리지 않고 필요할 때 로드됩니다.

간결하게 유지하세요. 각 줄마다 *"이것을 제거하면 Claude가 실수를 할까?"*라고 자문해 보세요. 그렇지 않다면 삭제하세요. 비대한 `CLAUDE.md` 파일은 Claude가 실제 지시 사항을 무시하게 만듭니다!

| ✅ 포함 (Include) | ❌ 제외 (Exclude) |
| :--- | :--- |
| Claude가 추측할 수 없는 Bash 명령어 | Claude가 코드를 읽어서 알아낼 수 있는 것 |
| 기본값과 다른 코드 스타일 규칙 | Claude가 이미 알고 있는 표준 언어 관습 |
| 테스트 지침 및 선호하는 테스트 러너 | 상세한 API 문서 (대신 문서 링크 제공) |
| 리포지토리 에티켓 (브랜치 명명, PR 규칙) | 자주 변경되는 정보 |
| 프로젝트에 특화된 아키텍처 결정 사항 | 긴 설명이나 튜토리얼 |
| 개발자 환경 특이사항 (필수 환경 변수) | 코드베이스의 파일별 설명 |
| 흔한 함정이나 명백하지 않은 동작 | "깨끗한 코드를 작성해라"와 같은 자명한 관행 |

금지 규칙이 있음에도 Claude가 원하지 않는 행동을 계속한다면, 파일이 너무 길어서 규칙이 묻히고 있을 가능성이 큽니다. `CLAUDE.md`에 답이 있는 질문을 Claude가 한다면 표현이 모호할 수 있습니다. `CLAUDE.md`를 코드처럼 다루세요: 문제가 생기면 검토하고, 정기적으로 정리하고, Claude의 행동이 실제로 변하는지 관찰하여 변경 사항을 테스트하세요.

강조(예: "IMPORTANT" 또는 "YOU MUST")를 추가하여 준수율을 높일 수 있습니다. 팀원들이 기여할 수 있도록 `CLAUDE.md`를 git에 체크인하세요. 이 파일의 가치는 시간이 지날수록 커집니다.

`CLAUDE.md` 파일은 `@path/to/import` 구문을 사용하여 추가 파일을 가져올 수 있습니다:

```markdown
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

`CLAUDE.md` 파일은 여러 위치에 둘 수 있습니다:

* **홈 폴더 (`~/.claude/CLAUDE.md`)**: 모든 Claude 세션에 적용
* **프로젝트 루트 (`./CLAUDE.md`)**: 팀과 공유하기 위해 git에 체크인하거나, `CLAUDE.local.md`로 이름 짓고 `.gitignore`에 추가
* **상위 디렉토리**: 모노레포에서 유용하며 `root/CLAUDE.md`와 `root/foo/CLAUDE.md`가 모두 자동으로 가져와짐
* **하위 디렉토리**: 해당 디렉토리의 파일로 작업할 때 Claude가 하위 `CLAUDE.md` 파일을 필요에 따라 가져옴

### 권한 구성

> 💡 **Tip**
>
> `/permissions`를 사용하여 안전한 명령어를 허용 목록에 추가하거나 `/sandbox`를 사용하여 OS 수준의 격리를 사용하세요. 이렇게 하면 통제권을 유지하면서 중단을 줄일 수 있습니다.

기본적으로 Claude Code는 시스템을 수정할 수 있는 작업(파일 쓰기, Bash 명령어, MCP 도구 등)에 대해 권한을 요청합니다. 이는 안전하지만 지루합니다. 열 번째 승인 후에는 제대로 검토하지 않고 그냥 클릭하게 됩니다. 이러한 중단을 줄이는 두 가지 방법이 있습니다:

* **권한 허용 목록(Permission allowlists)**: 안전하다고 알고 있는 특정 도구 허용 (예: `npm run lint` 또는 `git commit`)
* **샌드박싱(Sandboxing)**: 파일 시스템 및 네트워크 액세스를 제한하는 OS 수준 격리를 활성화하여 Claude가 정의된 경계 내에서 더 자유롭게 작업하도록 허용

또는 린트 오류 수정이나 상용구(boilerplate) 생성과 같이 격리된 워크플로우의 경우 `--dangerously-skip-permissions`를 사용하여 모든 권한 확인을 우회할 수 있습니다.

> ⚠️ **Warning**
>
> Claude가 임의의 명령어를 실행하게 하면 데이터 손실, 시스템 손상 또는 프롬프트 주입을 통한 데이터 유출이 발생할 수 있습니다. `--dangerously-skip-permissions`는 인터넷 액세스가 없는 샌드박스 환경에서만 사용하세요.

[권한 구성](/en/settings) 및 [샌드박싱 활성화](/en/sandboxing#sandboxing)에 대해 자세히 알아보세요.

### CLI 도구 사용

> 💡 **Tip**
>
> 외부 서비스와 상호 작용할 때 Claude Code에게 `gh`, `aws`, `gcloud`, `sentry-cli`와 같은 CLI 도구를 사용하도록 지시하세요.

CLI 도구는 외부 서비스와 상호 작용하는 가장 컨텍스트 효율적인 방법입니다. GitHub를 사용하는 경우 `gh` CLI를 설치하세요. Claude는 이를 사용하여 이슈 생성, PR 열기, 댓글 읽기 등을 수행하는 방법을 알고 있습니다. `gh`가 없어도 Claude는 GitHub API를 사용할 수 있지만, 인증되지 않은 요청은 속도 제한에 걸리기 쉽습니다.

Claude는 아직 모르는 CLI 도구를 배우는 데에도 효과적입니다. `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`(foo 도구에 대해 배우기 위해 help 명령어를 사용하고, A, B, C를 해결하는 데 사용해)와 같은 프롬프트를 시도해 보세요.

### MCP 서버 연결

> 💡 **Tip**
>
> `claude mcp add`를 실행하여 Notion, Figma 또는 데이터베이스와 같은 외부 도구를 연결하세요.

[MCP 서버](/en/mcp)를 사용하면 Claude에게 이슈 트래커의 기능을 구현하거나, 데이터베이스를 쿼리하거나, 모니터링 데이터를 분석하거나, Figma의 디자인을 통합하고, 워크플로우를 자동화하도록 요청할 수 있습니다.

### 훅(Hooks) 설정

> 💡 **Tip**
>
> 예외 없이 매번 발생해야 하는 작업에는 훅을 사용하세요.

[훅](/en/hooks-guide)은 Claude 워크플로우의 특정 지점에서 스크립트를 자동으로 실행합니다. 권고 사항인 `CLAUDE.md` 지침과 달리 훅은 결정적이며 작업 실행을 보장합니다.

Claude가 훅을 대신 작성해 줄 수 있습니다. *"모든 파일 편집 후에 eslint를 실행하는 훅을 작성해"* 또는 *"migrations 폴더에 쓰는 것을 차단하는 훅을 작성해"*와 같은 프롬프트를 사용해 보세요. 대화형 구성을 위해 `/hooks`를 실행하거나 `.claude/settings.json`을 직접 편집하세요.

### 스킬(Skills) 생성

> 💡 **Tip**
>
> `.claude/skills/`에 `SKILL.md` 파일을 생성하여 Claude에게 도메인 지식과 재사용 가능한 워크플로우를 제공하세요.

[스킬](/en/skills)은 프로젝트, 팀 또는 도메인에 특화된 정보로 Claude의 지식을 확장합니다. Claude는 관련이 있을 때 자동으로 적용하거나 `/skill-name`으로 직접 호출할 수 있습니다.

`.claude/skills/`에 `SKILL.md`가 포함된 디렉토리를 추가하여 스킬을 생성하세요:

```markdown
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

스킬은 직접 호출할 수 있는 반복 가능한 워크플로우를 정의할 수도 있습니다:

```markdown
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

`/fix-issue 1234`를 실행하여 호출합니다. 수동으로 트리거하려는 부작용(side effects)이 있는 워크플로우에는 `disable-model-invocation: true`를 사용하세요.

### 커스텀 서브 에이전트 생성

> 💡 **Tip**
>
> `.claude/agents/`에 Claude가 격리된 작업을 위임할 수 있는 전문 어시스턴트를 정의하세요.

[서브 에이전트](/en/sub-agents)는 허용된 도구 세트를 가지고 고유한 컨텍스트에서 실행됩니다. 많은 파일을 읽거나 메인 대화를 어지럽히지 않고 전문적인 집중이 필요한 작업에 유용합니다.

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Claude에게 명시적으로 서브 에이전트를 사용하라고 지시하세요: *"이 코드를 보안 문제에 대해 검토하기 위해 서브 에이전트를 사용해."*

### 플러그인 설치

> 💡 **Tip**
>
> `/plugin`을 실행하여 마켓플레이스를 둘러보세요. 플러그인은 구성 없이 스킬, 훅, 서브 에이전트 및 MCP 서버를 추가합니다.

[플러그인](/en/plugins)은 커뮤니티와 Anthropic에서 제공하는 스킬, 훅, 서브 에이전트 및 MCP 서버를 설치 가능한 단일 단위로 묶습니다. 타입이 있는 언어로 작업하는 경우, [코드 인텔리전스 플러그인](/en/discover-plugins#code-intelligence)을 설치하여 Claude에게 정밀한 심볼 탐색과 편집 후 자동 오류 감지 기능을 제공하세요.

스킬, 서브 에이전트, 훅, MCP 중에서 선택하는 방법은 [Claude Code 확장하기](/en/features-overview#match-features-to-your-goal)를 참조하세요.

---

## 효과적으로 소통하기

Claude Code와 소통하는 방식은 결과물의 품질에 큰 영향을 미칩니다.

### 코드베이스 관련 질문하기

> 💡 **Tip**
>
> 시니어 엔지니어에게 물어볼 만한 질문을 Claude에게 하세요.

새로운 코드베이스에 온보딩할 때 학습 및 탐색을 위해 Claude Code를 사용하세요. 다른 엔지니어에게 물어볼 법한 질문들을 Claude에게 할 수 있습니다:

* 로깅은 어떻게 작동해?
* 새 API 엔드포인트는 어떻게 만들어?
* `foo.rs`의 134번째 줄에 있는 `async move { ... }`는 무슨 역할을 해?
* `CustomerOnboardingFlowImpl`은 어떤 엣지 케이스들을 처리해?
* 왜 이 코드는 333번째 줄에서 `bar()` 대신 `foo()`를 호출해?

이런 방식으로 Claude Code를 사용하는 것은 효과적인 온보딩 워크플로우이며, 적응 시간을 단축하고 다른 엔지니어들의 부담을 줄여줍니다. 특별한 프롬프트가 필요 없습니다: 직접 질문하세요.

### Claude가 당신을 인터뷰하게 하세요

> 💡 **Tip**
>
> 더 큰 기능의 경우, Claude가 먼저 당신을 인터뷰하게 하세요. 최소한의 프롬프트로 시작하고 `AskUserQuestion` 도구를 사용하여 인터뷰해 달라고 요청하세요.

Claude는 기술적 구현, UI/UX, 엣지 케이스, 트레이드오프 등 당신이 아직 고려하지 않았을 수 있는 사항들에 대해 질문합니다.

```text
[간단한 설명]을 만들고 싶어. AskUserQuestion 도구를 사용하여 나를 상세히 인터뷰해줘.

기술적 구현, UI/UX, 엣지 케이스, 우려 사항, 트레이드오프에 대해 물어봐. 뻔한 질문은 하지 말고 내가 고려하지 못했을 어려운 부분들을 파고들어.

모든 것을 다룰 때까지 계속 인터뷰하고, 그 후에 SPEC.md에 완전한 스펙을 작성해줘.
```

스펙이 완료되면 새 세션을 시작하여 이를 실행하세요. 새 세션은 구현에만 집중된 깨끗한 컨텍스트를 가지며, 참조할 수 있는 작성된 스펙이 있습니다.

---

## 세션 관리하기

대화는 지속적이며 되돌릴 수 있습니다. 이를 유리하게 활용하세요!

### 조기에 자주 방향 수정하기

> 💡 **Tip**
>
> Claude가 궤도를 벗어나는 것을 알아차리는 즉시 수정하세요.

가장 좋은 결과는 긴밀한 피드백 루프에서 나옵니다. Claude가 가끔 첫 시도에 문제를 완벽하게 해결하기도 하지만, 빠르게 수정해 주는 것이 일반적으로 더 나은 해결책을 더 빨리 만들어냅니다.

* **`Esc`**: `Esc` 키로 작업 중간에 Claude를 멈추세요. 컨텍스트가 보존되므로 방향을 다시 잡을 수 있습니다.
* **`Esc + Esc` 또는 `/rewind`**: `Esc`를 두 번 누르거나 `/rewind`를 실행하여 되감기 메뉴를 열고 이전 대화 및 코드 상태를 복원하세요.
* **`"Undo that"`**: Claude에게 변경 사항을 되돌리라고 하세요.
* **`/clear`**: 관련 없는 작업 사이에는 컨텍스트를 초기화하세요. 관련 없는 컨텍스트가 많은 긴 세션은 성능을 저하시킬 수 있습니다.

한 세션에서 같은 문제에 대해 Claude를 두 번 이상 수정했다면, 컨텍스트는 실패한 접근 방식들로 어수선해진 상태입니다. `/clear`를 실행하고 알게 된 내용을 포함하여 더 구체적인 프롬프트로 새로 시작하세요. 더 나은 프롬프트가 있는 깨끗한 세션이 수정 사항이 누적된 긴 세션보다 거의 항상 더 나은 성과를 냅니다.

### 컨텍스트 적극적으로 관리하기

> 💡 **Tip**
>
> 관련 없는 작업 사이에는 `/clear`를 실행하여 컨텍스트를 초기화하세요.

Claude Code는 컨텍스트 제한에 도달하면 대화 기록을 자동으로 압축하여 중요한 코드와 결정 사항은 보존하면서 공간을 확보합니다.

긴 세션 동안 Claude의 컨텍스트 윈도우는 관련 없는 대화, 파일 내용, 명령어들로 가득 찰 수 있습니다. 이는 성능을 저하시키고 때로는 Claude를 산만하게 할 수 있습니다.

* 작업 간에 `/clear`를 자주 사용하여 컨텍스트 윈도우를 완전히 초기화하세요.
* 자동 압축이 트리거되면 Claude는 코드 패턴, 파일 상태, 주요 결정 사항 등 가장 중요한 내용을 요약합니다.
* 더 많은 제어를 위해 `/compact <지시사항>`을 실행하세요. 예: `/compact API 변경 사항에 집중해`.
* `CLAUDE.md`에서 압축 동작을 사용자 정의하세요. 예: `"압축할 때, 수정된 파일의 전체 목록과 테스트 명령어는 항상 보존해"`라고 하여 중요한 컨텍스트가 요약 과정에서 살아남도록 합니다.

### 조사를 위해 서브 에이전트 사용하기

> 💡 **Tip**
>
> `"서브 에이전트를 사용하여 X를 조사해"`라고 하여 연구를 위임하세요. 서브 에이전트는 별도의 컨텍스트에서 탐색하므로 메인 대화를 구현을 위해 깨끗하게 유지할 수 있습니다.

컨텍스트가 근본적인 제약 조건이므로, 서브 에이전트는 사용할 수 있는 가장 강력한 도구 중 하나입니다. Claude가 코드베이스를 조사할 때 많은 파일을 읽는데, 이 모든 것이 사용자의 컨텍스트를 소비합니다. 서브 에이전트는 별도의 컨텍스트 윈도우에서 실행되고 요약을 보고합니다:

```text
서브 에이전트를 사용하여 우리 인증 시스템이 토큰 갱신을 어떻게 처리하는지,
그리고 재사용할 만한 기존 OAuth 유틸리티가 있는지 조사해.
```

서브 에이전트는 코드베이스를 탐색하고, 관련 파일을 읽고, 결과를 보고합니다. 이 모든 과정이 메인 대화를 어지럽히지 않고 이루어집니다.

Claude가 무언가를 구현한 후 검증을 위해 서브 에이전트를 사용할 수도 있습니다:

```text
서브 에이전트를 사용하여 이 코드를 엣지 케이스에 대해 검토해.
```

### 체크포인트로 되감기

> 💡 **Tip**
>
> Claude가 수행하는 모든 작업은 체크포인트를 생성합니다. 대화, 코드 또는 둘 다를 이전 체크포인트로 복원할 수 있습니다.

Claude는 변경 전에 자동으로 체크포인트를 생성합니다. `Esc`를 두 번 탭하거나 `/rewind`를 실행하여 체크포인트 메뉴를 여세요. 대화만 복원(코드 변경 유지), 코드만 복원(대화 유지), 또는 둘 다 복원할 수 있습니다.

모든 움직임을 신중하게 계획하는 대신, Claude에게 위험한 시도를 해보라고 할 수 있습니다. 작동하지 않으면 되감고 다른 접근 방식을 시도하세요. 체크포인트는 세션 간에도 유지되므로 터미널을 닫았다가 나중에 다시 되감을 수 있습니다.

> ⚠️ **Warning**
>
> 체크포인트는 외부 프로세스가 아닌 *Claude에 의해* 변경된 사항만 추적합니다. 이것은 git을 대체하지 않습니다.

### 대화 재개하기

> 💡 **Tip**
>
> `claude --continue`를 실행하여 중단한 곳에서 다시 시작하거나, `--resume`을 실행하여 최근 세션 중에서 선택하세요.

Claude Code는 대화를 로컬에 저장합니다. 작업이 여러 세션에 걸쳐 있을 때(기능을 시작했다가 중단되고 다음 날 다시 돌아오는 경우) 컨텍스트를 다시 설명할 필요가 없습니다:

```bash
claude --continue    # 가장 최근 대화 재개
claude --resume      # 최근 대화 목록에서 선택
```

`/rename`을 사용하여 세션에 설명적인 이름(`"oauth-migration"`, `"debugging-memory-leak"`)을 붙여 나중에 찾을 수 있게 하세요. 세션을 브랜치처럼 다루세요. 서로 다른 업무 흐름은 별도의 지속적인 컨텍스트를 가질 수 있습니다.

---

## 자동화 및 확장

하나의 Claude를 효과적으로 사용하게 되면, 병렬 세션, 헤드리스 모드, 팬아웃(fan-out) 패턴으로 산출물을 증대시키세요.

지금까지의 내용은 한 명의 사람, 하나의 Claude, 하나의 대화를 가정했습니다. 하지만 Claude Code는 수평적으로 확장됩니다. 이 섹션의 기술들은 더 많은 일을 처리하는 방법을 보여줍니다.

### 헤드리스 모드 실행

> 💡 **Tip**
>
> CI, pre-commit 훅 또는 스크립트에서 `claude -p "prompt"`를 사용하세요. 스트리밍 JSON 출력을 위해 `--output-format stream-json`을 추가하세요.

`claude -p "your prompt"`를 사용하면 대화형 세션 없이 헤드리스로 Claude를 실행할 수 있습니다. 헤드리스 모드는 Claude를 CI 파이프라인, pre-commit 훅 또는 자동화된 워크플로우에 통합하는 방법입니다. 출력 형식(일반 텍스트, JSON, 스트리밍 JSON)을 통해 결과를 프로그래밍 방식으로 파싱할 수 있습니다.

```bash
# 일회성 쿼리
claude -p "이 프로젝트가 무엇을 하는지 설명해"

# 스크립트용 구조화된 출력
claude -p "모든 API 엔드포인트 나열해" --output-format json

# 실시간 처리를 위한 스트리밍
claude -p "이 로그 파일 분석해" --output-format stream-json
```

### 여러 Claude 세션 실행

> 💡 **Tip**
>
> 여러 Claude 세션을 병렬로 실행하여 개발 속도를 높이고, 격리된 실험을 실행하거나, 복잡한 워크플로우를 시작하세요.

병렬 세션을 실행하는 데는 두 가지 주요 방법이 있습니다:

* [Claude Desktop](/en/desktop): 여러 로컬 세션을 시각적으로 관리합니다. 각 세션은 고유한 격리된 작업 트리(worktree)를 가집니다.
* [웹에서의 Claude Code](/en/claude-code-on-the-web): Anthropic의 보안 클라우드 인프라의 격리된 VM에서 실행합니다.

작업 병렬화를 넘어, 다중 세션은 품질 중심의 워크플로우를 가능하게 합니다. 새로운 컨텍스트는 Claude가 방금 작성한 코드에 편향되지 않으므로 코드 리뷰를 개선합니다.

예를 들어, 작성자/검토자 패턴을 사용하세요:

| 세션 A (작성자) | 세션 B (검토자) |
| :--- | :--- |
| `API 엔드포인트를 위한 속도 제한(rate limiter) 구현해` | |
| | `@src/middleware/rateLimiter.ts의 속도 제한 구현을 검토해. 엣지 케이스, 경쟁 상태(race conditions), 그리고 기존 미들웨어 패턴과의 일관성을 찾아봐.` |
| `여기 검토 피드백이 있어: [세션 B 출력]. 이 문제들을 해결해.` | |

테스트에서도 비슷하게 할 수 있습니다. 한 Claude는 테스트를 작성하게 하고, 다른 Claude는 그 테스트를 통과하는 코드를 작성하게 하세요.

### 파일 간 팬아웃(Fan-out)

> 💡 **Tip**
>
> `claude -p`를 호출하여 작업을 반복하세요. `--allowedTools`를 사용하여 일괄 작업을 위한 권한 범위를 지정하세요.

대규모 마이그레이션이나 분석의 경우, 많은 병렬 Claude 호출에 작업을 분산시킬 수 있습니다:

1. **작업 목록 생성**
   Claude에게 마이그레이션이 필요한 모든 파일을 나열하게 합니다 (예: `마이그레이션이 필요한 2,000개의 Python 파일 모두 나열해`)

2. **목록을 반복하는 스크립트 작성**
   ```bash
   for file in $(cat files.txt); do
     claude -p "$file을 React에서 Vue로 마이그레이션해. 성공하면 OK, 실패하면 FAIL 반환." \
       --allowedTools "Edit,Bash(git commit:*)"
   done
   ```

3. **몇 개의 파일에서 테스트 후, 대규모 실행**
   처음 2~3개 파일에서 잘못된 점을 바탕으로 프롬프트를 다듬은 다음, 전체 세트에서 실행하세요. `--allowedTools` 플래그는 Claude가 할 수 있는 일을 제한하며, 이는 무인으로 실행할 때 중요합니다.

기존 데이터/처리 파이프라인에 Claude를 통합할 수도 있습니다:

```bash
claude -p "<your prompt>" --output-format json | your_command
```

개발 중 디버깅을 위해 `--verbose`를 사용하고, 프로덕션에서는 끄세요.

### 안전한 자율 모드

`claude --dangerously-skip-permissions`를 사용하여 모든 권한 확인을 우회하고 Claude가 중단 없이 작업하게 하세요. 이는 린트 오류 수정이나 상용구 코드 생성과 같은 워크플로우에 적합합니다.

> ⚠️ **Warning**
>
> Claude가 임의의 명령어를 실행하게 하는 것은 위험하며 데이터 손실, 시스템 손상 또는 데이터 유출(예: 프롬프트 주입 공격을 통해)을 초래할 수 있습니다. 이러한 위험을 최소화하려면 인터넷 액세스가 없는 컨테이너에서 `--dangerously-skip-permissions`를 사용하세요.
>
> 샌드박싱(`/sandbox`)을 활성화하면 모든 확인을 우회하는 대신 사전에 경계를 정의하여 더 나은 보안과 유사한 자율성을 얻을 수 있습니다.

---

## 흔한 실패 패턴 피하기

다음은 흔한 실수들입니다. 이를 일찍 인식하면 시간을 절약할 수 있습니다:

* **중구난방 세션 (The kitchen sink session)**
  하나의 작업으로 시작했다가, 관련 없는 것을 묻고, 다시 첫 번째 작업으로 돌아갑니다. 컨텍스트는 관련 없는 정보로 가득 찹니다.
  > **해결책**: 관련 없는 작업 사이에는 `/clear`를 하세요.

* **반복적인 수정**
  Claude가 무언가 잘못했고, 당신이 수정했지만 여전히 틀렸고, 다시 수정합니다. 컨텍스트는 실패한 접근 방식들로 오염됩니다.
  > **해결책**: 두 번의 실패한 수정 후에는 `/clear`를 하고 알게 된 내용을 포함하여 더 나은 초기 프롬프트를 작성하세요.

* **지나치게 상세한 CLAUDE.md**
  `CLAUDE.md`가 너무 길면, 중요한 규칙이 노이즈에 묻혀 Claude가 절반을 무시합니다.
  > **해결책**: 가차 없이 정리하세요. Claude가 지시 없이도 이미 올바르게 수행한다면 삭제하거나 훅으로 변환하세요.

* **'일단 믿고 나중에 확인'의 함정**
  Claude는 엣지 케이스를 처리하지 못하는 그럴듯해 보이는 구현을 생성합니다.
  > **해결책**: 항상 검증 수단(테스트, 스크립트, 스크린샷)을 제공하세요. 검증할 수 없다면 배포하지 마세요.

* **무한 탐색**
  범위를 지정하지 않고 Claude에게 무언가를 "조사"하라고 요청합니다. Claude는 수백 개의 파일을 읽어 컨텍스트를 채웁니다.
  > **해결책**: 조사 범위를 좁히거나 탐색이 메인 컨텍스트를 소비하지 않도록 서브 에이전트를 사용하세요.

---

## 직관 기르기

이 가이드의 패턴들은 절대적인 규칙이 아닙니다. 일반적으로 잘 작동하는 시작점일 뿐이며, 모든 상황에 최적이지 않을 수 있습니다.

때로는 하나의 복잡한 문제에 깊이 빠져 있고 기록이 가치 있기 때문에 컨텍스트가 쌓이게 *두어야* 합니다. 때로는 작업이 탐색적이기 때문에 계획을 건너뛰고 Claude가 알아내도록 해야 합니다. 때로는 문제를 제한하기 전에 Claude가 문제를 어떻게 해석하는지 보고 싶어서 모호한 프롬프트가 딱 맞을 수도 있습니다.

무엇이 효과적인지 주의 깊게 살펴보세요. Claude가 훌륭한 결과물을 낼 때, 당신이 무엇을 했는지 주목하세요: 프롬프트 구조, 제공한 컨텍스트, 사용 중이던 모드 등. Claude가 고전할 때는 이유를 물어보세요. 컨텍스트가 너무 시끄러웠나요? 프롬프트가 너무 모호했나요? 작업이 한 번에 처리하기에 너무 컸나요?

## 관련 리소스

* **[Claude Code 작동 방식](/en/how-claude-code-works)**: 에이전트 루프, 도구 및 컨텍스트 관리 이해하기
* **[Claude Code 확장하기](/en/features-overview)**: 스킬, 훅, MCP, 서브 에이전트, 플러그인 중 선택하기
* **[일반적인 워크플로우](/en/common-workflows)**: 디버깅, 테스트, PR 등을 위한 단계별 레시피
* **[CLAUDE.md](/en/memory)**: 프로젝트 컨벤션 및 지속적인 컨텍스트 저장