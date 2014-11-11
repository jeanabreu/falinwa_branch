# -*- coding: utf-8 -*-
{
    "name": "ACC-02_Account Cancel Ext",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to Extension the account cancel 
    """,
    "depends" : [
        'account_voucher',
        'account_cancel',
        ],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'account_cancel_view.xml',   
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: