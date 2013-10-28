from applications.finance.modules import get_pages, get_pagination, recursive_google_sector_company_query, recursive_google_sector_ancestors

# coding: utf8
# try something like
def index():
  catid = request.vars.get("catid")
  if catid == "None": catid = None
  start = int(request.vars.get("start", 0))
  num = min(1000, max(1, int(request.vars.get("num", 10))))
  is_root = catid is None
  
  sector = orm.session.query(orm.GoogleSector).filter(orm.GoogleSector.catid==catid).first()
  subsectors = sector and sector.children or []
  subsectors.sort(key=lambda x: x.name)

  ancestors = recursive_google_sector_ancestors(sector)
  ancestors.reverse()
  ancestors = filter(lambda ancestor: ancestor.catid is not None, ancestors)

  if is_root:
    company_q = orm.session.query(orm.GoogleCompany)
  else:
    company_q = recursive_google_sector_company_query(sector, orm)
  company_count = company_q.count()
  companies = company_q.order_by(orm.GoogleCompany.name).offset(start).limit(num)

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
    ancestors=ancestors,
    companies=companies,
    current_company=start+1,
    through_company=min(start+num, company_count),
    company_count=company_count,
    is_root=is_root,
    pagination=pagination,
    current_page=current_page,
  )
