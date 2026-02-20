"""강환국 울트라 전략 스크리너.

12개 지표 백분위 순위 합산 + 신F-스코어(≥3) 필터.
"""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "magic_formula.db")

FINANCIAL_SECTORS = {"은행", "증권", "보험", "카드", "캐피탈", "저축은행", "금융"}
FINANCIAL_NAME_KEYWORDS = {"금융", "은행", "보험", "증권", "캐피탈", "저축", "파이낸셜", "지주"}


def calc_inverse_per(per):
    if per is None or per <= 0:
        return None
    return 1.0 / per


def calc_inverse_pbr(pbr):
    if pbr is None or pbr <= 0:
        return None
    return 1.0 / pbr


def calc_inverse_psr(market_cap, quarterly_revenue):
    if not market_cap or market_cap <= 0:
        return None
    if not quarterly_revenue or quarterly_revenue <= 0:
        return None
    psr = market_cap / quarterly_revenue
    return 1.0 / psr


def calc_inverse_pfcr(market_cap, quarterly_ocf, quarterly_capex):
    if not market_cap or market_cap <= 0:
        return None
    fcf = (quarterly_ocf or 0) - (quarterly_capex or 0)
    if fcf <= 0:
        return None
    pfcr = market_cap / fcf
    return 1.0 / pfcr


def calc_gpa(gross_profit, total_assets):
    if gross_profit is None or total_assets is None or total_assets <= 0:
        return None
    return gross_profit / total_assets


def calc_asset_growth(curr_assets, prev_assets):
    if prev_assets is None or prev_assets <= 0:
        return None
    if curr_assets is None:
        return None
    return (curr_assets - prev_assets) / prev_assets


def calc_op_borrowing_ratio(op_curr, op_prev, borrow_curr, borrow_prev):
    """영업이익 증가율 / 차입금 증가율."""
    if op_prev is None or op_prev == 0:
        return None
    if borrow_prev is None or borrow_prev == 0:
        return None
    op_growth = (op_curr - op_prev) / abs(op_prev)
    borrow_growth = (borrow_curr - borrow_prev) / abs(borrow_prev)
    if borrow_growth == 0:
        return None
    return op_growth / borrow_growth


def calc_new_f_score(stock):
    """신F-스코어: 9개 항목, 전년도 대비 개선 여부 합산 (0~9점).

    1. 영업이익 증가
    2. 순이익 증가
    3. 영업현금흐름 증가
    4. 매출총이익률 개선
    5. 매출액 증가
    6. 자산회전율 개선 (매출/자산)
    7. 이익잉여금 증가
    8. 부채비율 감소 (부채/자산)
    9. 유동비율 개선 (유동자산/유동부채)
    """
    score = 0

    def _safe_gt(curr, prev):
        if curr is None or prev is None:
            return False
        return curr > prev

    # 1. 영업이익 증가
    if _safe_gt(stock.get("operating_income"), stock.get("prev_operating_income")):
        score += 1

    # 2. 순이익 증가
    if _safe_gt(stock.get("net_income"), stock.get("prev_net_income")):
        score += 1

    # 3. 영업현금흐름 증가
    if _safe_gt(stock.get("operating_cash_flow"), stock.get("prev_operating_cash_flow")):
        score += 1

    # 4. 매출총이익률 개선 (GP/Revenue)
    gp = stock.get("gross_profit")
    rev = stock.get("revenue")
    prev_gp = stock.get("prev_gross_profit")
    prev_rev = stock.get("prev_revenue")
    if gp is not None and rev and prev_gp is not None and prev_rev:
        if (gp / rev) > (prev_gp / prev_rev):
            score += 1

    # 5. 매출액 증가
    if _safe_gt(stock.get("revenue"), stock.get("prev_revenue")):
        score += 1

    # 6. 자산회전율 개선 (매출/자산)
    ta = stock.get("total_assets")
    prev_ta = stock.get("prev_total_assets")
    if rev and ta and ta > 0 and prev_rev and prev_ta and prev_ta > 0:
        if (rev / ta) > (prev_rev / prev_ta):
            score += 1

    # 7. 이익잉여금 증가
    if _safe_gt(stock.get("retained_earnings"), stock.get("prev_retained_earnings")):
        score += 1

    # 8. 부채비율 감소 (부채/자산)
    td = stock.get("total_debt")
    prev_td = stock.get("prev_total_debt")
    if td is not None and ta and ta > 0 and prev_td is not None and prev_ta and prev_ta > 0:
        if (td / ta) < (prev_td / prev_ta):
            score += 1

    # 9. 유동비율 개선 (유동자산/유동부채)
    ca = stock.get("current_assets")
    cl = stock.get("current_liabilities")
    prev_ca = stock.get("prev_current_assets")
    prev_cl = stock.get("prev_current_liabilities")
    if ca and cl and cl > 0 and prev_ca and prev_cl and prev_cl > 0:
        if (ca / cl) > (prev_ca / prev_cl):
            score += 1

    return score


def assign_percentile_ranks(stocks, key, descending=True):
    """지표별 순위 부여. None은 꼴찌.

    descending=True: 값이 클수록 좋음 (1/PER, 1/PBR 등)
    descending=False: 값이 작을수록 좋음 (자산성장률, 변동성)
    """
    rank_key = f"{key}_rank"
    n = len(stocks)

    valid = [(i, s[key]) for i, s in enumerate(stocks) if s.get(key) is not None]
    valid.sort(key=lambda x: x[1], reverse=descending)

    rank_map = {}
    for rank, (idx, _) in enumerate(valid, 1):
        rank_map[idx] = rank

    for i, s in enumerate(stocks):
        s[rank_key] = rank_map.get(i, n)

    return stocks


# 12개 지표 정의: (key, descending)
ULTRA_METRICS = [
    ("inverse_per", True),       # 1/PER — 높을수록 좋음
    ("inverse_pbr", True),       # 1/PBR
    ("inverse_psr", True),       # 1/PSR
    ("inverse_pfcr", True),      # 1/PFCR
    ("gpa", True),               # GP/A
    ("asset_growth", False),     # 자산성장률 — 낮을수록 좋음
    ("op_borrowing_ratio", True),  # 영업이익/차입금 증가율
    ("op_income_qoq", True),     # 영업이익 QoQ
    ("op_income_yoy", True),     # 영업이익 YoY
    ("net_income_qoq", True),    # 순이익 QoQ
    ("net_income_yoy", True),    # 순이익 YoY
    ("price_volatility", False), # 변동성 — 낮을수록 좋음
]


def rank_ultra(stocks, f_score_min=3):
    """12개 지표 백분위 순위 합산 + 신F-스코어 필터."""
    # 1) 지표 계산
    for s in stocks:
        s["inverse_per"] = calc_inverse_per(s.get("per"))
        s["inverse_pbr"] = calc_inverse_pbr(s.get("pbr"))
        s["inverse_psr"] = calc_inverse_psr(s.get("market_cap"), s.get("quarterly_revenue"))
        s["inverse_pfcr"] = calc_inverse_pfcr(
            s.get("market_cap"), s.get("quarterly_ocf"), s.get("quarterly_capex"))
        s["gpa"] = calc_gpa(s.get("gross_profit"), s.get("total_assets"))
        s["asset_growth"] = calc_asset_growth(
            s.get("total_assets"), s.get("prev_total_assets"))
        s["op_borrowing_ratio"] = calc_op_borrowing_ratio(
            s.get("operating_income", 0), s.get("prev_operating_income", 0),
            (s.get("short_term_borrowings", 0) or 0) + (s.get("long_term_borrowings", 0) or 0),
            (s.get("prev_short_term_borrowings", 0) or 0) + (s.get("prev_long_term_borrowings", 0) or 0),
        )
        s["f_score"] = calc_new_f_score(s)

    # 2) F-스코어 필터
    filtered = [s for s in stocks if s["f_score"] >= f_score_min]

    # 3) 지표별 백분위 순위
    for key, descending in ULTRA_METRICS:
        assign_percentile_ranks(filtered, key, descending)

    # 4) 합산 순위
    for s in filtered:
        s["ultra_rank"] = sum(s.get(f"{key}_rank", len(filtered)) for key, _ in ULTRA_METRICS)

    return sorted(filtered, key=lambda x: x["ultra_rank"])


def load_ultra_stocks_from_db(bsns_year, db_path=DB_PATH):
    """당기 + 전기 데이터를 로드하여 울트라 전략용 dict 리스트 생성."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    prev_year = str(int(bsns_year) - 1)

    rows = conn.execute("""
        SELECT c.corp_name AS name, c.sector, f.*
        FROM financials f
        JOIN companies c ON c.stock_code = f.stock_code
        WHERE f.bsns_year = ?
          AND f.operating_income > 0
          AND f.market_cap > 0
    """, (bsns_year,)).fetchall()

    # 전기 데이터 맵
    prev_rows = conn.execute("""
        SELECT stock_code, operating_income, net_income, operating_cash_flow,
               gross_profit, revenue, total_assets, total_debt,
               current_assets, current_liabilities, retained_earnings,
               short_term_borrowings, long_term_borrowings
        FROM financials WHERE bsns_year = ?
    """, (prev_year,)).fetchall()
    conn.close()

    prev_map = {r["stock_code"]: dict(r) for r in prev_rows}

    stocks = []
    for r in rows:
        name = r["name"] or ""
        sector = r["sector"] or ""
        if any(kw in sector for kw in FINANCIAL_SECTORS):
            continue
        if any(kw in name for kw in FINANCIAL_NAME_KEYWORDS):
            continue

        prev = prev_map.get(r["stock_code"], {})
        stocks.append({
            "stock_code": r["stock_code"],
            "name": name,
            "operating_income": r["operating_income"],
            "net_income": r["net_income"] or 0,
            "operating_cash_flow": r["operating_cash_flow"] or 0,
            "gross_profit": r["gross_profit"] or 0,
            "revenue": r["revenue"] or 0,
            "total_assets": r["total_assets"] or 0,
            "total_debt": r["total_debt"] or 0,
            "current_assets": r["current_assets"] or 0,
            "current_liabilities": r["current_liabilities"] or 0,
            "market_cap": r["market_cap"],
            "per": r["per"],
            "pbr": r["pbr"],
            "short_term_borrowings": r["short_term_borrowings"] or 0,
            "long_term_borrowings": r["long_term_borrowings"] or 0,
            "quarterly_revenue": r["quarterly_revenue"],
            "quarterly_ocf": r["quarterly_ocf"],
            "quarterly_capex": r["quarterly_capex"],
            "price_volatility": r["price_volatility"],
            "retained_earnings": r["retained_earnings"],
            "op_income_qoq": r["op_income_qoq"],
            "op_income_yoy": r["op_income_yoy"],
            "net_income_qoq": r["net_income_qoq"],
            "net_income_yoy": r["net_income_yoy"],
            # 전기 데이터
            "prev_operating_income": prev.get("operating_income"),
            "prev_net_income": prev.get("net_income"),
            "prev_operating_cash_flow": prev.get("operating_cash_flow"),
            "prev_gross_profit": prev.get("gross_profit"),
            "prev_revenue": prev.get("revenue"),
            "prev_total_assets": prev.get("total_assets"),
            "prev_total_debt": prev.get("total_debt"),
            "prev_current_assets": prev.get("current_assets"),
            "prev_current_liabilities": prev.get("current_liabilities"),
            "prev_retained_earnings": prev.get("retained_earnings"),
            "prev_short_term_borrowings": prev.get("short_term_borrowings"),
            "prev_long_term_borrowings": prev.get("long_term_borrowings"),
        })
    return stocks


def print_ultra(bsns_year, top_n=50):
    """울트라 전략 상위 종목 CLI 출력."""
    stocks = load_ultra_stocks_from_db(bsns_year)
    ranked = rank_ultra(stocks)

    print(f"\n{'='*100}")
    print(f" Ultra Strategy Top {top_n} — {bsns_year}")
    print(f"{'='*100}")
    print(f"{'순위':>4} {'종목명':<16} {'F점수':>5} {'합산':>6} "
          f"{'1/PER':>7} {'1/PBR':>7} {'GP/A':>7} {'변동성':>7}")
    print("-" * 100)

    for i, s in enumerate(ranked[:top_n], 1):
        inv_per = f"{s.get('inverse_per', 0) or 0:.2f}"
        inv_pbr = f"{s.get('inverse_pbr', 0) or 0:.2f}"
        gpa = f"{s.get('gpa', 0) or 0:.1%}"
        vol = f"{s.get('price_volatility', 0) or 0:.1%}" if s.get('price_volatility') else "N/A"
        print(f"{i:>4} {s['name']:<16} {s['f_score']:>5} {s['ultra_rank']:>6} "
              f"{inv_per:>7} {inv_pbr:>7} {gpa:>7} {vol:>7}")


def export_ultra_html(bsns_year, top_n=50):
    """울트라 전략 결과를 HTML 테이블 문자열로 반환."""
    stocks = load_ultra_stocks_from_db(bsns_year)
    ranked = rank_ultra(stocks)

    rows_html = []
    for i, s in enumerate(ranked[:top_n], 1):
        inv_per = f"{s.get('inverse_per', 0) or 0:.3f}"
        inv_pbr = f"{s.get('inverse_pbr', 0) or 0:.3f}"
        gpa = f"{(s.get('gpa', 0) or 0) * 100:.1f}%"
        vol = f"{(s.get('price_volatility', 0) or 0) * 100:.1f}%" if s.get('price_volatility') else "N/A"
        mcap_b = f"{s['market_cap'] / 1e8:,.0f}"
        rows_html.append(
            f"<tr><td>{i}</td><td>{s['name']}</td><td>{s['stock_code']}</td>"
            f"<td>{mcap_b}</td><td>{s['f_score']}</td><td>{s['ultra_rank']}</td>"
            f"<td>{inv_per}</td><td>{inv_pbr}</td><td>{gpa}</td><td>{vol}</td></tr>"
        )
    return "\n".join(rows_html)


if __name__ == "__main__":
    import sys
    year = sys.argv[1] if len(sys.argv) > 1 else "2024"
    print_ultra(year)
