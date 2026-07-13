import unittest

from naver_research import extract_pdf_url, parse_list


LIST_HTML = """
<table><tr><th>종목명</th></tr>
<tr>
  <td>SK하이닉스</td>
  <td><a href="/research/company_read.naver?nid=93931&page=1">슈퍼 모멘텀</a></td>
  <td>대신증권</td>
  <td>1.2M</td>
  <td>26.07.07</td>
</tr>
<tr>
  <td>SK하이닉스</td>
  <td><a href="/research/company_read.naver?nid=93621&page=1">2Q26 영업이익 63.7 조원 전망</a></td>
  <td>iM증권</td>
  <td>0.9M</td>
  <td>26.06.22</td>
</tr>
</table>
"""

READ_HTML = """
<a href="https://stock.pstatic.net/stock-research/company/15/20260707_company_38726000.pdf">
<img src="https://ssl.pstatic.net/static/nfinance/btn_report.gif"></a>
"""

READ_HTML_NO_PDF = '<div class="view_sec">본문만 있고 첨부 없음</div>'


class ParseListTest(unittest.TestCase):
    def test_returns_nid_date_broker_title(self):
        reports = parse_list(LIST_HTML)

        self.assertEqual(
            reports,
            [
                (93931, "20260707", "대신증권", "슈퍼 모멘텀"),
                (93621, "20260622", "iM증권", "2Q26 영업이익 63.7 조원 전망"),
            ],
        )

    def test_filters_by_since(self):
        reports = parse_list(LIST_HTML, since="20260701")

        self.assertEqual([r[0] for r in reports], [93931])

    def test_returns_empty_when_no_rows(self):
        self.assertEqual(parse_list("<table></table>"), [])


class ExtractPdfUrlTest(unittest.TestCase):
    def test_finds_current_host(self):
        url = extract_pdf_url(READ_HTML)

        self.assertEqual(
            url,
            "https://stock.pstatic.net/stock-research/company/15/20260707_company_38726000.pdf",
        )

    def test_returns_none_when_no_attachment(self):
        self.assertIsNone(extract_pdf_url(READ_HTML_NO_PDF))


if __name__ == "__main__":
    unittest.main()
