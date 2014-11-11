# -*- encoding: utf-8 -*-
{
    "name": "HRD-03_Expense Cancel",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """ 
Expenses Cancel:
===========================
Allows you to cancel an expense already paid to return to draft state and make
changes to your entrie or regenerate

    """,
    "depends" : ['base', 'account', 'hr_expense'],
    'data': [
        'workflow/hr_expense_workflow.xml',
        'hr_expense_view.xml',
        ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
