# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

from applications.finance.modules import dotdict

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(EM("irrealis"), "CHOMP", _class="brand", _href=URL("sector", "index"))
response.title = "irrealisFINANCE"
response.webtitle = A(EM("irrealis"), "FINANCE", _id="webtitle", _href=URL("../.."))
#response.subtitle = P("simple algorithmic investing")

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Kaben Nanlohy <kaben.nanlohy@gmail.com>'
response.meta.description = "Simple algorithmic investing"
response.meta.keywords = 'investing'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = []

# Example use of response.sidebar_navitems:
# def index():
#   navitems = response.sidebar_navitems.copy()
#   navitems.enabled_items.insert(0, "company")
#   navitems.company.subitems.expand = True
#   sidebar_menu = DIV(NAV_LIST(get_menuitems(navitems)), _class="nav-menu")
#   return dotdict(message="hello from company.py", sidebar_menu=sidebar_menu)

response.sidebar_navitems = dotdict(
  enabled_items = ["future1", "future2"],
  company = dotdict(
    text = T("COMPANY"),
    expand = False,
    enabled_items = ["summary", "financials"],
    summary = dotdict(
      text=T("Summary"),
    ),
    financials = dotdict(
      text=T("Financials"),
    ),
  ),
  sector = dotdict(
    text = T("SECTOR"),
    helper = URL("sector", "index"),
    expand = False,
    enabled_items = ["summary", "summary_future_1"],
    summary = dotdict(text=T("Summary")),
    summary_future_1 = dotdict(text=T("Future submenu of summary")),
  ),
  future1 = dotdict(
    text = T("FUTURE MENU 1"),
    expand = False,
    enabled_items = ["future1_1"],
    future1_1 = dotdict(text=T("Future submenu 1.1")),
  ),
  future2 = dotdict(text=T("FUTURE MENU 2")),
)

def get_menuitems(navitems):
  menuitems = list()
  for enabled_item in navitems["enabled_items"]:
    navitem = navitems[enabled_item]
    text = navitem["text"]
    active = navitem.get("active", False)
    helper = navitem.get("helper", "")
    subitems = get_menuitems(navitem) if navitem.get("expand") else []
    menuitems.append([text, active, helper, subitems])
  return menuitems

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (SPAN('web2py'), False, 'http://web2py.com', [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
        (T('This App'), False, URL('admin', 'default', 'design/%s' % app), [
        (T('Controller'), False,
         URL(
         'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
        (T('View'), False,
         URL(
         'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
        (T('Layout'), False,
         URL(
         'admin', 'default', 'edit/%s/views/layout.html' % app)),
        (T('Stylesheet'), False,
         URL(
         'admin', 'default', 'edit/%s/static/css/web2py.css' % app)),
        (T('DB Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/db.py' % app)),
        (T('Menu Model'), False,
         URL(
         'admin', 'default', 'edit/%s/models/menu.py' % app)),
        (T('Database'), False, URL(app, 'appadmin', 'index')),
        (T('Errors'), False, URL(
         'admin', 'default', 'errors/' + app)),
        (T('About'), False, URL(
         'admin', 'default', 'about/' + app)),
        ]),
            ('web2py.com', False, 'http://www.web2py.com', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Layouts'), False, 'http://web2py.com/layouts'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             (T('Semantic'), False, 'http://web2py.com/semantic'),
             ]),
            (T('Documentation'), False, 'http://www.web2py.com/book', [
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Buy this book'), False,
              'http://stores.lulu.com/web2py'),
             ]),
            (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
                        (T('Twitter'), False, 'http://twitter.com/web2py'),
                        (T('Live Chat'), False,
                         'http://webchat.freenode.net/?channels=web2py'),
                        ]),
                (T('Plugins'), False, None, [
                        ('plugin_wiki', False,
                         'http://web2py.com/examples/default/download'),
                        (T('Other Plugins'), False,
                         'http://web2py.com/plugins'),
                        (T('Layout Plugins'),
                         False, 'http://web2py.com/layouts'),
                        ])
                ]
         )]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
