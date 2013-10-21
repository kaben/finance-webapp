# coding: utf8
# try something like
def index():
  navitems = response.sidebar_navitems.copy()
  navitems["enabled_items"].insert(0, "company")
  navitems["company"]["expand"] = True
  navitems["company"]["summary"]["active"] = True
  sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")
  return dict(message="hello from company.py", sidebar_menu=sidebar_menu)

def plot():
  import pygal
  response.headers["Content-Type"]="image/svg+xml"
  chart = pygal.StackedLine(fill=True, interpolate='cubic', style=pygal.style.LightColorizedStyle)
  chart.add('A', [1, 3,  5, 16, 13, 3,  7])
  chart.add('B', [5, 2,  3,  2,  5, 7, 17])
  chart.add('C', [6, 10, 9,  7,  3, 1,  0])
  chart.add('D', [2,  3, 5,  9, 12, 9,  5])
  chart.add('E', [7,  4, 2,  1,  2, 10, 0])
  return chart.render()
