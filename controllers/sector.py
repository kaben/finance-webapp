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

  
  # Get number of companies in this sector.
  count = company_q.count()
  # Get first page.
  current_page=start/num
  # Get number of pages.
  page_count=count/num
  # Get first and last pages to link to.
  page_min = max(0, current_page - 10 )
  page_max = min(current_page + 10, page_count)
  # Get list of pages to link to.
  pages = range(page_min, page_max)
  page_numbers = [page+1 for page in pages]
  offsets = [page*num for page in pages]
  nums_offsets = zip(page_numbers, offsets)
  # Construct list of links for display.
  pagination = [A(unicode(page_number), _href="?catid={}&start={}&num={}".format(catid, offset, num)) for page_number, offset in nums_offsets]

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
    pagination=pagination,
    current_page=current_page,
  )
