# -*- coding: utf-8 -*-
{
    "name": "PJC-04_Project Search",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
        Module to add view to search by project
    """,
    "depends" : ['base','account','sale','purchase','project'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'account_view.xml',
        'purchase_view.xml'
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': ['static/src/js/fal_project.js'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: