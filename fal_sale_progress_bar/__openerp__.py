# -*- coding: utf-8 -*-
{
    "name": "SAL-01_Sale Progress Bar",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add progress bar on Sale Order
    """,
    "depends" : ['sale','account','account_voucher'],
    'init_xml': [],
    'update_xml': [
        'sale_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: