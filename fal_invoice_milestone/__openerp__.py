# -*- coding: utf-8 -*-
{
    "name": "GEN-06_Invoice Milestone",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give invoice milestone rule
    """,
    "depends" : ['sale','account','fal_invoice_milestone_purchase'],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'wizard/fsale_make_invoice_advance.xml',
        'wizard/purchase_make_invoice_advance.xml',
        'sale_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: