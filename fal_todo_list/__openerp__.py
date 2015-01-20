# -*- coding: utf-8 -*-
{
    "name": "PJC-03_To Do List",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module To create a To Do list submenu in human resource 
    """,
    "depends" : ['project','project_long_term','project_gtd','hr'],
    'init_xml': [],
    'data': [
        'security/project_security.xml',
    ],
    'update_xml': [
        'project_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: