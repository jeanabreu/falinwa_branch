# -*- coding: utf-8 -*-
{
    "name": "GEN-27_Classic Invoice Control",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give classic invoice control
    """,
    "depends" : ['base', 'stock', 'sale', 'sale_stock','account', 'stock_account'],
    'init_xml': [],
    'update_xml': [
        'stock_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: