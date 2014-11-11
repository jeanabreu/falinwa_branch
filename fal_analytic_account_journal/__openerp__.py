# -*- coding: utf-8 -*-
{
    "name": "ACC-21_Analytic Account in Journal CoA",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add analytic account field in Journal CoA
    """,
    "depends" : ['account'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: