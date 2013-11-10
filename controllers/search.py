from applications.finance.modules import like_queries

# coding: utf8
# try something like
def index():
  search_term = request.vars.get("q")
  like = u"%{}%".format(search_term)
  company_queries = like_queries(orm.GoogleCompany, (orm.GoogleCompany.name, orm.GoogleCompany.stock_symbol), like, orm)
  sector_queries = like_queries(orm.GoogleSector, (orm.GoogleSector.name, orm.GoogleSector.catid), like, orm)
  return dict(
    search_term = search_term,
    companies = company_queries.order_by(orm.GoogleCompany.stock_symbol),
    sectors = sector_queries.order_by(orm.GoogleSector.catid),
    message="hello from search.py",
  )
