# -*- coding: utf-8 -*-
{
    "name": "ACC-06_Account Payment Document",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to able payment to be print and sent email. 
    """,
    "depends" : [
        'account',
        ],
    'init_xml': [],
    'update_xml': [
        'fal_payment_report.xml',
        'account_voucher_view.xml',
        'fal_payment_data.xml',
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: