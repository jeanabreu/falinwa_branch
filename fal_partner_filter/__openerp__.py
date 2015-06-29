# -*- coding: utf-8 -*-
{
    "name": "GEN-44_Partner Filter",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to filter partner that has no contact in sale,purchase,invoice
    
    """,
    "depends" : ['sale', 'purchase', 'account'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'sale_view.xml',
        'purchase_view.xml',
        'account_invoice_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: