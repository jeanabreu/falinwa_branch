# -*- coding: utf-8 -*-
{
    "name": "ACC-11_Generic Falinwa CoAA",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to install Generic Falinwa Chart of Analytic Account 
    """,
    "depends" : [
        'account',
        'analytic'
        ],
    'init_xml': [],
    'update_xml': [
        'account_chart_analytic_generic_template.xml',
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: