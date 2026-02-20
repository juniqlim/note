"""DART + pykrx 데이터 수집 → SQLite 저장."""

import math
import os
import sqlite3
import time
import sys
from datetime import datetime, timedelta
from pathlib import Path

import OpenDartReader
from pykrx import stock as krx

DB_PATH = os.path.join(os.path.dirname(__file__), "magic_formula.db")
API_KEY_PATH = os.path.expanduser("~/.dart_api_key")
CALL_DELAY = 0.7  # DART API: 100 req/min
PREV_REPORT_CODE_MAP = {
    "11014": "11012",  # Q3 -> H1
    "11012": "11013",  # H1 -> Q1
}

EXTRA_FINANCIAL_COLUMNS = {
    "gross_profit": "INTEGER",
    "net_income": "INTEGER",
    "short_term_borrowings": "INTEGER",
    "long_term_borrowings": "INTEGER",
    "per": "REAL",
    "pbr": "REAL",
    "op_income_yoy": "REAL",
    "net_income_yoy": "REAL",
    "op_income_qoq": "REAL",
    "net_income_qoq": "REAL",
    "quarterly_revenue": "INTEGER",
    "quarterly_ocf": "INTEGER",
    "quarterly_capex": "INTEGER",
    "price_volatility": "REAL",
    "retained_earnings": "INTEGER",
}


def calc_volatility(prices):
    """일별 종가 리스트 → 연환산 변동성 (표준편차 * sqrt(252))."""
    if not prices or len(prices) < 2:
        return None
    returns = []
    for i in range(1, len(prices)):
        if prices[i - 1] == 0:
            continue
        returns.append((prices[i] - prices[i - 1]) / prices[i - 1])
    if not returns:
        return None
    n = len(returns)
    mean = sum(returns) / n
    variance = sum((r - mean) ** 2 for r in returns) / n
    return math.sqrt(variance) * math.sqrt(252)


def get_api_key():
    return Path(API_KEY_PATH).read_text().strip()


def _ensure_financials_columns(conn):
    existing_cols = {
        row[1] for row in conn.execute("PRAGMA table_info(financials)").fetchall()
    }
    for col, col_type in EXTRA_FINANCIAL_COLUMNS.items():
        if col in existing_cols:
            continue
        conn.execute(f"ALTER TABLE financials ADD COLUMN {col} {col_type}")


def init_db(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS companies (
            stock_code TEXT PRIMARY KEY,
            corp_code  TEXT,
            corp_name  TEXT,
            sector     TEXT
        );
        CREATE TABLE IF NOT EXISTS financials (
            stock_code         TEXT,
            bsns_year          TEXT,
            revenue            INTEGER,
            operating_income   INTEGER,
            total_assets       INTEGER,
            current_assets     INTEGER,
            current_liabilities INTEGER,
            cash               INTEGER,
            tangible_assets    INTEGER,
            total_debt         INTEGER,
            market_cap         INTEGER,
            operating_cash_flow INTEGER,
            depreciation       INTEGER,
            capex              INTEGER,
            tax_expense        INTEGER,
            interest_expense   INTEGER,
            gross_profit       INTEGER,
            net_income         INTEGER,
            short_term_borrowings INTEGER,
            long_term_borrowings  INTEGER,
            shares_outstanding INTEGER,
            per                REAL,
            pbr                REAL,
            op_income_yoy      REAL,
            net_income_yoy     REAL,
            op_income_qoq      REAL,
            net_income_qoq     REAL,
            PRIMARY KEY (stock_code, bsns_year)
        );
    """)
    _ensure_financials_columns(conn)
    conn.commit()
    return conn


def fetch_company_list(dart):
    """DART 상장기업 목록."""
    corp_list = dart.corp_codes
    listed = corp_list[corp_list["stock_code"].notna() & (corp_list["stock_code"] != " ")]
    return listed


def save_companies(conn, companies_df):
    for _, row in companies_df.iterrows():
        conn.execute(
            "INSERT OR REPLACE INTO companies (stock_code, corp_code, corp_name) VALUES (?, ?, ?)",
            (row["stock_code"].strip(), row["corp_code"].strip(), row["corp_name"].strip()),
        )
    conn.commit()
    print(f"  → {len(companies_df)}개 상장기업 저장")


def _find_trading_date(date_str):
    """주어진 날짜의 시가총액 데이터를 조회, 없으면 이전 거래일 탐색."""
    df = krx.get_market_cap(date_str)
    if not df.empty:
        return df
    for delta in range(1, 15):
        d = datetime.strptime(date_str, "%Y%m%d") - timedelta(days=delta)
        alt = d.strftime("%Y%m%d")
        df = krx.get_market_cap(alt)
        if not df.empty:
            print(f"  → {alt} 사용 ({date_str} 대신)")
            return df
    return df


def _find_market_fundamental_date(date_str):
    """주어진 날짜의 기본지표(PER/PBR) 조회, 없으면 이전 거래일 탐색."""
    df = krx.get_market_fundamental(date_str, market="ALL")
    if not df.empty:
        return df
    for delta in range(1, 15):
        d = datetime.strptime(date_str, "%Y%m%d") - timedelta(days=delta)
        alt = d.strftime("%Y%m%d")
        df = krx.get_market_fundamental(alt, market="ALL")
        if not df.empty:
            print(f"  → {alt} 기본지표 사용 ({date_str} 대신)")
            return df
    return df


def fetch_market_caps(date_str):
    """pykrx 전 종목 시가총액. {종목코드: 시가총액}."""
    df = _find_trading_date(date_str)
    return {code: int(row["시가총액"]) for code, row in df.iterrows()}


def _to_float_or_none(val):
    if val is None or val == "":
        return None
    try:
        num = float(val)
        if math.isnan(num) or math.isinf(num):
            return None
        return num
    except (ValueError, TypeError):
        return None


def fetch_market_fundamentals(date_str):
    """pykrx 전 종목 기본지표(PER/PBR). {종목코드: {'per': x, 'pbr': y}}."""
    df = _find_market_fundamental_date(date_str)
    if df.empty:
        return {}

    fundamentals = {}
    for code, row in df.iterrows():
        fundamentals[code] = {
            "per": _to_float_or_none(row.get("PER")),
            "pbr": _to_float_or_none(row.get("PBR")),
        }
    return fundamentals


def save_market_caps(conn, bsns_year, market_caps):
    for stock_code, mcap in market_caps.items():
        conn.execute("""
            INSERT INTO financials (stock_code, bsns_year, market_cap)
            VALUES (?, ?, ?)
            ON CONFLICT(stock_code, bsns_year) DO UPDATE SET market_cap = ?
        """, (stock_code, bsns_year, mcap, mcap))
    conn.commit()
    print(f"  → {len(market_caps)}개 시가총액 저장 ({bsns_year})")


def save_market_fundamentals(conn, bsns_year, fundamentals):
    for stock_code, metric in fundamentals.items():
        per = metric.get("per")
        pbr = metric.get("pbr")
        conn.execute("""
            INSERT INTO financials (stock_code, bsns_year, per, pbr)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(stock_code, bsns_year) DO UPDATE SET
                per = excluded.per,
                pbr = excluded.pbr
        """, (stock_code, bsns_year, per, pbr))
    conn.commit()
    print(f"  → {len(fundamentals)}개 PER/PBR 저장 ({bsns_year})")


def fetch_shares_outstanding(bsns_year):
    """pykrx 상장주식수. {종목코드: 주식수}."""
    df = _find_trading_date(f"{bsns_year}1230")
    if df.empty:
        return {}
    return {code: int(row["상장주식수"]) for code, row in df.iterrows()}


def save_shares(conn, bsns_year, shares_map):
    for stock_code, shares in shares_map.items():
        conn.execute("""
            UPDATE financials SET shares_outstanding = ?
            WHERE stock_code = ? AND bsns_year = ?
        """, (shares, stock_code, bsns_year))
    conn.commit()
    print(f"  → {len(shares_map)}개 상장주식수 저장 ({bsns_year})")


def _to_int_amount(val):
    """문자열 금액 → int."""
    if not val or val == "":
        return 0
    try:
        return int(str(val).replace(",", "").replace(" ", ""))
    except (ValueError, TypeError):
        return 0


def _calc_growth_rate(current, base):
    """성장률 계산. base가 0/None이면 None."""
    if base in (None, 0):
        return None
    return (current - base) / abs(base)


def _income_current_and_yoy_base(row):
    """손익 항목의 현재값/전년동기 기준값 추출."""
    current = _to_int_amount(row.get("thstrm_amount", ""))
    yoy_base_raw = row.get("frmtrm_q_amount")
    if yoy_base_raw in (None, ""):
        yoy_base_raw = row.get("frmtrm_amount", "")
    yoy_base = _to_int_amount(yoy_base_raw)
    return current, yoy_base


def _parse_amount(val):
    return _to_int_amount(val)


def _fetch_finstate_with_retry(dart, stock_code, bsns_year, reprt_code):
    for attempt in range(3):
        try:
            df = dart.finstate(stock_code, bsns_year, reprt_code=reprt_code)
            time.sleep(CALL_DELAY)
            return df
        except Exception:
            time.sleep(CALL_DELAY * (attempt + 1))
    return None


def _fetch_finstate_all_with_retry(dart, stock_code, bsns_year, reprt_code, fs_div):
    for attempt in range(3):
        try:
            df = dart.finstate_all(stock_code, bsns_year, reprt_code=reprt_code, fs_div=fs_div)
            time.sleep(CALL_DELAY)
            return df
        except Exception:
            time.sleep(CALL_DELAY * (attempt + 1))
    return None


def fetch_finstate(dart, stock_code, bsns_year, reprt_code="11011"):
    """dart.finstate로 주요 재무항목 조회.
    유동자산, 유동부채, 자산총계, 부채총계, 매출액, 영업이익 등.
    """
    df = _fetch_finstate_with_retry(dart, stock_code, bsns_year, reprt_code)
    if df is None:
        return None

    if df is None or (hasattr(df, 'empty') and df.empty):
        return None

    # 연결재무제표(CFS) 우선
    cfs = df[df["fs_div"] == "CFS"]
    data = cfs if not cfs.empty else df[df["fs_div"] == "OFS"]
    if data.empty:
        return None

    info = {}
    for _, row in data.iterrows():
        acnt = str(row.get("account_nm", ""))
        amt = _parse_amount(row.get("thstrm_amount", ""))

        if acnt == "유동자산":
            info["current_assets"] = amt
        elif acnt == "비유동자산":
            pass
        elif acnt == "자산총계":
            info["total_assets"] = amt
        elif acnt == "유동부채":
            info["current_liabilities"] = amt
        elif acnt == "부채총계":
            info["total_debt"] = amt
        elif acnt == "매출액":
            info["revenue"] = amt
        elif "영업이익" in acnt:
            info.setdefault("operating_income", amt)
        elif "당기순이익" in acnt:
            info.setdefault("net_income", amt)

    return info if "operating_income" in info else None


def _extract_income_snapshot(df):
    """분기 손익 데이터(영업이익/순이익) 추출."""
    snapshot = {}
    if df is None or (hasattr(df, "empty") and df.empty):
        return snapshot

    for _, row in df.iterrows():
        acnt = str(row.get("account_nm", ""))
        sj = str(row.get("sj_nm", ""))
        if sj not in ("손익계산서", "포괄손익계산서"):
            continue

        curr, yoy_base = _income_current_and_yoy_base(row)
        if "영업이익" in acnt:
            snapshot.setdefault("operating_income_q", curr)
            snapshot.setdefault("op_income_yoy", _calc_growth_rate(curr, yoy_base))
        elif "당기순이익" in acnt or "분기순이익" in acnt:
            snapshot.setdefault("net_income_q", curr)
            snapshot.setdefault("net_income", curr)
            snapshot.setdefault("net_income_yoy", _calc_growth_rate(curr, yoy_base))

    return snapshot


def fetch_previous_quarter_income(dart, stock_code, bsns_year, reprt_code):
    """이전 분기 손익(영업이익/순이익) 스냅샷."""
    prev_report_code = PREV_REPORT_CODE_MAP.get(reprt_code)
    if not prev_report_code:
        return {}

    prev_df = _fetch_finstate_all_with_retry(
        dart, stock_code, bsns_year, reprt_code=prev_report_code, fs_div="CFS"
    )
    if prev_df is None or (hasattr(prev_df, "empty") and prev_df.empty):
        prev_df = _fetch_finstate_all_with_retry(
            dart, stock_code, bsns_year, reprt_code=prev_report_code, fs_div="OFS"
        )
    return _extract_income_snapshot(prev_df)


def fetch_detail_accounts(dart, stock_code, bsns_year, reprt_code="11011"):
    """dart.finstate_all로 세부 계정 조회.
    현금, 유형자산, 감가상각비, CAPEX, 법인세비용, 이자비용.
    """
    df = _fetch_finstate_all_with_retry(dart, stock_code, bsns_year, reprt_code, fs_div="CFS")
    if df is None or (hasattr(df, 'empty') and df.empty):
        df = _fetch_finstate_all_with_retry(dart, stock_code, bsns_year, reprt_code, fs_div="OFS")

    if df is None or (hasattr(df, 'empty') and df.empty):
        return {}

    detail = _extract_income_snapshot(df)
    for _, row in df.iterrows():
        acnt = str(row.get("account_nm", ""))
        sj = str(row.get("sj_nm", ""))
        amt = _parse_amount(row.get("thstrm_amount", ""))

        if "현금및현금성자산" in acnt or "현금 및 현금성자산" in acnt:
            if sj == "재무상태표":
                detail["cash"] = amt
        elif acnt == "유형자산" and sj == "재무상태표":
            detail["tangible_assets"] = amt
        elif acnt == "매출총이익" and sj in ("손익계산서", "포괄손익계산서"):
            detail.setdefault("gross_profit", amt)
        elif "감가상각비" in acnt:
            detail.setdefault("depreciation", amt)
        elif acnt == "영업활동현금흐름" and sj == "현금흐름표":
            detail["operating_cash_flow"] = amt
        elif "유형자산의 취득" in acnt or "유형자산의취득" in acnt:
            detail["capex"] = abs(amt)  # 투자활동은 음수일 수 있음
        elif "법인세비용" == acnt or "법인세비용(수익)" == acnt:
            if sj in ("손익계산서", "포괄손익계산서"):
                detail.setdefault("tax_expense", amt)
        elif "이자비용" in acnt:
            detail.setdefault("interest_expense", amt)
        elif acnt == "단기차입금" and sj == "재무상태표":
            detail["short_term_borrowings"] = amt
        elif acnt == "장기차입금" and sj == "재무상태표":
            detail["long_term_borrowings"] = amt
        elif acnt == "이익잉여금" and sj == "재무상태표":
            detail.setdefault("retained_earnings", amt)
        elif acnt == "매출액" and sj in ("손익계산서", "포괄손익계산서"):
            detail.setdefault("quarterly_revenue", amt)

    if "short_term_borrowings" in detail or "long_term_borrowings" in detail:
        detail["borrowings"] = (
            detail.get("short_term_borrowings", 0)
            + detail.get("long_term_borrowings", 0)
        )

    # 분기 OCF/CAPEX: finstate_all에서 추출한 값을 그대로 사용
    if "operating_cash_flow" in detail:
        detail.setdefault("quarterly_ocf", detail["operating_cash_flow"])
    if "capex" in detail:
        detail.setdefault("quarterly_capex", detail["capex"])

    return detail


def save_financials(conn, bsns_year, financials_data):
    """재무데이터 일괄 저장."""
    for stock_code, info in financials_data.items():
        conn.execute("""
            INSERT INTO financials (
                stock_code, bsns_year, revenue, operating_income,
                total_assets, current_assets, current_liabilities,
                cash, tangible_assets, total_debt,
                operating_cash_flow, depreciation, capex, tax_expense, interest_expense,
                gross_profit, net_income, short_term_borrowings, long_term_borrowings,
                op_income_yoy, net_income_yoy, op_income_qoq, net_income_qoq,
                quarterly_revenue, quarterly_ocf, quarterly_capex, retained_earnings
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(stock_code, bsns_year) DO UPDATE SET
                revenue=excluded.revenue,
                operating_income=excluded.operating_income,
                total_assets=excluded.total_assets,
                current_assets=excluded.current_assets,
                current_liabilities=excluded.current_liabilities,
                cash=excluded.cash,
                tangible_assets=excluded.tangible_assets,
                total_debt=excluded.total_debt,
                operating_cash_flow=excluded.operating_cash_flow,
                depreciation=excluded.depreciation,
                capex=excluded.capex,
                tax_expense=excluded.tax_expense,
                interest_expense=excluded.interest_expense,
                gross_profit=excluded.gross_profit,
                net_income=excluded.net_income,
                short_term_borrowings=excluded.short_term_borrowings,
                long_term_borrowings=excluded.long_term_borrowings,
                op_income_yoy=excluded.op_income_yoy,
                net_income_yoy=excluded.net_income_yoy,
                op_income_qoq=excluded.op_income_qoq,
                net_income_qoq=excluded.net_income_qoq,
                quarterly_revenue=excluded.quarterly_revenue,
                quarterly_ocf=excluded.quarterly_ocf,
                quarterly_capex=excluded.quarterly_capex,
                retained_earnings=excluded.retained_earnings
        """, (
            stock_code, bsns_year,
            info.get("revenue", 0), info.get("operating_income", 0),
            info.get("total_assets", 0), info.get("current_assets", 0),
            info.get("current_liabilities", 0), info.get("cash", 0),
            info.get("tangible_assets", 0), info.get("total_debt", 0),
            info.get("operating_cash_flow", 0), info.get("depreciation", 0),
            info.get("capex", 0), info.get("tax_expense", 0),
            info.get("interest_expense", 0),
            info.get("gross_profit", 0), info.get("net_income", 0),
            info.get("short_term_borrowings", 0), info.get("long_term_borrowings", 0),
            info.get("op_income_yoy"), info.get("net_income_yoy"),
            info.get("op_income_qoq"), info.get("net_income_qoq"),
            info.get("quarterly_revenue"), info.get("quarterly_ocf"),
            info.get("quarterly_capex"), info.get("retained_earnings"),
        ))
    conn.commit()
    print(f"  → {len(financials_data)}개 재무데이터 저장 ({bsns_year})")


def fetch_and_save_volatility(conn, bsns_year, targets):
    """pykrx로 종목별 1년간 일별 종가 → 연환산 변동성 계산 후 DB 저장."""
    start = f"{bsns_year}0101"
    end = f"{bsns_year}1231"
    saved = 0
    for i, sc in enumerate(targets):
        try:
            df = krx.get_market_ohlcv(start, end, sc)
            if df is None or df.empty:
                continue
            prices = df["종가"].tolist()
            vol = calc_volatility(prices)
            if vol is not None:
                conn.execute("""
                    UPDATE financials SET price_volatility = ?
                    WHERE stock_code = ? AND bsns_year = ?
                """, (vol, sc, bsns_year))
                saved += 1
        except Exception:
            pass
        if (i + 1) % 100 == 0:
            print(f"    변동성 {i+1}/{len(targets)} ({saved}개 저장)")
        time.sleep(0.2)
    conn.commit()
    print(f"  → {saved}개 변동성 저장 ({bsns_year})")


def run(years=None, limit=None):
    """전체 데이터 수집 파이프라인.

    years: 수집할 사업연도 리스트 (기본: ["2023", "2024"])
    limit: 종목 수 제한 (None=전체, 테스트용)
    """
    if years is None:
        years = ["2023", "2024"]

    dart = OpenDartReader(get_api_key())
    conn = init_db()

    # 1) 상장기업 목록
    print("[1] 상장기업 목록 수집...")
    companies_df = fetch_company_list(dart)
    save_companies(conn, companies_df)

    dart_codes = set(companies_df["stock_code"].str.strip().tolist())

    for year in years:
        print(f"\n===== {year}년 데이터 수집 =====")

        # 연도별 reprt_code 결정: 2025년은 3분기보고서, 그 외 사업보고서
        if year == "2025":
            reprt_code = "11014"  # 3분기보고서
            mcap_date = f"{year}0930"
            print(f"  reprt_code={reprt_code} (3분기), 시총기준일={mcap_date}")
        else:
            reprt_code = "11011"  # 사업보고서
            mcap_date = f"{year}1230"

        # 2) 시가총액 + 상장주식수 → 양쪽 모두 있는 종목만 대상
        print(f"[2] 시가총액/상장주식수 수집 ({year})...")
        market_caps = fetch_market_caps(mcap_date)
        save_market_caps(conn, year, market_caps)
        fundamentals = fetch_market_fundamentals(mcap_date)
        save_market_fundamentals(conn, year, fundamentals)
        shares = fetch_shares_outstanding(year)
        save_shares(conn, year, shares)

        # DART에도 있고 KRX에도 있는 종목, 시가총액 큰 순서로
        targets = sorted(
            [sc for sc in market_caps if sc in dart_codes],
            key=lambda sc: market_caps[sc], reverse=True,
        )
        if limit:
            targets = targets[:limit]
        print(f"  대상 종목: {len(targets)}개")

        # 3) 재무데이터 (finstate + finstate_all 개별 호출)
        print(f"[3] 재무데이터 수집 ({year}, {len(targets)}개 종목)...")
        all_data = {}
        errors = 0
        for i, sc in enumerate(targets):
            # 주요 항목
            info = fetch_finstate(dart, sc, int(year), reprt_code=reprt_code)
            if info is None:
                errors += 1
                continue

            # 세부 항목
            detail = fetch_detail_accounts(dart, sc, int(year), reprt_code=reprt_code)
            info.update(detail)

            # QOQ 성장률은 이전 분기와 비교 (Q3/H1에서만 계산)
            prev_income = fetch_previous_quarter_income(dart, sc, int(year), reprt_code=reprt_code)
            if prev_income:
                prev_op = prev_income.get("operating_income_q")
                prev_net = prev_income.get("net_income_q")
                curr_op = info.get("operating_income_q")
                curr_net = info.get("net_income_q")
                info["op_income_qoq"] = _calc_growth_rate(curr_op, prev_op) if curr_op is not None else None
                info["net_income_qoq"] = _calc_growth_rate(curr_net, prev_net) if curr_net is not None else None

            all_data[sc] = info

            if (i + 1) % 100 == 0:
                print(f"    {i+1}/{len(targets)} ({len(all_data)}개 성공, {errors}개 실패)")

        save_financials(conn, year, all_data)
        print(f"  최종: {len(all_data)}개 성공, {errors}개 실패")

        # 4) 변동성 수집
        print(f"[4] 주가 변동성 수집 ({year}, {len(targets)}개 종목)...")
        fetch_and_save_volatility(conn, year, targets)

    conn.close()
    print("\n완료!")


if __name__ == "__main__":
    years = sys.argv[1:] if len(sys.argv) > 1 else None
    run(years=years)
