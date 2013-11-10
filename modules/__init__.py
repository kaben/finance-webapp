from gluon import *

def setup_tables(db):
  from gluon.dal import Field
  db.define_table(
    "google_companies",
  	Field("stock_symbol"),
  	Field("name"),
  	Field("sector_id", "reference google_sectors"),
    migrate=False
  )
  db.define_table(
    "google_sectors",
  	Field("catid"),
  	Field("name"),
    migrate=False
  )
  db.define_table(
    "google_sectors_assoc",
  	Field("child_id", "reference google_sectors"),
  	Field("parent_id", "reference google_sectors"),
    migrate=False
  )
  db.define_table(
    "nasdaq_company_financials",
    Field("company_id", "reference google_companies"),
    Field("period_ending"),
    Field("quarter_ending"),
    Field("quarter"),
    Field("accounting_changes"),
    Field("accounts_payable"),
    Field("accounts_receivable"),
    Field("accumulated_amortization"),
    Field("additional_income_or_expense_items"),
    Field("adjustments_to_net_income"),
    Field("capital_expenditures"),
    Field("capital_surpolus"),
    Field("cash_and_equivalents"),
    Field("common_stocks"),
    Field("cost_of_revenue"),
    Field("deferred_asset_charges"),
    Field("deferred_liability_charges"),
    Field("depreciation"),
    Field("discontinued_operations"),
    Field("dividends_paid"),
    Field("earnings_before_interest_and_tax"),
    Field("earnings_before_tax"),
    Field("effect_of_exchange_rate"),
    Field("equity_earnings_unconsolidated_subsidiary"),
    Field("extraordinary_items"),
    Field("fixed_assets"),
    Field("goodwill"),
    Field("gross_profit"),
    Field("income_tax"),
    Field("intangible_assets"),
    Field("interest_expense"),
    Field("inventory"),
    Field("investments"),
    Field("liabilities"),
    Field("long_term_debt"),
    Field("long_term_investments"),
    Field("minority_interest"),
    Field("misc_stocks"),
    Field("negative_goodwill"),
    Field("net_borrowing"),
    Field("net_cash_flow"),
    Field("net_operating_cash_flow"),
    Field("net_cash_flow_from_financing"),
    Field("net_cash_flow_from_investing"),
    Field("net_income"),
    Field("net_income_adjustments"),
    Field("shareholder_net_income"),
    Field("net_income_from_continuing_operations"),
    Field("net_receivables"),
    Field("non_recurring_items"),
    Field("operating_income"),
    Field("other_assets"),
    Field("other_current_assets"),
    Field("other_current_liabilities"),
    Field("other_equity"),
    Field("other_financing_activities"),
    Field("other_investing_activities"),
    Field("other_items"),
    Field("other_liabilities"),
    Field("other_operating_activities"),
    Field("other_operating_items"),
    Field("preferred_stocks"),
    Field("redeemable_stocks"),
    Field("research_and_development"),
    Field("retained_earnings"),
    Field("sale_and_purchase_of_stock"),
    Field("sales_general_and_admin"),
    Field("short_term_debt"),
    Field("short_term_investments"),
    Field("total_assets"),
    Field("total_current_assets"),
    Field("total_current_liabilities"),
    Field("total_equity"),
    Field("total_liabilities"),
    Field("total_revenue"),
    Field("treasury_stock"),
    Field("eps"),
    Field("shares_outstanding"),
    Field("gross_margin"),
    Field("net_margin"),
    Field("cash_to_debt_ratio"),
    Field("net_cash"),
    Field("foolish_flow_ratio"),
    Field("cash_king_margin"),
    migrate=False
  )

def get_sqlalchemy_orm(url):
  from irrealis_orm import ORM
  from sqlalchemy.orm import relationship
  
  orm_defs = dict(
    GoogleSectorAssoc = dict(
      __tablename__ = "google_sectors_assoc",
    ),
    GoogleSector = dict(
      __tablename__ = "google_sectors",
      children = relationship(
        "GoogleSector",
        secondary = "google_sectors_assoc",
        primaryjoin = "google_sectors.c.id==google_sectors_assoc.c.parent_id",
        secondaryjoin = "google_sectors.c.id==google_sectors_assoc.c.child_id",
        backref = "parents",
      ),
    ),
    GoogleCompany = dict(
      __tablename__ = "google_companies",
      sector = relationship(
        "GoogleSector",
        primaryjoin = "google_companies.c.sector_id==google_sectors.c.id",
      ),
      industry = relationship(
        "GoogleSector",
        primaryjoin = "google_companies.c.industry_id==google_sectors.c.id",
      ),
      quarterly_financials = relationship(
        "CompanyFinancials",
        primaryjoin = "and_(GoogleCompany.id==CompanyFinancials.company_id, CompanyFinancials.duration==1)",
        order_by = "CompanyFinancials.period_ending",
      ),
      annual_financials = relationship(
        "CompanyFinancials",
        primaryjoin = "and_(GoogleCompany.id==CompanyFinancials.company_id, CompanyFinancials.duration==2)",
        order_by = "CompanyFinancials.period_ending",
      ),
    ),
    CompanyFinancials = dict(__tablename__ = "company_financials"),
    NasdaqCompanyFinancials = dict(
      __tablename__ = "nasdaq_company_financials",
      company = relationship("GoogleCompany", backref="nasdaq_financials"),
    ),
  )
  orm = ORM(orm_defs, url)
  return orm


def get_pages(
  current_record_number,
  record_count,
  records_per_page,
  previous_pages = 10,
  next_pages = 10,
):
  current_page = current_record_number/records_per_page
  page_count = (record_count - 1)/records_per_page + 1
  page_min = max(0, current_page - previous_pages )
  page_max = min(current_page + next_pages + 1, page_count)
  pages = range(page_min, page_max)
  return current_page, pages


def get_pagination(href_fmt, pages, current_page, records_per_page):
  paginate = list()

  # "Prev" link.
  if 0 < current_page: paginate.append(LI(A(u"prev", _href=href_fmt.format(records_per_page*(current_page-1)))))
  # Disable "prev" link if we're on first page.
  else: paginate.append(LI(SPAN(u"prev"), _class="disabled"))

  # Page-number links.
  for page in pages:
    page_unicode = unicode(page+1)
    # Disable link for current page.
    if page == current_page: paginate.append(LI(SPAN(page_unicode), _class="active"))
    else: paginate.append(LI(A(page_unicode, _href=href_fmt.format(records_per_page*page))))

  # "Next" link.
  if pages and (current_page < pages[-1]): paginate.append(LI(A(u"next", _href=href_fmt.format(records_per_page*(current_page+1)))))
  # Disable "next" link if we're on last page.
  else: paginate.append(LI(SPAN(u"next"), _class="disabled"))

  return paginate


def recursive_google_sector_company_query(sector, orm):
  subsectors = sector and sector.children or []
  query = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.sector==sector)
  return query.union_all(*(recursive_google_sector_company_query(subsector, orm) for subsector in subsectors))
  

def recursive_google_sector_ancestors(sector):
  parents = sector and sector.parents or []
  ancestors = parents[:]
  for parent in parents: ancestors.extend(recursive_google_sector_ancestors(parent))
  return ancestors


def like_queries(klass, columns, like, orm):
  queries = (
    orm.session.query(klass).filter(column.like(like))
    for column in columns
  )
  return reduce(lambda p, q: p.union(q), queries)
  


class dotdict(dict):
  def __init__(self, *l, **d):
    super(dotdict, self).__init__(*l, **d)
    self.__dict__ = self
  def copy(self):
    return dotdict(self)
  @staticmethod
  def fromkeys(*l, **d):
    return dotdict(dict.fromkeys(*l, **d))
