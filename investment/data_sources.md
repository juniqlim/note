# 투자 데이터 소스

## 1. 텔레그램 채널 검색

- **인증**: `~/.telegram_credentials` (api_id, api_hash)
- **세션**: `~/.telegram_session`
- **라이브러리**: `telethon`

### 사용법

```bash
# 채널 목록 조회
python telegram_info.py

# 키워드 검색
python telegram_search.py 코스맥스
python telegram_search.py 코스맥스 실리콘투 -n 10 -o result.txt
```

## 2. 와이낫셀리포트 (whynotsellreport.com)

증권사 애널리스트 리포트 메타데이터 (목표가, 투자의견, 요약 등). 인증 불필요.

### API

```
# 최근 N일 날짜 목록
GET https://www.whynotsellreport.com/api/reports/dates/range/{N}

# 기간별 리포트 조회
GET https://www.whynotsellreport.com/api/reports/from/{YYYY-MM-DD}/to/{YYYY-MM-DD}
```

### 응답 필드

| 필드 | 설명 |
|------|------|
| company_name | 종목명 |
| analyst_name | 애널리스트 |
| title | 리포트 제목 |
| judge | 투자의견 (BUY, 매수, HOLD 등) |
| price | 목표주가 |
| description | 핵심 요약 |
| report_url | 네이버 금융 리포트 링크 |
| date | 발행일 |

### 예시

```bash
# 오늘 리포트 전체
curl https://www.whynotsellreport.com/api/reports/from/2026-02-11/to/2026-02-11

# 최근 한달 코스맥스 리포트 → jq로 필터
curl -s 'https://www.whynotsellreport.com/api/reports/from/2026-01-11/to/2026-02-11' \
  | jq '[.[] | select(.company_name == "코스맥스")]'
```

## 3. DART OpenAPI

- **API Key**: `~/.dart_api_key`
- 공시 조회, 재무제표 등

## 4. SEC EDGAR (미국 상장사)

미국 상장사 10-K(연간), 10-Q(분기), 8-K(수시) 등 공시 보고서. 인증 불필요.

### 공시 검색

```
# EFTS 검색 API (추천)
https://efts.sec.gov/LATEST/search-index?q="회사명"&forms=10-K,10-Q&dateRange=custom&startdt=2023-01-01&enddt=2026-12-31

# cgi-bin 방식
https://www.sec.gov/cgi-bin/browse-edgar?company=회사명&CIK=&type=10-K&dateb=&owner=include&count=40&search_text=&action=getcompany
```

### 보고서 본문 URL 패턴

```
# HTML 본문 (CIK + accession number + 파일명)
https://www.sec.gov/Archives/edgar/data/{CIK}/{accession}/{ticker}-{period}.htm

# 예: Netflix 10-K FY2025
https://www.sec.gov/Archives/edgar/data/1065280/000106528026000034/nflx-20251231.htm
```

### 주요 CIK

| 회사 | CIK |
|------|-----|
| Netflix | 1065280 |
| DoorDash | 1792789 |

### 사용 사례

- `netflix/report/` → 10-K, 10-Q, 8-K(주주서한) txt 저장
- `DoorDash/report/` → 10-K, 10-Q txt 저장

## 5. HKEX (홍콩 상장사)

홍콩거래소 공시 시스템. 인증 불필요.

### 공시 검색

```
# 종목별 공시 검색 (stock=종목코드 5자리, category=0 전체)
https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en&stock=02209&category=0&from=20230101&to=20260205
```

### 보고서 PDF 직접 다운로드

```
# URL 패턴
https://www1.hkexnews.hk/listedco/listconews/sehk/{YYYY}/{MMDD}/{문서ID}.pdf

# 예: YesAsia 2025 중간보고서
https://www1.hkexnews.hk/listedco/listconews/sehk/2025/0417/2025041700063.pdf
```

### 사용 사례

- `KBeautyDistribution/yesasia_reports/` → YesAsia(2209.HK) Annual/Interim Report PDF+txt 저장
