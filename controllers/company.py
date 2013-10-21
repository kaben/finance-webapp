# coding: utf8
# try something like
def index():
  navitems = response.sidebar_navitems.copy()
  navitems["enabled_items"].insert(0, "company")
  navitems["company"]["expand"] = True
  navitems["company"]["summary"]["active"] = True
  sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")
  return dict(message="hello from company.py", sidebar_menu=sidebar_menu)
