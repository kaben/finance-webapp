from applications.finance.modules import get_pages

# coding: utf8
# try something like
def index():
  catid = request.vars.get("catid")
  start = int(request.vars.get("start", 0))
  num = min(1000, int(request.vars.get("num", 10)))
  
  sector = orm.session.query(orm.GoogleSector).filter(orm.GoogleSector.catid==catid).first()
  is_root = (sector.name == "root")
  subsectors = sector and sector.children or []
  subsectors.sort(key=lambda x: x.name)

  company_q = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.sector==sector)
  companies = company_q.order_by(orm.GoogleCompany.name).offset(start).limit(num)

  # Get list of page numbers to link to.
  current_page, pages = get_pages(start, company_q.count(), num)

  page_numbers = [str(page+1) for page in pages]
  offsets = [page*num for page in pages]

  nums_offsets = zip(page_numbers, offsets)
  # Construct list of links for display.
  pagination = [A(unicode(page_number), _href="?catid={}&start={}&num={}".format(catid, offset, num)) for page_number, offset in nums_offsets]

  # Construct left sidebar menu.
  navitems = response.sidebar_navitems.copy()
  navitems.enabled_items.insert(0, "sector")
  navitems.sector.expand = True
  navitems.sector.summary.active = True
  sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")

  return dict(
    message="hello from sector.py",
    sidebar_menu=sidebar_menu,
    sector=sector,
    subsectors=subsectors,
    companies=companies,
    is_root=is_root,
    pagination=pagination,
    current_page=current_page,
  )
