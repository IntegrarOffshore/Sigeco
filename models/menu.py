# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                  _class="brand-logo",_href="http://www.web2py.com/",
#                  _id="web2py-logo")

response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Edilson Alzemand <edilson.alzemand@gmail.com>'
response.meta.description = 'Sigeco'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'level'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    try:
        grupo = auth.user_groups
        if grupo[2] == 'gerente':
            response.menu += [
                  (T('Cadastro'), False, URL('default', 'funcionario')),
                 (T('Atendimentos'), False, '#', [
                      (T('Pendentes'), True,
                      URL('default', 'ver_funcionario?keywords=funcionario.status+not+in+"Concluido"')),
                      (T('Concluidos'), True,
                      URL('default', 'ver_funcionario')),
                 ]),
                  (T('Usuários'), False, URL('default', 'ver_usuarios')),
                ]
    except:
        response.menu += [
              (T('Cadastro'), False, URL('default', 'funcionario')),
                    (T('Atendimentos'), False, '#', [
                         (T('Pendentes'), True,
                         URL('default', 'ver_funcionario?keywords=funcionario.status+not+in+"Concluido"')),
                         (T('Concluidos'), True,
                         URL('default', 'ver_funcionario')),
                    ]),
            ]

if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
