from applications.finance.modules import get_pages, get_pagination

# coding: utf8
# try something like
def index():
  catid = request.vars.get("catid")
  start = int(request.vars.get("start", 0))
  num = min(1000, max(1, int(request.vars.get("num", 10))))
  
  sector = orm.session.query(orm.GoogleSector).filter(orm.GoogleSector.catid==catid).first()
  is_root = (sector.name == "root")
  subsectors = sector and sector.children or []
  subsectors.sort(key=lambda x: x.name)

  company_q = orm.session.query(orm.GoogleCompany).filter(orm.GoogleCompany.sector==sector)
  companies = company_q.order_by(orm.GoogleCompany.name).offset(start).limit(num)
  company_count = company_q.count()

  # Get list of page numbers to link to.
  href_fmt = u"?catid={c}&start={o}&num={n}".format(c=catid, n=num, o=u"{}")
  current_page, pages = get_pages(start, company_count, num)
  pagination = get_pagination(href_fmt, pages, current_page, num)

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
    current_company=start+1,
    through_company=min(start+num, company_count),
    company_count=company_count,
    is_root=is_root,
    pagination=pagination,
    current_page=current_page,
  )
