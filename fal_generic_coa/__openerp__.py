# -*- coding: utf-8 -*-
{
    "name": "ACC-10_Generic Falinwa CoA",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to install Generic Falinwa CoA 
    """,
    "depends" : [
        'account',
        ],
    'init_xml': [],
    'update_xml': [
        'account_chart_type.xml',
        'chart_wizard.xml',
        'account_chart_generic_template.xml',
        'account_tax.xml',
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: