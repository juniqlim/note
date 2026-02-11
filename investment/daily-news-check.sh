#!/bin/bash
# 매일 보유 종목 뉴스 체크 자동화
# launchd에서 매일 09:00에 실행

set -euo pipefail

NEWS_DIR="/Users/juniq/develop/code/juniqlim/note/investment/daily-news"
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="${NEWS_DIR}/${TODAY}.md"

mkdir -p "$NEWS_DIR"

# Claude Code CLI로 뉴스 검색 실행 (stdin으로 프롬프트 전달)
cat <<PROMPT | /Users/juniq/.local/bin/claude -p \
  --allowedTools "WebSearch Read Glob" \
  > "$OUTPUT_FILE" 2>>"${NEWS_DIR}/error.log"
오늘은 ${TODAY}이다. /Users/juniq/develop/code/juniqlim/note/investment/daily-news-check.md 의 종목 리스트에 있는 각 종목에 대해 어제와 오늘 투자에 영향을 줄 수 있는 뉴스를 검색해줘.

검색 방법:
1. 각 종목별로 "종목명 news today" 또는 "종목명 뉴스 오늘" 형태로 검색해.
2. 추가로 "major corporate news today bonds M&A SEC regulation" 그리고 "오늘 주요 기업 뉴스 채권 인수합병 규제" 로 포괄 검색을 1회씩 해서, 종목 리스트에 해당하는 뉴스가 있으면 해당 종목에 추가해.

출력 형식:
1. 가장 상단에 "## 진짜 알아야됨" 섹션을 만들어. 여기에는 전 종목 뉴스 중에서 매수/매도 판단에 직접 영향을 주는 것만 넣어. 기준: 실적 서프라이즈/미스, 규제/법적 리스크, M&A, 대규모 자금조달(채권발행 등), 대규모 투자 변경, 경영권 이슈, 목표가 대폭 변경. 해당 없으면 "오늘은 없음"으로 표시.
2. 그 아래에 종목별로 정리하고 뉴스가 없으면 특이사항 없음으로 표시해.
마크다운 형식으로 출력해.
PROMPT

# macOS 알림 (클릭하면 파일 열림)
/opt/homebrew/bin/terminal-notifier \
  -title "투자 뉴스 체크 완료" \
  -message "${TODAY} 뉴스 확인하기" \
  -open "file://${OUTPUT_FILE}" \
  -sound default
