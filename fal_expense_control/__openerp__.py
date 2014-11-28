# -*- coding: utf-8 -*-
{
    "name": "HRD-02_Expense Control",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add expense budget field in product that can be expense, and add control on expense.
    """,
    "depends" : ['base', 'account', 'hr_expense'],
    'init_xml': [],
    'update_xml': [
        'wizard/fal_expense_line_reason_wizard_view.xml',
        'hr_expense_report.xml',
        'hr_expense_view.xml'
    ],
    'css': ['static/css/expense.css'],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: