# Boris Cherny의 Claude Code 사용 설정 가이드
https://x.com/bcherny/status/2007179832300581177  

저는 Boris이고 Claude Code를 만들었습니다. 많은 분들이 제가 Claude Code를 어떻게 사용하는지 물어보셔서, 제 설정을 조금 자랑해 보려고 합니다.

제 설정은 놀라울 정도로 평범할(vanilla) 수 있습니다! Claude Code는 기본 상태로도 훌륭하게 작동하기 때문에 저는 개인적으로 커스터마이징을 많이 하지 않습니다. Claude Code를 사용하는 데 정해진 정답은 없습니다. 우리는 의도적으로 여러분이 원하는 대로 사용하고, 수정하고, 해킹할 수 있도록 만들었습니다. Claude Code 팀의 각 팀원들도 매우 다르게 사용하고 있습니다.

자, 시작해 보겠습니다.

1. 터미널 병렬 실행
   저는 터미널에서 5개의 Claude를 병렬로 실행합니다. 탭 번호를 1-5로 매기고, Claude가 입력을 필요로 할 때 알 수 있도록 시스템 알림을 사용합니다. https://code.claude.com/docs/en/terminal-config#iterm-2-system-notifications

2. 웹과 로컬의 연동
   로컬 Claude와 병행하여 http://claude.ai/code 에서도 5-10개의 Claude를 실행합니다. 터미널에서 코딩하다가 종종 로컬 세션을 웹으로 넘기거나(& 사용), 크롬에서 수동으로 세션을 시작하기도 하고, 때로는 --teleport를 사용하여 이리저리 오갑니다. 또한 매일 아침과 일과 중에 폰(Claude iOS 앱)으로 몇 개의 세션을 시작해 두고 나중에 확인하기도 합니다.

3. 모델 선택: Opus 4.5
   저는 모든 작업에 Opus 4.5 with thinking을 사용합니다. 제가 써본 코딩 모델 중 최고입니다. Sonnet보다 크고 느리지만, 덜 지시해도 되고(steer it less) 도구 사용 능력이 뛰어나기 때문에, 결과적으로는 작은 모델을 사용하는 것보다 거의 항상 더 빠릅니다.

4. 팀 공유 설정 (CLAUDE.md)
   우리 팀은 Claude Code 리포지토리를 위해 하나의 http://CLAUDE.md를 공유합니다. 이를 Git에 체크인하고 팀 전체가 일주일에 여러 번 기여합니다. Claude가 뭔가 잘못하는 것을 볼 때마다 http://CLAUDE.md에 내용을 추가해서 다음번에는 그렇게 하지 않도록 합니다.

다른 팀들은 각자의 http://CLAUDE.md를 관리합니다. 최신 상태로 유지하는 것은 각 팀의 업무입니다.

5. 코드 리뷰와 자동화
   코드 리뷰 중에 동료의 PR(Pull Request)에 @claude를 태그하여 PR의 일부로 http://CLAUDE.md에 내용을 추가하도록 종종 요청합니다. 우리는 이를 위해 Claude Code Github Action(/install-github-action)을 사용합니다. 이것은 우리 식의 Compounding Engineering(@danshipper)입니다.

6. 계획 모드 (Plan Mode)
   대부분의 세션은 Plan 모드(shift+tab 두 번)에서 시작합니다. 제 목표가 PR을 작성하는 것이라면, Plan 모드를 사용하여 제가 계획이 마음에 들 때까지 Claude와 대화를 주고받습니다. 그 후 자동 수락(auto-accept edits) 모드로 전환하면 Claude가 보통 한 번에(1-shot) 처리해 냅니다. 좋은 계획이 정말 중요합니다!

7. 슬래시 커맨드 (/slash commands)
   하루에 여러 번 수행하게 되는 모든 "내부 루프(inner loop)" 워크플로우에는 슬래시 커맨드를 사용합니다. 이렇게 하면 반복적인 프롬프트 작성을 줄일 수 있고, Claude도 이 워크플로우를 사용할 수 있게 됩니다. 커맨드들은 Git에 체크인되며 .claude/commands/에 저장됩니다.

예를 들어, Claude와 저는 매일 수십 번씩 /commit-push-pr 슬래시 커맨드를 사용합니다. 이 커맨드는 인라인 bash를 사용하여 git status와 기타 몇 가지 정보를 미리 계산함으로써 커맨드가 빨리 실행되게 하고 모델과의 불필요한 대화를 피합니다. https://code.claude.com/docs/en/slash-commands#bash-command-execution

8. 서브 에이전트 (Subagents)
   저는 몇 가지 서브 에이전트를 정기적으로 사용합니다. Claude가 작업을 마친 후 코드를 단순화해 주는 code-simplifier, Claude Code를 엔드 투 엔드로 테스트하기 위한 자세한 지침이 있는 verify-app 등이 있습니다. 슬래시 커맨드와 마찬가지로, 저는 서브 에이전트를 대부분의 PR에서 수행하는 가장 일반적인 워크플로우를 자동화하는 것으로 생각합니다. https://code.claude.com/docs/en/sub-agents

9. 포맷팅 훅 (PostToolUse Hook)
   우리는 Claude의 코드를 포맷팅하기 위해 PostToolUse 훅을 사용합니다. Claude는 기본적으로도 코드를 잘 포맷팅하지만, 이 훅이 마지막 10%를 처리하여 나중에 CI에서 포맷팅 오류가 발생하는 것을 방지합니다.

10. 권한 관리
    저는 --dangerously-skip-permissions를 사용하지 않습니다. 대신, /permissions를 사용하여 제 환경에서 안전하다고 알고 있는 일반적인 bash 명령어들을 미리 허용해 둠으로써 불필요한 권한 프롬프트를 피합니다. 이 설정의 대부분은 .claude/settings.json에 체크인되어 팀과 공유됩니다.

11. 외부 도구 연동 (MCP)
    Claude Code는 저를 위해 제 모든 도구를 사용합니다. (MCP 서버를 통해) Slack을 검색하거나 포스팅하고, (bq CLI를 사용하여) 분석 질문에 답하기 위해 BigQuery 쿼리를 실행하며, Sentry에서 에러 로그를 가져오는 등의 작업을 수행합니다. Slack MCP 설정은 .mcp.json에 체크인되어 팀과 공유됩니다.

12. 장시간 작업 처리
    매우 오래 걸리는 작업의 경우, 저는 (a) Claude에게 작업이 완료되면 백그라운드 에이전트와 함께 작업을 검증하도록 프롬프트하거나, (b) 에이전트 Stop 훅을 사용하여 더 결정론적으로 수행하거나, (c) ralph-wiggum 플러그인(@GeoffreyHuntley이 처음 구상함)을 사용합니다. 또한 샌드박스 환경에서 --permission-mode=dontAsk나 --dangerously-skip-permissions를 사용하여 세션 동안 권한 프롬프트가 뜨지 않게 함으로써, 제가 없어도 Claude가 멈추지 않고 계속 작업(cook)할 수 있게 합니다.

https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum

https://code.claude.com/docs/en/hooks-guide

13. 가장 중요한 팁: 검증 (Verification)
    마지막 팁이자 아마도 Claude Code로 훌륭한 결과를 얻는 가장 중요한 것입니다. Claude에게 작업을 검증할 방법을 제공하세요. Claude가 그런 피드백 루프를 갖게 되면, 최종 결과물의 품질이 2-3배 높아집니다.

Claude는 제가 http://claude.ai/code에 반영하는 모든 변경 사항을 Claude Chrome 확장 프로그램을 사용하여 테스트합니다. 브라우저를 열고, UI를 테스트하고, 코드가 작동하고 UX가 좋다고 느껴질 때까지 반복합니다.

검증은 도메인마다 다르게 보일 수 있습니다. 간단히 bash 명령어를 실행하는 것일 수도 있고, 테스트 스위트를 돌리거나, 브라우저나 폰 시뮬레이터에서 앱을 테스트하는 것일 수도 있습니다. 이 부분을 견고하게 만드는 데 투자하십시오. https://code.claude.com/docs/en/chrome

이 내용이 도움이 되었기를 바랍니다! 여러분의 Claude Code 사용 팁은 무엇인가요? 다음에는 어떤 내용을 듣고 싶으신가요?