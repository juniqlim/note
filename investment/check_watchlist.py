"""
투자 Watch List 체크 스크립트

사용법: python3 investment/check_watchlist.py
        python3 investment/check_watchlist.py --ticker DASH
"""

import argparse
import json
import urllib.request
from datetime import datetime

# === Watch List 정의 ===

WATCHLIST = {
    "DASH": {
        "name": "DoorDash",
        "signals": [
            {"metric": "GOV YoY", "current": "20%", "trigger": "25%+"},
            {"metric": "주문수 YoY", "current": "20%", "trigger": "볼륨 주도 성장"},
            {"metric": "MAU", "current": "4,200만 (13%)", "trigger": "침투율 20%+"},
            {"metric": "DashPass 구독자", "current": "2,200만", "trigger": "3,000만+"},
            {"metric": "Deliveroo 통합", "current": "미반영", "trigger": "해외 매출 20%+ & 흑자"},
        ],
        "verdict": "GOV 재가속 + 마진 유지/개선 조합 시 재검토",
    },
    "NFLX": {
        "name": "Netflix",
        "signals": [
            {"metric": "WBD 인수", "current": "규제 승인 대기", "trigger": "클로징 여부"},
            {"metric": "광고 매출", "current": "not material", "trigger": "성장 가시화"},
            {"metric": "길드 협상", "current": "2026.5~6 만료", "trigger": "파업 or 비용 증가"},
            {"metric": "영업이익률", "current": "Q3 28.2%→Q4 24.5%", "trigger": "Q4 하락 패턴"},
        ],
        "verdict": "WBD 통합 + 길드 협상 결과 (2026 상반기)",
    },
    "257720.KQ": {
        "name": "실리콘투",
        "signals": [
            {"metric": "매출 성장률", "current": "+59%(2025E)", "trigger": "36%(2026E)→추가 하락?"},
            {"metric": "OPM", "current": "~18.4%(2025E)", "trigger": "하락 지속 여부"},
            {"metric": "조선미녀 비중", "current": "23~24%", "trigger": "직접유통 추가 이탈"},
            {"metric": "유럽 성장률", "current": "+138% YoY", "trigger": "지속 가능성"},
        ],
        "verdict": "조선미녀 이탈 영향 + 유럽 성장 지속 여부 (다음 검토: 2026-08-05)",
    },
    "1613.HK": {
        "name": "YesAsia (ABW)",
        "signals": [
            {"metric": "ABW GPM", "current": "18.6%", "trigger": "유지/상향 (목표 21%→24%)"},
            {"metric": "ABW 매출 성장률", "current": "+111% YoY", "trigger": "50%+ 지속?"},
            {"metric": "B2B:B2C 비율", "current": "32:68", "trigger": "50:50 방향 진행"},
            {"metric": "한국 물류센터", "current": "셋업 중", "trigger": "1H2026 마진 반영"},
        ],
        "verdict": "ABW 마진 개선 + B2B 비중 증가 (다음 검토: FY2025 보고서)",
    },
}


def fetch_quote(ticker: str) -> dict | None:
    """Yahoo Finance에서 현재 주가 정보를 가져온다."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?range=5d&interval=1d"
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        result = data["chart"]["result"][0]
        meta = result["meta"]
        closes = result["indicators"]["quote"][0]["close"]
        closes = [c for c in closes if c is not None]
        if len(closes) >= 2:
            prev, last = closes[-2], closes[-1]
            change_pct = (last - prev) / prev * 100
        else:
            last = closes[-1] if closes else meta.get("regularMarketPrice", 0)
            change_pct = 0
        return {
            "price": last,
            "change_pct": change_pct,
            "currency": meta.get("currency", "USD"),
        }
    except Exception as e:
        return {"error": str(e)}


def print_separator():
    print("=" * 70)


def print_watchlist(ticker_filter: str | None = None):
    print_separator()
    print(f"  INVESTMENT WATCH LIST  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print_separator()

    for ticker, info in WATCHLIST.items():
        if ticker_filter and ticker != ticker_filter:
            continue

        print(f"\n  [{ticker}] {info['name']}")
        print("-" * 70)

        # 주가 조회
        quote = fetch_quote(ticker)
        if quote and "error" not in quote:
            arrow = "+" if quote["change_pct"] >= 0 else ""
            print(f"  주가: {quote['price']:.2f} {quote['currency']} ({arrow}{quote['change_pct']:.1f}%)")
        elif quote:
            print(f"  주가: 조회 실패 ({quote['error'][:50]})")
        print()

        # 시그널 테이블
        print(f"  {'시그널':<22} {'현재':<22} {'트리거'}")
        print(f"  {'-'*22} {'-'*22} {'-'*22}")
        for s in info["signals"]:
            print(f"  {s['metric']:<22} {s['current']:<22} {s['trigger']}")

        print(f"\n  >> {info['verdict']}")

    print()
    print_separator()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="투자 Watch List 체크")
    parser.add_argument("--ticker", type=str, help="특정 티커만 조회 (e.g. DASH, NFLX)")
    args = parser.parse_args()

    print_watchlist(args.ticker)
