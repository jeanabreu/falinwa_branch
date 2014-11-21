# -*- coding: utf-8 -*-
{
    "name": "MUL-01_Color Company",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to change the color according to the company - and not only the logo - to avoid any confusion
    """,
    "depends" : ['base', 'web'],
    'init_xml': [],
    'update_xml': [
        'views/web_client_template.xml',
        'res_company_view.xml',
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: