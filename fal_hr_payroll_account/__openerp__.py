#-*- coding:utf-8 -*-
{
    'name': 'HRD-07_Payroll Accounting',
    'version': '1.0',
    'category': 'Human Resources',
    'description': """
        Module to extends Payroll Accounting
    """,
    'author':'Falinwa Hans',
    'website':'http://www.falinwa.com',
    'depends': [
        'hr_payroll',
        'account',
        'hr_payroll_account',
        'hr_expense'
    ],
    'update_xml': [
        'hr_payroll_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
