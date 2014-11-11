# -*- coding: utf-8 -*-
{
    "name": "ACC-07_Invoice Pending",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give pending state on invoice
    """,
    "depends" : ['account'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: