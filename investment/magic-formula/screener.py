"""Magic Formula + DCF 스크리너."""

import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "magic_formula.db")

# 금융업종 키워드 — sector 또는 종목명에서 필터
FINANCIAL_SECTORS = {"은행", "증권", "보험", "카드", "캐피탈", "저축은행", "금융"}
FINANCIAL_NAME_KEYWORDS = {"금융", "은행", "보험", "증권", "캐피탈", "저축", "파이낸셜", "지주"}


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


def calculate_fcf_from_ocf(operating_cash_flow, capex):
    """Free Cash Flow = 영업활동현금흐름 - CAPEX. 감가상각비 미공시 기업용."""
    return operating_cash_flow - capex


def calculate_dcf_value(projected_fcfs, wacc, terminal_growth):
    """DCF 기업가치 = PV(FCFs) + PV(Terminal Value)."""
    n = len(projected_fcfs)
    pv_fcfs = sum(fcf / (1 + wacc) ** i for i, fcf in enumerate(projected_fcfs, 1))

    terminal_value = projected_fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_terminal = terminal_value / (1 + wacc) ** n

    return pv_fcfs + pv_terminal


def dcf_from_financials(financial, growth_rate=0.05, wacc=0.10, terminal_growth=0.02,
                        projection_years=5, prev_financial=None):
    """DB 재무데이터 dict → DCF 적정 주가 산출.

    financial: {operating_income, tax_expense, depreciation, capex,
                current_assets, current_liabilities, cash, total_debt,
                shares_outstanding, market_cap}
    prev_financial: 전년도 데이터 (운전자본 변동 계산용, 선택)
    """
    shares = financial.get("shares_outstanding", 0)
    if not shares or shares <= 0:
        return None

    ebit = financial["operating_income"]
    tax_expense = financial.get("tax_expense", 0)
    tax_rate = tax_expense / ebit if ebit > 0 and tax_expense > 0 else 0.22
    depreciation = financial.get("depreciation", 0)
    capex = financial.get("capex", 0)
    ocf = financial.get("operating_cash_flow", 0)

    # FCF 산출: OCF가 있으면 OCF - CAPEX, 없으면 EBIT 기반
    if ocf and ocf != 0:
        fcf = calculate_fcf_from_ocf(ocf, capex)
        fcf_method = "OCF"
        wc_change = 0
    else:
        # 운전자본 변동: 전년도 데이터가 있으면 계산, 없으면 0
        if prev_financial:
            def _wc(f):
                return (f.get("current_assets", 0) - f.get("cash", 0)) - f.get("current_liabilities", 0)
            wc_change = _wc(financial) - _wc(prev_financial)
        else:
            wc_change = 0
        fcf = calculate_fcf(ebit, tax_rate, depreciation, capex, wc_change)
        fcf_method = "EBIT"

    if fcf > 0:
        projected = [fcf * (1 + growth_rate) ** i for i in range(1, projection_years + 1)]
        enterprise_value = calculate_dcf_value(projected, wacc, terminal_growth)
    else:
        # FCF 음수: 그래도 계산은 하되 의미 없음을 표시
        projected = [fcf * (1 + growth_rate) ** i for i in range(1, projection_years + 1)]
        enterprise_value = calculate_dcf_value(projected, wacc, terminal_growth)

    equity_value = enterprise_value - financial.get("total_debt", 0) + financial.get("cash", 0)
    dcf_price = equity_value / shares
    current_price = financial["market_cap"] / shares
    upside = (dcf_price - current_price) / current_price if current_price > 0 else 0

    return {
        "dcf_price": round(dcf_price, 2),
        "current_price": round(current_price, 2),
        "upside": round(upside, 4),
        "fcf": fcf,
        "fcf_method": fcf_method,
        "tax_rate": round(tax_rate, 4),
        "wc_change": wc_change,
    }


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
        # 금융주 제외 (sector 또는 종목명 기반)
        name = r["name"] or ""
        sector = r["sector"] or ""
        if any(kw in sector for kw in FINANCIAL_SECTORS):
            continue
        if any(kw in name for kw in FINANCIAL_NAME_KEYWORDS):
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


def load_stock_financials(stock_code, bsns_year, db_path=DB_PATH):
    """SQLite에서 특정 종목의 재무데이터 조회."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    row = conn.execute("""
        SELECT c.corp_name AS name, f.*
        FROM financials f
        JOIN companies c ON c.stock_code = f.stock_code
        WHERE f.stock_code = ? AND f.bsns_year = ?
    """, (stock_code, bsns_year)).fetchone()
    conn.close()
    return dict(row) if row else None


def print_dcf(stock_code, bsns_year, growth_rate=0.05, wacc=0.10):
    """특정 종목의 DCF 적정가 출력."""
    curr = load_stock_financials(stock_code, bsns_year)
    if not curr:
        print(f"{stock_code} {bsns_year}년 데이터 없음")
        return

    # 전년도 데이터 (운전자본 변동용)
    prev_year = str(int(bsns_year) - 1)
    prev = load_stock_financials(stock_code, prev_year)

    result = dcf_from_financials(curr, growth_rate=growth_rate, wacc=wacc, prev_financial=prev)
    if not result:
        print(f"{stock_code} DCF 계산 불가 (상장주식수 없음)")
        return

    name = curr.get("name", stock_code)
    print(f"\n{'='*60}")
    print(f" DCF 분석: {name} ({stock_code}) — {bsns_year}")
    print(f"{'='*60}")
    print(f" 영업이익(EBIT):    {curr['operating_income']/1e8:>12,.0f} 억원")
    print(f" 유효세율:          {result['tax_rate']:>12.1%}")
    print(f" 감가상각비:        {curr.get('depreciation',0)/1e8:>12,.0f} 억원")
    print(f" CAPEX:             {curr.get('capex',0)/1e8:>12,.0f} 억원")
    print(f" 운전자본 변동:     {result['wc_change']/1e8:>12,.0f} 억원")
    print(f" FCF:               {result['fcf']/1e8:>12,.0f} 억원  ({result.get('fcf_method','EBIT')} 기반)")
    print(f"-" * 60)
    print(f" 성장률:            {growth_rate:>12.1%}")
    print(f" WACC:              {wacc:>12.1%}")
    print(f" 영구성장률:        {'2.0%':>12}")
    print(f"-" * 60)
    print(f" DCF 적정 주가:     {result['dcf_price']:>12,.0f} 원")
    print(f" 현재 주가:         {result['current_price']:>12,.0f} 원")
    print(f" 괴리율(upside):    {result['upside']:>12.1%}")
    if result["fcf"] < 0:
        print(f"\n ⚠ FCF가 음수이므로 DCF 결과는 참고용입니다.")


if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == "dcf":
        stock_code = sys.argv[2]
        year = sys.argv[3] if len(sys.argv) > 3 else "2024"
        print_dcf(stock_code, year)
    else:
        year = sys.argv[1] if len(sys.argv) > 1 else "2024"
        print_magic_formula(year)
