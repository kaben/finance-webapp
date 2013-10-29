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
