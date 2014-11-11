# -*- coding: utf-8 -*-
{
    "name": "GEN-29_Total Amount CNY Store",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to customize Total amount in CNY for all the views and report (order / invoice). (Store Version)
    """,
    "depends" : ['base','purchase','sale','account','account_voucher','purchase_discount'],
    'init_xml': [],
    'update_xml': [
        'purchase_view.xml',
        'sale_view.xml',
        'account_invoice_view.xml',
        'account_voucher_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: