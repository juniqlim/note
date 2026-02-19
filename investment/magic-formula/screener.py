"""Magic Formula + DCF 스크리너."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "magic_formula.db")

# 금융업종 키워드 (은행, 증권, 보험, 카드, 캐피탈, 저축은행 등)
FINANCIAL_SECTORS = {"은행", "증권", "보험", "카드", "캐피탈", "저축은행", "금융"}


# --- Magic Formula 계산 ---

def calculate_roic(ebit, current_assets, current_liabilities, cash, tangible_assets):
    """ROIC = EBIT / 투하자본. 투하자본 <= 0이면 None."""
    invested_capital = current_assets - current_liabilities - cash + tangible_assets
    if invested_capital <= 0:
        return None
    return ebit / invested_capital


def calculate_earnings_yield(ebit, market_cap, total_debt, cash):
    """Earnings Yield = EBIT / EV. EV <= 0이면 None."""
    ev = market_cap + total_debt - cash
    if ev <= 0:
        return None
    return ebit / ev


def rank_stocks(stocks):
    """마법공식 순위 계산. ROIC/EY가 유효한 종목만 포함."""
    valid = []
    for s in stocks:
        roic = calculate_roic(
            s["ebit"], s["current_assets"], s["current_liabilities"],
            s["cash"], s["tangible_assets"],
        )
        ey = calculate_earnings_yield(
            s["ebit"], s["market_cap"], s["total_debt"], s["cash"],
        )
        if roic is not None and ey is not None:
            valid.append({**s, "roic": roic, "earnings_yield": ey})

    # 높은 ROIC → 낮은 순위 번호 (1이 최고)
    sorted_by_roic = sorted(valid, key=lambda x: x["roic"], reverse=True)
    for i, s in enumerate(sorted_by_roic):
        s["roic_rank"] = i + 1

    # 높은 EY → 낮은 순위 번호
    sorted_by_ey = sorted(valid, key=lambda x: x["earnings_yield"], reverse=True)
    for i, s in enumerate(sorted_by_ey):
        s["ey_rank"] = i + 1

    # 종합 순위: 두 순위 합산, 낮을수록 상위
    for s in valid:
        s["magic_rank"] = s["roic_rank"] + s["ey_rank"]

    return sorted(valid, key=lambda x: x["magic_rank"])


# --- DCF 계산 ---

def calculate_fcf(ebit, tax_rate, depreciation, capex, wc_change):
    """Free Cash Flow = EBIT*(1-t) + 감가상각 - CAPEX - 운전자본증가."""
    return ebit * (1 - tax_rate) + depreciation - capex - wc_change


def calculate_dcf_value(projected_fcfs, wacc, terminal_growth):
    """DCF 기업가치 = PV(FCFs) + PV(Terminal Value)."""
    n = len(projected_fcfs)
    pv_fcfs = sum(fcf / (1 + wacc) ** i for i, fcf in enumerate(projected_fcfs, 1))

    terminal_value = projected_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** n

    return pv_fcfs + pv_terminal


def backtest_dcf(yearly_data, wacc=0.10, terminal_growth=0.02, projection_years=5):
    """과거 연도별 데이터로 DCF 적정가를 구하고 실제 주가와 비교.

    yearly_data: {
        "2021": {ebit, tax_rate, depreciation, capex, wc_change,
                 total_debt, cash, shares, growth_rate, actual_price},
        ...
    }
    """
    results = []
    for year in sorted(yearly_data.keys()):
        d = yearly_data[year]
        base_fcf = calculate_fcf(
            d["ebit"], d["tax_rate"], d["depreciation"], d["capex"], d["wc_change"],
        )
        # 성장률로 5년 FCF 추정
        projected = [base_fcf * (1 + d["growth_rate"]) ** i for i in range(1, projection_years + 1)]
        enterprise_value = calculate_dcf_value(projected, wacc, terminal_growth)
        equity_value = enterprise_value - d["total_debt"] + d["cash"]
        dcf_price = equity_value / d["shares"] if d["shares"] > 0 else 0

        actual = d["actual_price"]
        upside = (dcf_price - actual) / actual if actual > 0 else 0

        results.append({
            "year": year,
            "dcf_price": round(dcf_price, 2),
            "actual_price": actual,
            "upside": round(upside, 4),
        })
    return results


# --- DB에서 읽어서 스크리닝 ---

def load_stocks_from_db(bsns_year, db_path=DB_PATH):
    """SQLite에서 특정 사업연도 데이터를 읽어 종목 리스트로 반환."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("""
        SELECT c.corp_name AS name, c.sector, f.*
        FROM financials f
        JOIN companies c ON c.stock_code = f.stock_code
        WHERE f.bsns_year = ?
          AND f.operating_income > 0
          AND f.market_cap > 0
    """, (bsns_year,)).fetchall()
    conn.close()

    stocks = []
    for r in rows:
        # 금융주 제외
        if r["sector"] and any(kw in r["sector"] for kw in FINANCIAL_SECTORS):
            continue
        stocks.append({
            "stock_code": r["stock_code"],
            "name": r["name"],
            "ebit": r["operating_income"],
            "current_assets": r["current_assets"] or 0,
            "current_liabilities": r["current_liabilities"] or 0,
            "cash": r["cash"] or 0,
            "tangible_assets": r["tangible_assets"] or 0,
            "market_cap": r["market_cap"],
            "total_debt": r["total_debt"] or 0,
            "revenue": r["revenue"] or 0,
        })
    return stocks


def print_magic_formula(bsns_year, top_n=30):
    """마법공식 상위 종목 출력."""
    stocks = load_stocks_from_db(bsns_year)
    ranked = rank_stocks(stocks)

    print(f"\n{'='*80}")
    print(f" Magic Formula Top {top_n} — {bsns_year}")
    print(f"{'='*80}")
    print(f"{'순위':>4} {'종목명':<16} {'매출(억)':>10} {'영업이익(억)':>12} "
          f"{'ROIC':>8} {'EY':>8} {'합산':>6}")
    print("-" * 80)

    for i, s in enumerate(ranked[:top_n], 1):
        print(f"{i:>4} {s['name']:<16} {s.get('revenue',0)/1e8:>10,.0f} "
              f"{s['ebit']/1e8:>12,.0f} {s['roic']:>8.1%} "
              f"{s['earnings_yield']:>8.1%} {s['magic_rank']:>6}")


if __name__ == "__main__":
    import sys
    year = sys.argv[1] if len(sys.argv) > 1 else "2024"
    print_magic_formula(year)
