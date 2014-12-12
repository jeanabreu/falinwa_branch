# -*- coding: utf-8 -*-
{
    "name": "GEN-09_Invoice Milestone Purchase",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give invoice milestone rule for Purchase
    """,
    "depends" : ['purchase','account'],
    'init_xml': [],
    'update_xml': [
        'wizard/purchase_make_invoice_advance.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: