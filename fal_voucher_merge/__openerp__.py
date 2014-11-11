# -*- coding: utf-8 -*-
{
    "name": "ACC-05_Account Voucher Merge",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to merge supplier and customer voucher 
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