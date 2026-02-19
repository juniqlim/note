"""DART + pykrx 데이터 수집 → SQLite 저장."""

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


def get_api_key():
    return Path(API_KEY_PATH).read_text().strip()


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
            shares_outstanding INTEGER,
            PRIMARY KEY (stock_code, bsns_year)
        );
    """)
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


def fetch_market_caps(date_str):
    """pykrx 전 종목 시가총액. {종목코드: 시가총액}."""
    df = _find_trading_date(date_str)
    return {code: int(row["시가총액"]) for code, row in df.iterrows()}


def save_market_caps(conn, bsns_year, market_caps):
    for stock_code, mcap in market_caps.items():
        conn.execute("""
            INSERT INTO financials (stock_code, bsns_year, market_cap)
            VALUES (?, ?, ?)
            ON CONFLICT(stock_code, bsns_year) DO UPDATE SET market_cap = ?
        """, (stock_code, bsns_year, mcap, mcap))
    conn.commit()
    print(f"  → {len(market_caps)}개 시가총액 저장 ({bsns_year})")


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


def _parse_amount(val):
    """문자열 금액 → int."""
    if not val or val == "":
        return 0
    try:
        return int(str(val).replace(",", "").replace(" ", ""))
    except (ValueError, TypeError):
        return 0


def fetch_finstate(dart, stock_code, bsns_year):
    """dart.finstate로 주요 재무항목 조회.
    유동자산, 유동부채, 자산총계, 부채총계, 매출액, 영업이익 등.
    """
    try:
        df = dart.finstate(stock_code, bsns_year)
        time.sleep(CALL_DELAY)
    except Exception as e:
        time.sleep(CALL_DELAY)
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

    return info if "operating_income" in info else None


def fetch_detail_accounts(dart, stock_code, bsns_year):
    """dart.finstate_all로 세부 계정 조회.
    현금, 유형자산, 감가상각비, CAPEX, 법인세비용, 이자비용.
    """
    try:
        df = dart.finstate_all(stock_code, bsns_year, fs_div="CFS")
        time.sleep(CALL_DELAY)
    except Exception:
        try:
            df = dart.finstate_all(stock_code, bsns_year, fs_div="OFS")
            time.sleep(CALL_DELAY)
        except Exception:
            time.sleep(CALL_DELAY)
            return {}

    if df is None or (hasattr(df, 'empty') and df.empty):
        return {}

    detail = {}
    for _, row in df.iterrows():
        acnt = str(row.get("account_nm", ""))
        sj = str(row.get("sj_nm", ""))
        amt = _parse_amount(row.get("thstrm_amount", ""))

        if "현금및현금성자산" in acnt or "현금 및 현금성자산" in acnt:
            if sj == "재무상태표":
                detail["cash"] = amt
        elif acnt == "유형자산" and sj == "재무상태표":
            detail["tangible_assets"] = amt
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

    return detail


def save_financials(conn, bsns_year, financials_data):
    """재무데이터 일괄 저장."""
    for stock_code, info in financials_data.items():
        conn.execute("""
            INSERT INTO financials (
                stock_code, bsns_year, revenue, operating_income,
                total_assets, current_assets, current_liabilities,
                cash, tangible_assets, total_debt,
                operating_cash_flow, depreciation, capex, tax_expense, interest_expense
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(stock_code, bsns_year) DO UPDATE SET
                revenue=?, operating_income=?,
                total_assets=?, current_assets=?, current_liabilities=?,
                cash=?, tangible_assets=?, total_debt=?,
                operating_cash_flow=?, depreciation=?, capex=?, tax_expense=?, interest_expense=?
        """, (
            stock_code, bsns_year,
            info.get("revenue", 0), info.get("operating_income", 0),
            info.get("total_assets", 0), info.get("current_assets", 0),
            info.get("current_liabilities", 0), info.get("cash", 0),
            info.get("tangible_assets", 0), info.get("total_debt", 0),
            info.get("operating_cash_flow", 0), info.get("depreciation", 0),
            info.get("capex", 0), info.get("tax_expense", 0),
            info.get("interest_expense", 0),
            # UPDATE values
            info.get("revenue", 0), info.get("operating_income", 0),
            info.get("total_assets", 0), info.get("current_assets", 0),
            info.get("current_liabilities", 0), info.get("cash", 0),
            info.get("tangible_assets", 0), info.get("total_debt", 0),
            info.get("operating_cash_flow", 0), info.get("depreciation", 0),
            info.get("capex", 0), info.get("tax_expense", 0),
            info.get("interest_expense", 0),
        ))
    conn.commit()
    print(f"  → {len(financials_data)}개 재무데이터 저장 ({bsns_year})")


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

        # 2) 시가총액 + 상장주식수 → 양쪽 모두 있는 종목만 대상
        print(f"[2] 시가총액/상장주식수 수집 ({year})...")
        market_caps = fetch_market_caps(f"{year}1230")
        save_market_caps(conn, year, market_caps)
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
            info = fetch_finstate(dart, sc, int(year))
            if info is None:
                errors += 1
                continue

            # 세부 항목
            detail = fetch_detail_accounts(dart, sc, int(year))
            info.update(detail)
            all_data[sc] = info

            if (i + 1) % 100 == 0:
                print(f"    {i+1}/{len(targets)} ({len(all_data)}개 성공, {errors}개 실패)")

        save_financials(conn, year, all_data)
        print(f"  최종: {len(all_data)}개 성공, {errors}개 실패")

    conn.close()
    print("\n완료!")


if __name__ == "__main__":
    years = sys.argv[1:] if len(sys.argv) > 1 else None
    run(years=years)
