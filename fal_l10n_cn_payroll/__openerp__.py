# -*- coding: utf-8 -*-
{
    "name": "HRD-08_Payroll China Falinwa",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to developed Odoo payroll based on Falinwa standard.
    """,
    "depends" : ['hr_payroll','account'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'views/hr_payroll_report_view.xml',
        'hr_payslip_workflow.xml',
        'base_data.xml',
        'hr_payroll_report.xml',
        'hr_payroll_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: