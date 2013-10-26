# coding: utf8
# try something like
def index():
  catid = request.vars.get("catid")
  start = request.vars.get("start", 1)
  count = request.vars.get("count", 10)
  
  sector = orm.session.query(orm.GoogleSector).filter(orm.GoogleSector.catid==catid).first()
  is_root = (sector.name == "root")
  subsectors = sector and sector.children or []
  subsectors.sort(key=lambda x: x.name)
  companies = sector and sector.companies or []

  # Construct left sidebar menu.
  navitems = response.sidebar_navitems.copy()
  navitems["enabled_items"].insert(0, "sector")
  navitems["sector"]["expand"] = True
  navitems["sector"]["summary"]["active"] = True
  sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")

  return dict(
    message="hello from sector.py",
    sidebar_menu=sidebar_menu,
    sector=sector,
    subsectors=subsectors,
    companies=companies,
    is_root=is_root,
  )
