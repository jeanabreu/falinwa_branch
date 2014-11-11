# -*- coding: utf-8 -*-
{
    "name": "GEN-05_Contract Conditions",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add Contract Conditions template.
    """,
    "depends" : ['base','purchase','sale','account','account_voucher'],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'contract_condition_view.xml',
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