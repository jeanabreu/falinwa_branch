# -*- coding: utf-8 -*-
{
    "name": "GEN-26_Prepayment Order",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add prepayment in Order. 
    """,
    "depends" : [
        'sale',
        'account_voucher',
        'account_prepayment',
        'fal_voucher_validation',
        ],
    'init_xml': [],
    'update_xml': [
        #'account_voucher_view.xml',
        'security/ir.model.access.csv',
        'sale_view.xml'
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: