# -*- coding: utf-8 -*-
{
    "name": "HRD-10_Extra Hours",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to developed Odoo extra hours connected to payroll based on Falinwa standard.
    """,
    "depends" : ['hr_payroll'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/ir.model.access.csv',
        'hr_payroll_view.xml',
        'payroll_sequence.xml',
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