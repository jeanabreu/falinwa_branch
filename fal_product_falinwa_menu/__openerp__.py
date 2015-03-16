# -*- coding: utf-8 -*-
{
    "name": "PRO-14_Falinwa Product Menu",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to just show product variant menu.
    """,
    "depends" : ['base', 'sale', 'stock', 'purchase', 'mrp', 'account'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/security.xml',
        'product_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: