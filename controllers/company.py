from applications.finance.modules import get_pages, get_pagination
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

def financials():
  stock_symbol = request.vars.get("stock_symbol")
  start = int(request.vars.get("start", 0))
  num = min(1000, max(1, int(request.vars.get("num", 4))))
  period = request.vars.get("period", "quarterly")
  url_vars = dict(
    stock_symbol=stock_symbol,
    start=start,
    num=num,
    period=period,
  )

  company = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.stock_symbol==stock_symbol).first()
  if company:
    financials_q = orm.session.query(
      orm.NasdaqCompanyFinancials
    ).filter(
      orm.NasdaqCompanyFinancials.company == company
    )
    if period == "quarterly":
      financials_q = financials_q.filter(
        orm.NasdaqCompanyFinancials.quarter_ending
      ).order_by(
        orm.NasdaqCompanyFinancials.quarter_ending
      )
    else:
      financials_q = financials_q.filter(
        orm.NasdaqCompanyFinancials.period_ending
      ).order_by(
        orm.NasdaqCompanyFinancials.period_ending
      )
    financials_count = financials_q.count()
    financials_q = financials_q.offset(start).limit(num)
    financials = financials_q
  else:
    financials = tuple()
    financials_count = 0

  # Get list of page numbers to link to.
  href_fmt = u"?stock_symbol={stock_symbol}&period={period}&start={offset}&num={num}".format(
    stock_symbol=stock_symbol,
    period=period,
    num=num,
    offset=u"{}"
  )
  current_page, pages = get_pages(start, financials_count, num)
  pagination = get_pagination(href_fmt, pages, current_page, num)

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
