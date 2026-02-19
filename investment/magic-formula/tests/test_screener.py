import pytest
from screener import (
    calculate_roic,
    calculate_earnings_yield,
    rank_stocks,
    calculate_fcf,
    calculate_dcf_value,
    backtest_dcf,
    dcf_from_financials,
)


# --- Magic Formula ---

class TestROIC:
    def test_basic(self):
        # ROIC = EBIT / (유동자산 - 유동부채 - 현금 + 유형자산)
        # 100 / (500 - 200 - 50 + 300) = 100 / 550 ≈ 0.1818
        result = calculate_roic(
            ebit=100, current_assets=500, current_liabilities=200,
            cash=50, tangible_assets=300,
        )
        assert pytest.approx(result, rel=1e-3) == 100 / 550

    def test_negative_invested_capital_returns_none(self):
        # 투하자본이 0 이하이면 의미 없음
        result = calculate_roic(
            ebit=100, current_assets=100, current_liabilities=200,
            cash=50, tangible_assets=10,
        )
        assert result is None

    def test_negative_ebit(self):
        result = calculate_roic(
            ebit=-50, current_assets=500, current_liabilities=200,
            cash=50, tangible_assets=300,
        )
        assert result < 0


class TestEarningsYield:
    def test_basic(self):
        # EY = EBIT / EV, EV = 시가총액 + 총부채 - 현금
        # 100 / (1000 + 300 - 50) = 100 / 1250 = 0.08
        result = calculate_earnings_yield(
            ebit=100, market_cap=1000, total_debt=300, cash=50,
        )
        assert pytest.approx(result, rel=1e-3) == 0.08

    def test_zero_ev_returns_none(self):
        result = calculate_earnings_yield(
            ebit=100, market_cap=0, total_debt=0, cash=0,
        )
        assert result is None


class TestRankStocks:
    def test_ranking_order(self):
        # A: ROIC=200/1100=0.18, EY=200/2400=0.08 → roic_rank=2, ey_rank=2 → 4
        # B: ROIC=300/950=0.32, EY=300/1250=0.24 → roic_rank=1, ey_rank=1 → 2
        # C: ROIC=50/670=0.07,  EY=50/3770=0.01  → roic_rank=3, ey_rank=3 → 6
        stocks = [
            {"name": "A", "ebit": 200, "current_assets": 1000,
             "current_liabilities": 300, "cash": 100, "tangible_assets": 500,
             "market_cap": 2000, "total_debt": 500},
            {"name": "B", "ebit": 300, "current_assets": 800,
             "current_liabilities": 200, "cash": 50, "tangible_assets": 400,
             "market_cap": 1000, "total_debt": 300},
            {"name": "C", "ebit": 50, "current_assets": 600,
             "current_liabilities": 100, "cash": 30, "tangible_assets": 200,
             "market_cap": 3000, "total_debt": 800},
        ]
        ranked = rank_stocks(stocks)
        assert ranked[0]["name"] == "B"

    def test_excludes_invalid_stocks(self):
        stocks = [
            {"name": "Good", "ebit": 100, "current_assets": 500,
             "current_liabilities": 200, "cash": 50, "tangible_assets": 300,
             "market_cap": 1000, "total_debt": 200},
            {"name": "Bad", "ebit": 100, "current_assets": 100,
             "current_liabilities": 200, "cash": 50, "tangible_assets": 10,
             "market_cap": 1000, "total_debt": 200},  # 투하자본 음수
        ]
        ranked = rank_stocks(stocks)
        assert len(ranked) == 1
        assert ranked[0]["name"] == "Good"


# --- DCF ---

class TestFCF:
    def test_basic(self):
        # FCF = EBIT * (1 - tax_rate) + depreciation - capex - wc_change
        # 100 * (1 - 0.25) + 30 - 40 - 10 = 75 + 30 - 40 - 10 = 55
        result = calculate_fcf(
            ebit=100, tax_rate=0.25, depreciation=30, capex=40, wc_change=10,
        )
        assert pytest.approx(result) == 55


class TestDCFValue:
    def test_basic(self):
        # 5년간 동일 FCF 100, 할인율 10%, 영구성장률 2%
        fcfs = [100, 100, 100, 100, 100]
        wacc = 0.10
        terminal_growth = 0.02
        result = calculate_dcf_value(fcfs, wacc, terminal_growth)

        # Terminal Value = FCF[-1] * (1+g) / (wacc - g) = 100*1.02/0.08 = 1275
        # PV of FCFs + PV of TV
        expected_pv_fcfs = sum(100 / (1.1 ** i) for i in range(1, 6))
        tv = 100 * 1.02 / (0.10 - 0.02)
        expected_pv_tv = tv / (1.1 ** 5)
        expected = expected_pv_fcfs + expected_pv_tv
        assert pytest.approx(result, rel=1e-3) == expected

    def test_growing_fcf(self):
        fcfs = [100, 110, 121, 133, 146]
        result = calculate_dcf_value(fcfs, wacc=0.10, terminal_growth=0.02)
        assert result > 0


class TestBacktestDCF:
    def test_basic(self):
        # 과거 연도별 재무데이터 → DCF 적정가 vs 실제 주가
        yearly_data = {
            "2021": {
                "ebit": 100, "tax_rate": 0.25, "depreciation": 30,
                "capex": 40, "wc_change": 10, "total_debt": 200,
                "cash": 50, "shares": 100,
                "growth_rate": 0.05, "actual_price": 8000,
            },
            "2022": {
                "ebit": 120, "tax_rate": 0.25, "depreciation": 35,
                "capex": 45, "wc_change": 5, "total_debt": 180,
                "cash": 60, "shares": 100,
                "growth_rate": 0.05, "actual_price": 9500,
            },
        }
        results = backtest_dcf(yearly_data, wacc=0.10, terminal_growth=0.02)
        assert len(results) == 2
        for r in results:
            assert "year" in r
            assert "dcf_price" in r
            assert "actual_price" in r
            assert "upside" in r  # (dcf_price - actual_price) / actual_price


class TestDCFFromFinancials:
    """DB에서 읽은 재무데이터 dict로 DCF 적정 주가를 구하는 통합 함수 테스트."""

    def test_basic(self):
        # 삼성전자 2024 스케일 축소 (단위: 억원)
        financial = {
            "operating_income": 1000,   # EBIT
            "tax_expense": 250,         # 유효세율 25%
            "depreciation": 300,
            "capex": 400,
            "current_assets": 5000,
            "current_liabilities": 2000,
            "cash": 1000,
            "total_debt": 3000,
            "shares_outstanding": 100,
            "market_cap": 50000,
        }
        result = dcf_from_financials(financial, growth_rate=0.05, wacc=0.10, terminal_growth=0.02)

        assert "dcf_price" in result
        assert "current_price" in result
        assert "upside" in result
        assert "fcf" in result
        assert result["dcf_price"] > 0
        assert result["current_price"] == 50000 / 100  # market_cap / shares

    def test_negative_fcf(self):
        """FCF가 음수면 DCF가 의미 없으므로 표시."""
        financial = {
            "operating_income": 100,
            "tax_expense": 25,
            "depreciation": 10,
            "capex": 500,  # CAPEX >> EBIT → FCF 음수
            "current_assets": 1000,
            "current_liabilities": 200,
            "cash": 100,
            "total_debt": 300,
            "shares_outstanding": 100,
            "market_cap": 10000,
        }
        result = dcf_from_financials(financial, growth_rate=0.05, wacc=0.10, terminal_growth=0.02)
        assert result["fcf"] < 0

    def test_zero_shares_returns_none(self):
        financial = {
            "operating_income": 100,
            "tax_expense": 25,
            "depreciation": 30,
            "capex": 40,
            "current_assets": 500,
            "current_liabilities": 200,
            "cash": 50,
            "total_debt": 200,
            "shares_outstanding": 0,
            "market_cap": 10000,
        }
        result = dcf_from_financials(financial, growth_rate=0.05, wacc=0.10, terminal_growth=0.02)
        assert result is None

    def test_wc_change_from_two_years(self):
        """2개년 데이터가 있으면 운전자본 변동을 계산."""
        prev = {
            "current_assets": 4000, "current_liabilities": 1800, "cash": 800,
        }
        curr = {
            "operating_income": 1000, "tax_expense": 250,
            "depreciation": 300, "capex": 400,
            "current_assets": 5000, "current_liabilities": 2000, "cash": 1000,
            "total_debt": 3000, "shares_outstanding": 100, "market_cap": 50000,
        }
        result = dcf_from_financials(curr, growth_rate=0.05, wacc=0.10, terminal_growth=0.02, prev_financial=prev)

        # WC = (유동자산-현금) - 유동부채
        # prev WC = (4000-800) - 1800 = 1400
        # curr WC = (5000-1000) - 2000 = 2000
        # wc_change = 2000 - 1400 = 600
        expected_fcf = 1000 * 0.75 + 300 - 400 - 600  # = 50
        assert pytest.approx(result["fcf"]) == expected_fcf
