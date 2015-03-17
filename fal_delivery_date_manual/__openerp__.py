# -*- coding: utf-8 -*-
{
    "name": "SAL-03_Delivery Date Manual",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give Delivery Date manually
    """,
    "depends" : ['sale', 'sale_stock', 'account'],
    'init_xml': [],
    'update_xml': [
        'sale_view.xml',
        'invoice_view.xml'
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: