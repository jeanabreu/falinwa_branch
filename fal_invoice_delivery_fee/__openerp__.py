# -*- coding: utf-8 -*-
{
    "name": "ACC-03_Invoice Delivery fee",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add delivery fees on invoice.
    Warning: This module can wok only if the VAT rate is the same for all the products. 
    If no, the computed tax amount will not correspond to the fapiao tax amount.
    """,
    "depends" : ['base','account','purchase','sale','fal_subtotal_vat','purchase_discount'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'account_invoice_view.xml',
        'purchase_view.xml',
        'sale_view.xml',
        'fal_report.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: