# -*- coding: utf-8 -*-
{
    "name": "ACC-12_Invoice Double Validate",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to have double validation on Invoice.
    """,
    "depends" : ['account'],
    'init_xml': [],
    'update_xml': [
        'account_invoice_workflow.xml',
        'account_invoice_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: