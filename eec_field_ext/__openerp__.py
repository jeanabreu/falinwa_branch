# -*- coding: utf-8 -*-
{
    "name": "EEC Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for eec
    """,
    "depends" : ['sale','sale_stock','account', 'fal_expense_control'],
    'init_xml': [],
    'update_xml': [       
        'account_view.xml',
        'sale_view.xml',
        'stock_inventory_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: