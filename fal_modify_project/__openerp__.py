# -*- coding: utf-8 -*-
{
    "name": "GEN-38_Modify Project",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to modify project
    """,
    "depends" : ['base','account','sale','purchase','project'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'wizard/project_modify_wizard_view.xml',
        'sale_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: