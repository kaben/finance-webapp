# coding: utf8
# try something like
def index():
  catid = request.vars.get("catid")
  start = request.vars.get("start")
  count = request.vars.get("count")
  
  sector = orm.session.query(orm.GoogleSector).filter(orm.GoogleSector.catid==catid).first()
  subsectors = sector and sector.children or []
  subsectors.sort(key=lambda x: x.name)
  companies = sector and sector.companies or []
  companies.sort(key=lambda x: x.name)

  # Construct left sidebar menu.
  navitems = response.sidebar_navitems.copy()
  navitems["future1"]["active"] = True
  sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")

  return dict(
    message="hello from sector.py",
    sidebar_menu=sidebar_menu,
    sector=sector,
    subsectors=subsectors,
    companies=companies,
  )
