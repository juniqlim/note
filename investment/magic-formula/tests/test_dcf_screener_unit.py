import pytest

from screener import (
    calculate_fcf,
    calculate_fcf_from_ocf,
    calculate_dcf_value,
    dcf_from_financials,
    screen_dcf,
)


class TestCalculateFcf:
    def test_basic(self):
        # EBIT*(1-t) + dep - capex - wc_change
        # 100*(1-0.2) + 20 - 30 - 10 = 80 + 20 - 30 - 10 = 60
        assert calculate_fcf(100, 0.2, 20, 30, 10) == 60

    def test_zero_tax(self):
        assert calculate_fcf(100, 0, 20, 30, 0) == 90


class TestCalculateFcfFromOcf:
    def test_basic(self):
        assert calculate_fcf_from_ocf(200, 50) == 150


class TestCalculateDcfValue:
    def test_positive_fcfs(self):
        fcfs = [100, 105, 110]
        wacc = 0.10
        tg = 0.02
        result = calculate_dcf_value(fcfs, wacc, tg)
        assert result > 0

    def test_terminal_value_dominates(self):
        fcfs = [10, 10, 10, 10, 10]
        result = calculate_dcf_value(fcfs, 0.10, 0.02)
        # PV of FCFs is small; terminal value should dominate
        pv_fcfs = sum(10 / 1.1 ** i for i in range(1, 6))
        assert result > pv_fcfs


class TestDcfFromFinancials:
    def _base_financial(self):
        return {
            "operating_income": 100_0000_0000,  # 100억
            "tax_expense": 22_0000_0000,
            "depreciation": 10_0000_0000,
            "capex": 15_0000_0000,
            "operating_cash_flow": 90_0000_0000,
            "current_assets": 200_0000_0000,
            "current_liabilities": 80_0000_0000,
            "cash": 50_0000_0000,
            "total_debt": 100_0000_0000,
            "shares_outstanding": 1_000_000,
            "market_cap": 500_0000_0000,
        }

    def test_returns_result(self):
        f = self._base_financial()
        result = dcf_from_financials(f)
        assert result is not None
        assert "dcf_price" in result
        assert "upside" in result
        assert "fcf" in result

    def test_no_shares_returns_none(self):
        f = self._base_financial()
        f["shares_outstanding"] = 0
        assert dcf_from_financials(f) is None

    def test_ocf_method_preferred(self):
        f = self._base_financial()
        result = dcf_from_financials(f)
        assert result["fcf_method"] == "OCF"
        assert result["fcf"] == 90_0000_0000 - 15_0000_0000  # OCF - CAPEX

    def test_ebit_method_when_no_ocf(self):
        f = self._base_financial()
        f["operating_cash_flow"] = 0
        result = dcf_from_financials(f)
        assert result["fcf_method"] == "EBIT"

    def test_upside_positive_when_dcf_above_market(self):
        f = self._base_financial()
        f["market_cap"] = 100_0000_0000  # 매우 낮은 시총
        result = dcf_from_financials(f, growth_rate=0.10)
        assert result["upside"] > 0

    def test_upside_negative_when_dcf_below_market(self):
        f = self._base_financial()
        f["market_cap"] = 100000_0000_0000  # 매우 높은 시총
        result = dcf_from_financials(f)
        assert result["upside"] < 0
