# -*- coding: utf-8 -*-
{
    "name": "GEN-13_Line View",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give line view
    """,
    "depends" : ['sale','purchase','account'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
        'purchase_order_view.xml',
        'sale_order_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: