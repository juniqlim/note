#!/bin/bash
# 매일 보유 종목 뉴스 체크 자동화
# launchd에서 매일 09:00에 실행

set -euo pipefail

# 네트워크 연결 대기 (최대 60초)
for i in $(seq 1 12); do
  curl -s --max-time 3 https://api.anthropic.com > /dev/null && break
  sleep 5
done

NEWS_DIR="/Users/juniq/develop/code/juniqlim/note/investment/daily-news"
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="${NEWS_DIR}/${TODAY}.md"

mkdir -p "$NEWS_DIR"

# Claude Code CLI로 뉴스 검색 실행 (stdin으로 프롬프트 전달)
# atomic write: 임시파일에 쓰고 성공시에만 교체 (실패해도 기존 파일 보존)
TMP_OUTPUT="${OUTPUT_FILE}.tmp"
cat <<PROMPT | /Users/juniq/.local/bin/claude -p \
  --allowedTools "WebSearch Read Glob" \
  > "$TMP_OUTPUT" 2>>"${NEWS_DIR}/error.log"
오늘은 ${TODAY}이다. /Users/juniq/develop/code/juniqlim/note/investment/daily-news-check.md 의 종목 리스트에 있는 각 종목에 대해 어제와 오늘 투자에 영향을 줄 수 있는 뉴스를 검색해줘.

검색 방법:
1. 각 종목별로 "종목명 news today" 또는 "종목명 뉴스 오늘" 형태로 검색해.
2. 추가로 "major corporate news today bonds M&A SEC regulation" 그리고 "오늘 주요 기업 뉴스 채권 인수합병 규제" 로 포괄 검색을 1회씩 해서, 종목 리스트에 해당하는 뉴스가 있으면 해당 종목에 추가해.
3. 테마별로 아래 키워드로 추가 검색해서, 보유 종목에 영향을 줄 수 있는 산업 전체 뉴스를 찾아:
   - AI: "AI semiconductor HBM news today" / "AI 반도체 HBM 뉴스 오늘"
   - K-Beauty: "K-Beauty cosmetics export news today" / "K뷰티 화장품 수출 뉴스 오늘"
   - OTT: "streaming OTT industry news today" / "OTT 스트리밍 뉴스 오늘"
   - K-Food: "K-Food ramen export news today" / "K푸드 라면 수출 뉴스 오늘"

출력 형식:
1. 가장 상단에 "## 진짜 알아야됨" 섹션을 만들어. 여기에는 전 종목 뉴스 중에서 매수/매도 판단에 직접 영향을 주는 것만 넣어. 기준: 실적 서프라이즈/미스, 규제/법적 리스크, M&A, 대규모 자금조달(채권발행 등), 대규모 투자 변경, 경영권 이슈, 목표가 대폭 변경. 해당 없으면 "오늘은 없음"으로 표시.
2. 그 아래에 테마별로 묶어서 정리해. 각 테마 섹션 상단에 "### 테마 동향"으로 산업 전체 뉴스를 먼저 넣고, 그 아래에 개별 종목 뉴스를 정리해. 뉴스가 없으면 특이사항 없음으로 표시해.
마크다운 형식으로 출력해.
PROMPT

# atomic write 마무리: 비어있지 않을 때만 실제 파일로 교체
if [ -s "$TMP_OUTPUT" ]; then
  mv "$TMP_OUTPUT" "$OUTPUT_FILE"
else
  rm -f "$TMP_OUTPUT"
  echo "[$(date)] daily-news 생성 실패 (빈 출력) — push 건너뜀" >> "${NEWS_DIR}/error.log"
fi

# git 단계는 별도 claude -p에 위임
# - autostash로 사용자 unstaged 변경 보존
# - rebase 자동 머지 가능하면 진행, 충돌이 사람 판단을 요구하면 abort 후 알림
cd /Users/juniq/develop/code/juniqlim/note
GIT_TARGET="investment/daily-news/${TODAY}.md"
GIT_MSG="daily-news: ${TODAY}"
cat <<GITPROMPT | /Users/juniq/.local/bin/claude -p \
  --allowedTools "Bash(git:*)" \
  >> "${NEWS_DIR}/error.log" 2>&1
다음 git 작업을 수행해. 작업 디렉토리는 /Users/juniq/develop/code/juniqlim/note 이다.

1. \`${GIT_TARGET}\` 파일을 stage하고 "${GIT_MSG}" 메시지로 커밋해. 변경이 없으면 커밋은 건너뛰어.
2. \`git pull --rebase --autostash origin master\` 로 원격을 당겨와.
3. rebase 도중 충돌이 발생하면:
   a. 충돌이 같은 줄을 양쪽에서 다르게 수정한 "사람 판단이 필요한" 충돌이면 \`git rebase --abort\` 하고 종료해. push 시도하지 마.
   b. 한 쪽만 변경된 add/add 또는 modify/delete 같은 명백한 케이스면 자동으로 해결하고 \`git rebase --continue\`로 진행해.
4. rebase 끝나면 \`git push origin master\` 해.
5. 모든 단계의 결과를 한 줄씩 stdout에 적어줘. 실패하면 어디서 왜 실패했는지 명시해.

위험한 명령 금지: --force, --force-with-lease, reset --hard, push -f, branch -D 등은 절대 쓰지 마.
GITPROMPT

# 일주일치 쌓이면 weekly 생성
DOW=$(date +%u)  # 1=월 ... 7=일
if [ "$DOW" -eq 7 ]; then
  WEEK_START=$(date -v-6d +%Y-%m-%d)
  WEEK_END="${TODAY}"
  WEEKLY_FILE="${NEWS_DIR}/weekly-${WEEK_START}_${WEEK_END}.md"

  # 해당 주의 daily 파일 목록
  DAILY_FILES=""
  for i in $(seq 0 6); do
    DAY=$(date -v-${i}d +%Y-%m-%d)
    F="${NEWS_DIR}/${DAY}.md"
    [ -f "$F" ] && DAILY_FILES="${F} ${DAILY_FILES}"
  done

  if [ -n "$DAILY_FILES" ]; then
    # 각 daily 파일 내용을 합쳐서 Claude에게 weekly 생성 요청
    {
      echo "아래는 ${WEEK_START} ~ ${WEEK_END} 일주일간의 일일 투자 뉴스입니다."
      echo "이 내용을 바탕으로 주간 투자 뉴스 요약을 만들어줘."
      echo ""
      echo "규칙:"
      echo "1. 중복 뉴스는 제거하고, 가장 최신/완전한 버전만 남겨."
      echo "2. 진짜 중요한 내용(실적 서프라이즈/미스, 규제 리스크, M&A, 대규모 자금조달, 목표가 대폭 변경)은 **굵게** 강조해."
      echo "3. 주간 동안 진행 상황이 있는 이슈는 타임라인으로 정리해."
      echo "4. 형식: '## 진짜 알아야됨' 섹션을 맨 위에, 그 아래 테마별로 정리."
      echo "5. 각 종목별로 한 주간 주가 변동률이 있으면 포함해."
      echo "6. '특이사항 없음'인 종목은 생략해."
      echo ""
      for f in $DAILY_FILES; do
        echo "=== $(basename "$f" .md) ==="
        cat "$f"
        echo ""
      done
    } | /Users/juniq/.local/bin/claude -p \
        --allowedTools "Read Glob" \
        > "${WEEKLY_FILE}.tmp" 2>>"${NEWS_DIR}/error.log"

    if [ -s "${WEEKLY_FILE}.tmp" ]; then
      mv "${WEEKLY_FILE}.tmp" "$WEEKLY_FILE"

      # weekly git 단계도 동일하게 위임
      WEEKLY_TARGET="investment/daily-news/weekly-${WEEK_START}_${WEEK_END}.md"
      WEEKLY_MSG="weekly-news: ${WEEK_START} ~ ${WEEK_END}"
      cat <<GITPROMPT | /Users/juniq/.local/bin/claude -p \
        --allowedTools "Bash(git:*)" \
        >> "${NEWS_DIR}/error.log" 2>&1
다음 git 작업을 수행해. 작업 디렉토리는 /Users/juniq/develop/code/juniqlim/note 이다.

1. \`${WEEKLY_TARGET}\` 파일을 stage하고 "${WEEKLY_MSG}" 메시지로 커밋해. 변경이 없으면 커밋은 건너뛰어.
2. \`git pull --rebase --autostash origin master\` 로 원격을 당겨와.
3. rebase 충돌이 사람 판단을 요구하는 경우(같은 줄을 양쪽이 다르게 수정)면 \`git rebase --abort\` 후 종료. 명백한 케이스면 자동 해결 후 \`git rebase --continue\`.
4. \`git push origin master\` 해.
5. 결과를 stdout에 한 줄씩 적어. --force류 위험 명령은 금지.
GITPROMPT
    else
      rm -f "${WEEKLY_FILE}.tmp"
      echo "[$(date)] weekly 생성 실패 (빈 출력) — push 건너뜀" >> "${NEWS_DIR}/error.log"
    fi
  fi
fi

# macOS 알림 (클릭하면 파일 열림)
NOTIF_MSG="${TODAY} 뉴스 확인하기"
[ "$DOW" -eq 7 ] && NOTIF_MSG="${TODAY} 뉴스 + 주간 요약 확인하기"
/opt/homebrew/bin/terminal-notifier \
  -title "투자 뉴스 체크 완료" \
  -message "$NOTIF_MSG" \
  -open "file://${OUTPUT_FILE}" \
  -sound default

# 사용자가 안 쓰고 있을 때만 다시 잠자기
if /usr/sbin/ioreg -c AppleBacklightDisplay | grep -q '"DisplayIsOn"=0'; then
  pmset sleepnow
fi
