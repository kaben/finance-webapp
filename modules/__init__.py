
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
