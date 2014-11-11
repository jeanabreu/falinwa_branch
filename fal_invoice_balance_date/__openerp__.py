# -*- coding: utf-8 -*-
{
    "name": "GEN-28_Invoice Balance on Date",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add Invoice Balance based on date that we define on the wizard form.
    """,
    "depends" : ['account'],
    'init_xml': [],
    'update_xml': [
        'wizard/invoice_balance_wizard_view.xml',
        'account_invoice_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: