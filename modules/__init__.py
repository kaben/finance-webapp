
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
      sector = relationship("GoogleSector", backref="companies"),
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
  page_count = record_count/records_per_page
  page_min = max(0, current_page - previous_pages )
  page_max = min(current_page + next_pages, page_count)
  pages = range(page_min, page_max)
  return current_page, pages


class dotdict(dict):
  def __init__(self, *l, **d):
    super(dotdict, self).__init__(*l, **d)
    self.__dict__ = self
  def copy(self):
    return dotdict(self)
  @staticmethod
  def fromkeys(*l, **d):
    return dotdict(dict.fromkeys(*l, **d))
