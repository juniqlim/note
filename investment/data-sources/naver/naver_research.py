"""네이버 금융 리서치에서 종목별 애널리스트 리포트 PDF를 받는다.

사용법:
    python naver_research.py 000660 --since 2026-06-01 --out ai-agent/hynix/analyst-report

주의 (2026-07 기준):
- 리포트 등록은 발행일로부터 수일 지연된다. 당일 리포트는 없다.
- 일부 리포트는 PDF 원문이 없다(목록엔 있으나 상세에 첨부 없음).
- 짧은 간격으로 반복 요청하면 SSL 단에서 차단된다. DELAY로 간격을 둔다.
"""

import argparse
import os
import re
import sys
import time
import urllib.request

LIST_URL = "https://finance.naver.com/research/company_list.naver?searchType=itemCode&itemCode={code}"
READ_URL = "https://finance.naver.com/research/company_read.naver?nid={nid}&page=1"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/126.0 Safari/537.36"
DELAY = 1.5

ROW = re.compile(r"<tr>(.*?)</tr>", re.S)
NID = re.compile(r"nid=(\d+)")
CELL = re.compile(r"<td.*?>(.*?)</td>", re.S)
DATE = re.compile(r"(\d{2})\.(\d{2})\.(\d{2})")
TAG = re.compile(r"<[^>]+>")
PDF = re.compile(r"https://stock\.pstatic\.net/stock-research/[^\s\"'<>]+\.pdf")


def fetch(url, encoding="euc-kr"):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as res:
        return res.read().decode(encoding, "ignore")


def parse_list(html, since=None):
    """목록 HTML → [(nid, YYYYMMDD, 증권사, 제목)]. since 이전 발행분은 제외."""
    reports = []
    for row in ROW.findall(html):
        nid = NID.search(row)
        if not nid:
            continue
        cells = [TAG.sub("", c).strip() for c in CELL.findall(row)]
        dates = [DATE.match(c) for c in cells]
        date = next((d for d in dates if d), None)
        if not date:
            continue
        yymmdd = "20{}{}{}".format(*date.groups())
        if since and yymmdd < since:
            continue
        reports.append((int(nid.group(1)), yymmdd, cells[2], cells[1]))
    return reports


def extract_pdf_url(html):
    """상세 HTML → PDF URL. 첨부가 없으면 None."""
    found = PDF.search(html)
    return found.group(0) if found else None


def download(code, since, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    reports = parse_list(fetch(LIST_URL.format(code=code)), since)
    if not reports:
        print(f"{code}: {since} 이후 리포트 없음")
        return

    for nid, date, broker, title in reports:
        path = os.path.join(out_dir, f"{date}_{broker}.pdf")
        if os.path.exists(path):
            print(f"  건너뜀 {date} {broker} (이미 있음)")
            continue

        time.sleep(DELAY)
        url = extract_pdf_url(fetch(READ_URL.format(nid=nid)))
        if not url:
            print(f"  없음   {date} {broker} — PDF 원문 미제공 ({title})")
            continue

        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as res:
            body = res.read()
        with open(path, "wb") as f:
            f.write(body)
        print(f"  받음   {date} {broker} {len(body):>9,}B — {title}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("code", help="종목코드 (예: 000660)")
    p.add_argument("--since", default="", help="이 날짜 이후만 (YYYY-MM-DD)")
    p.add_argument("--out", default=".", help="저장 디렉토리")
    args = p.parse_args()

    download(args.code, args.since.replace("-", ""), args.out)


if __name__ == "__main__":
    sys.exit(main())
