# -*- coding: utf-8 -*-
{
    "name": "Falinwa Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for falinwa
    """,
    "depends" : ['base', 'account','analytic','project'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
        'project_view.xml',
        'views/fal_account_invoice.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: