# -*- coding: utf-8 -*-
{
    "name": "ACC-04_Account Voucher Validation",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add validate state in voucher 
    """,
    "depends" : [
        'account_voucher',
        ],
    'init_xml': [],
    'update_xml': [
        'account_voucher_view.xml',   
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: