# -*- coding: utf-8 -*-
{
    "name": "HRD-01_Expense Ext",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add extention functional in expense
    """,
    "depends" : ['base', 'account', 'account_voucher', 'hr', 'hr_expense', 'fal_hr_ext'],
    'init_xml': [],
    'update_xml': [
        'account_voucher_view.xml',
        'hr_expense_view.xml'
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: