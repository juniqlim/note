# 일일 투자 뉴스 체크

> 이 파일을 Claude Code에서 읽고 실행하면 보유/관심 종목의 어제·오늘 뉴스를 검색합니다.

## 종목 리스트

| 종목 | 검색 키워드 (한글) | 검색 키워드 (영문) |
|---|---|---|
| SK하이닉스 | SK하이닉스 | SK Hynix 000660 |
| 실리콘투 | 실리콘투 | Silicon2 257720 |
| YesAsia | 예스아시아홀딩스 | YesAsia Holdings 2209.HK |
| Google | 구글 알파벳 | Google Alphabet GOOGL |
| Netflix | 넷플릭스 | Netflix NFLX |
| Apple | 애플 | Apple AAPL |
| 삼양식품 | 삼양식품 | Samyang Foods 003230 |
| DoorDash | 도어대시 | DoorDash DASH |

## 실행 프롬프트

```
daily-news-check.md 를 읽고, 종목 리스트의 각 종목에 대해 어제·오늘 투자에 영향을 줄 수 있는 뉴스를 검색해줘.
검색할 때 "종목명 어제 오늘 뉴스" 또는 "종목명 news today yesterday" 형태로 검색해.
결과는 종목별로 정리하고, 뉴스가 없으면 "특이사항 없음"으로 표시해.
```
