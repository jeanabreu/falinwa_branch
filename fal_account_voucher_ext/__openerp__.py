# -*- coding: utf-8 -*-
{
    "name": "ACC-01_Account Voucher Ext",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to Extension the account voucher 
    """,
    "depends" : [
        'account_voucher',
        'fal_project_search'
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