import math

import pytest

from ultra_screener import (
    calc_inverse_per,
    calc_inverse_pbr,
    calc_inverse_pfcr,
    calc_inverse_psr,
    calc_gpa,
    calc_asset_growth,
    calc_op_borrowing_ratio,
    calc_new_f_score,
    assign_percentile_ranks,
    rank_ultra,
)


# --- 개별 지표 계산 ---

class TestCalcInversePer:
    def test_normal(self):
        assert pytest.approx(calc_inverse_per(10.0)) == 0.1

    def test_zero_returns_none(self):
        assert calc_inverse_per(0) is None

    def test_none_returns_none(self):
        assert calc_inverse_per(None) is None

    def test_negative(self):
        assert calc_inverse_per(-5.0) is None


class TestCalcInversePbr:
    def test_normal(self):
        assert pytest.approx(calc_inverse_pbr(2.0)) == 0.5

    def test_zero_returns_none(self):
        assert calc_inverse_pbr(0) is None

    def test_none_returns_none(self):
        assert calc_inverse_pbr(None) is None


class TestCalcInversePsr:
    def test_normal(self):
        # market_cap=1000, quarterly_revenue=200 → PSR=5 → 1/PSR=0.2
        assert pytest.approx(calc_inverse_psr(1000, 200)) == 0.2

    def test_zero_market_cap(self):
        assert calc_inverse_psr(0, 200) is None

    def test_zero_revenue(self):
        assert calc_inverse_psr(1000, 0) is None

    def test_none_revenue(self):
        assert calc_inverse_psr(1000, None) is None


class TestCalcInversePfcr:
    def test_normal(self):
        # market_cap=1000, ocf=300, capex=100 → FCF=200 → PFCR=5 → 1/PFCR=0.2
        assert pytest.approx(calc_inverse_pfcr(1000, 300, 100)) == 0.2

    def test_negative_fcf(self):
        assert calc_inverse_pfcr(1000, 100, 300) is None

    def test_zero_market_cap(self):
        assert calc_inverse_pfcr(0, 300, 100) is None


class TestCalcGpa:
    def test_normal(self):
        assert pytest.approx(calc_gpa(500, 2000)) == 0.25

    def test_zero_assets(self):
        assert calc_gpa(500, 0) is None

    def test_none_gross_profit(self):
        assert calc_gpa(None, 2000) is None


class TestCalcAssetGrowth:
    def test_positive_growth(self):
        assert pytest.approx(calc_asset_growth(1200, 1000)) == 0.2

    def test_negative_growth(self):
        assert pytest.approx(calc_asset_growth(800, 1000)) == -0.2

    def test_zero_prev(self):
        assert calc_asset_growth(1000, 0) is None

    def test_none_prev(self):
        assert calc_asset_growth(1000, None) is None


class TestCalcOpBorrowingRatio:
    def test_both_increase(self):
        # 영업이익 100→150 (+50%), 차입금 200→240 (+20%) → 50/20=2.5
        result = calc_op_borrowing_ratio(150, 100, 240, 200)
        assert pytest.approx(result) == 2.5

    def test_borrowing_no_change(self):
        # 차입금 변동률 0 → None
        assert calc_op_borrowing_ratio(150, 100, 200, 200) is None

    def test_no_prev_op(self):
        assert calc_op_borrowing_ratio(150, 0, 240, 200) is None


# --- 신F-스코어 ---

def _make_stock(**overrides):
    """테스트용 기본 stock dict."""
    base = {
        "operating_income": 100,
        "prev_operating_income": 80,
        "net_income": 50,
        "prev_net_income": 40,
        "operating_cash_flow": 120,
        "prev_operating_cash_flow": 100,
        "gross_profit": 220,
        "prev_gross_profit": 180,
        "revenue": 1000,
        "prev_revenue": 900,
        "total_assets": 5000,
        "prev_total_assets": 4800,
        "retained_earnings": 300,
        "prev_retained_earnings": 250,
        "total_debt": 2000,
        "prev_total_debt": 2100,
        "current_assets": 1500,
        "current_liabilities": 800,
        "prev_current_assets": 1400,
        "prev_current_liabilities": 750,
    }
    base.update(overrides)
    return base


class TestCalcNewFScore:
    def test_perfect_score(self):
        # 모든 항목 개선 → 9점
        s = _make_stock()
        assert calc_new_f_score(s) == 9

    def test_all_bad(self):
        s = _make_stock(
            operating_income=-10,
            prev_operating_income=80,
            net_income=-5,
            prev_net_income=40,
            operating_cash_flow=-10,
            prev_operating_cash_flow=100,
            gross_profit=100,
            prev_gross_profit=200,
            revenue=800,
            prev_revenue=900,
            total_assets=6000,
            prev_total_assets=4800,
            retained_earnings=200,
            prev_retained_earnings=300,
            total_debt=2500,
            prev_total_debt=2000,
            # 유동비율 악화
            current_assets=800,
            current_liabilities=1000,
            prev_current_assets=1400,
            prev_current_liabilities=750,
        )
        assert calc_new_f_score(s) == 0

    def test_partial_missing_data(self):
        # prev 데이터 없으면 해당 항목 0점, 나머지 계산
        s = _make_stock(prev_operating_income=None, prev_net_income=None)
        score = calc_new_f_score(s)
        assert 0 <= score <= 9


# --- 백분위 순위 ---

class TestAssignPercentileRanks:
    def test_descending_high_is_better(self):
        stocks = [{"val": 10}, {"val": 30}, {"val": 20}]
        result = assign_percentile_ranks(stocks, "val", descending=True)
        # 30이 1등(가장 낮은 순위값), 10이 3등
        ranks = {s["val"]: s["val_rank"] for s in result}
        assert ranks[30] < ranks[10]

    def test_ascending_low_is_better(self):
        # 자산성장률/변동성: 낮을수록 좋음
        stocks = [{"val": 0.5}, {"val": 0.1}, {"val": 0.3}]
        result = assign_percentile_ranks(stocks, "val", descending=False)
        ranks = {s["val"]: s["val_rank"] for s in result}
        assert ranks[0.1] < ranks[0.5]

    def test_none_values_get_worst_rank(self):
        stocks = [{"val": 10}, {"val": None}, {"val": 20}]
        result = assign_percentile_ranks(stocks, "val", descending=True)
        none_stock = [s for s in result if s["val"] is None][0]
        assert none_stock["val_rank"] == len(stocks)


# --- 종합 순위 ---

class TestRankUltra:
    def test_filters_low_f_score(self):
        stocks = [
            _make_stock(name="Good", stock_code="001", per=5.0, pbr=1.0,
                        market_cap=1000, quarterly_revenue=200,
                        quarterly_ocf=300, quarterly_capex=100,
                        price_volatility=0.3),
            _make_stock(name="Bad", stock_code="002", per=5.0, pbr=1.0,
                        market_cap=1000, quarterly_revenue=200,
                        quarterly_ocf=300, quarterly_capex=100,
                        price_volatility=0.3,
                        # F-스코어 0점 만들기
                        operating_income=-10, prev_operating_income=80,
                        net_income=-5, prev_net_income=40,
                        operating_cash_flow=-10, prev_operating_cash_flow=100,
                        gross_profit=100, prev_gross_profit=200,
                        revenue=800, prev_revenue=900,
                        total_assets=6000, prev_total_assets=4800,
                        retained_earnings=200, prev_retained_earnings=300,
                        total_debt=2500, prev_total_debt=2000,
                        current_assets=800, current_liabilities=1000,
                        prev_current_assets=1400, prev_current_liabilities=750),
        ]
        result = rank_ultra(stocks)
        names = [s["name"] for s in result]
        assert "Good" in names
        assert "Bad" not in names

    def test_ranking_order(self):
        # 더 좋은 지표 → 더 낮은 합산 순위
        good = _make_stock(name="BetterVal", stock_code="A01",
                           per=3.0, pbr=0.5, market_cap=500,
                           quarterly_revenue=300, quarterly_ocf=400,
                           quarterly_capex=50, price_volatility=0.1)
        mediocre = _make_stock(name="WorseVal", stock_code="A02",
                               per=30.0, pbr=5.0, market_cap=5000,
                               quarterly_revenue=100, quarterly_ocf=150,
                               quarterly_capex=100, price_volatility=0.8)
        result = rank_ultra([good, mediocre])
        assert len(result) >= 1
        if len(result) == 2:
            assert result[0]["name"] == "BetterVal"
