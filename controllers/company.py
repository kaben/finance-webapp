from applications.finance.modules import get_pages, get_pagination, filter_and_order_query_by_field_descending
import itertools
# coding: utf8
# try something like
def index():
  stock_symbol = request.vars.get("stock_symbol")
  start = int(request.vars.get("start", 0))
  num = min(1000, max(1, int(request.vars.get("num", 4))))
  url_vars = dict(
    stock_symbol=stock_symbol,
    start=start,
    num=num,
  )

  company = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.stock_symbol==stock_symbol).first()

  # Construct left sidebar menu.
  navitems = response.sidebar_navitems.copy()
  navitems.enabled_items.insert(0, "company")
  navitems.company.expand = True
  navitems.company.summary.active = True
  navitems.company.summary.helper = URL("company", "index", vars=url_vars)
  navitems.company.financials.helper = URL("company", "financials", vars=url_vars)
  sidebar_menu = DIV(MENU(get_menuitems(navitems)), _class="nav-menu")

  return dict(
    message="hello from company.py",
    sidebar_menu=sidebar_menu,
    company=company,
  )

financial_fields = (
  "period_ending",
  "quarter_ending",
  "quarter",
  "accounting_changes",
  "accounts_payable",
  "accounts_receivable",
  "accumulated_amortization",
  "additional_income_or_expense_items",
  "adjustments_to_net_income",
  "capital_expenditures",
  "capital_surpolus",
  "cash_and_equivalents",
  "common_stocks",
  "cost_of_revenue",
  "deferred_asset_charges",
  "deferred_liability_charges",
  "depreciation",
  "discontinued_operations",
  "dividends_paid",
  "earnings_before_interest_and_tax",
  "earnings_before_tax",
  "effect_of_exchange_rate",
  "equity_earnings_unconsolidated_subsidiary",
  "extraordinary_items",
  "fixed_assets",
  "goodwill",
  "gross_profit",
  "income_tax",
  "intangible_assets",
  "interest_expense",
  "inventory",
  "investments",
  "liabilities",
  "long_term_debt",
  "long_term_investments",
  "minority_interest",
  "misc_stocks",
  "negative_goodwill",
  "net_borrowing",
  "net_cash_flow",
  "net_operating_cash_flow",
  "net_cash_flow_from_financing",
  "net_cash_flow_from_investing",
  "net_income",
  "net_income_adjustments",
  "shareholder_net_income",
  "net_income_from_continuing_operations",
  "net_receivables",
  "non_recurring_items",
  "operating_income",
  "other_assets",
  "other_current_assets",
  "other_current_liabilities",
  "other_equity",
  "other_financing_activities",
  "other_investing_activities",
  "other_items",
  "other_liabilities",
  "other_operating_activities",
  "other_operating_items",
  "preferred_stocks",
  "redeemable_stocks",
  "research_and_development",
  "retained_earnings",
  "sale_and_purchase_of_stock",
  "sales_general_and_admin",
  "short_term_debt",
  "short_term_investments",
  "total_assets",
  "total_current_assets",
  "total_current_liabilities",
  "total_equity",
  "total_liabilities",
  "total_revenue",
  "treasury_stock",
  "eps",
  "shares_outstanding",
  "gross_margin",
  "net_margin",
  "cash_to_debt_ratio",
  "net_cash",
  "foolish_flow_ratio",
  "cash_king_margin",
)

def financials():
  # Uniquely identify requested company by stock symbol.
  stock_symbol = request.vars.get("stock_symbol")
  # Offset for financial records to view.
  start = int(request.vars.get("start", 0))
  # Number of financial records to view.
  num = min(1000, max(1, int(request.vars.get("num", 4))))
  # Whether to view quarterly- or annual-period records.
  period = request.vars.get("period", "quarterly")
  if period != "quarterly": period = "annual"
  # Dict for constructing URL with request arguments.
  url_vars = dict(
    stock_symbol=stock_symbol,
    start=start,
    num=num,
    period=period,
  )

  # Query database for unique company with exact match for requested stock symbol.
  company = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.stock_symbol==stock_symbol).one()
  if company:
    # Query database for financials for this company.
    financials_q = orm.session.query(orm.NasdaqCompanyFinancials).filter(orm.NasdaqCompanyFinancials.company == company)
    # Filter and reverse-order financials by either annual or quarterly period ending.
    financials_q = filter_and_order_query_by_field_descending(
      financials_q,
        orm.NasdaqCompanyFinancials.quarter_ending
      if period == "quarterly" else
        orm.NasdaqCompanyFinancials.period_ending
    )
    # How many financials records did we find?
    financials_count = financials_q.count()
    # Limit and offset number of records to view.
    financials_q = financials_q.offset(start).limit(num)
    # Extract rows of financial data from financial objects.
    financials = [[getattr(financial, key) for key in financial_fields] for financial in financials_q]
    # Insert corresponding field names at top row.
    financials.insert(0, financial_fields)
    # Convert rows to columns.
    financials = itertools.izip_longest(*financials, fillvalue=None)
    # Filter-out empty rows.
    financials = [row for row in financials if filter(None, row[1:])]
  else:
    # No company found; return empty data.
    financials = tuple()
    financials_count = 0
    data = tuple()

  # Get list of page numbers to link to for more financials data..
  pagination_href_fmt = u"?stock_symbol={stock_symbol}&period={period}&start={offset}&num={num}".format(
    stock_symbol=stock_symbol,
    period=period,
    num=num,
    offset=u"{}"
  )
  current_page, pages = get_pages(start, financials_count, num)
  pagination = get_pagination(pagination_href_fmt, pages, current_page, num)

  # Setup a link to switch from quarterly to annual period view (and v.v.).
  switch_view_period_vars = url_vars.copy()
  switch_view_period_vars["period"] = "annual" if period == "quarterly" else "quarterly"
  switch_view_period_vars["start"]=0
  switch_view_period_link = A("{period} view".format(period=switch_view_period_vars["period"]), _href=URL("company", "financials", vars=switch_view_period_vars))

  # Construct left sidebar menu.
  navitems = response.sidebar_navitems.copy()
  navitems.enabled_items.insert(0, "company")
  navitems.company.expand = True
  navitems.company.financials.active = True
  navitems.company.summary.helper = URL("company", "index", vars=url_vars)
  navitems.company.financials.helper = URL("company", "financials", vars=url_vars)
  sidebar_menu = DIV(MENU(get_menuitems(navitems)), _class="nav-menu")

  return dict(
    message="hello from company.py",
    sidebar_menu=sidebar_menu,
    company=company,
    financials=financials,
    current_financial_stmt=start+1,
    through_financial_stmt=min(start+num, financials_count),
    financials_count=financials_count,
    pagination=pagination,
    current_page=current_page,
    period=period.capitalize(),
    switch_view_period_link=switch_view_period_link,
  )

def plot():
  import pygal
  response.headers["Content-Type"]="image/svg+xml"
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=pygal.style.LightColorizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])
  return chart.render()
