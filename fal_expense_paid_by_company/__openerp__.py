# -*- coding: utf-8 -*-
{
    "name": "HRD-04_Expense Paid By Company",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add functionality on expense paid by company.
    """,
    "depends" : ['fal_expense_control', 'purchase', 'fal_subtotal_vat'],
    'init_xml': [],
    'update_xml': [
        'hr_expense_view.xml',
        'account_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: