# -*- coding: utf-8 -*-
{
    "name": "STC-03_Picking Menu Extension",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional picking menu in warehouse module
    """,
    "depends" : ['sale_stock', 'stock', 'purchase'],
    'init_xml': [],
    'update_xml': [
        'stock_view.xml'
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: