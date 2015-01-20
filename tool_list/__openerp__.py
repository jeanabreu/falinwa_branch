# -*- coding: utf-8 -*-
{
    "name": "PJC-01_Tool List",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to use the task object as a tool and follow-up all the tool produced 
    """,
    "depends" : ['base','project','project_long_term','project_gtd'],
    'init_xml': [],
    'data': [
        'project_data.xml',
        'tools_sequence.xml',
    ],
    'update_xml': [
        'security/ir.model.access.csv',
        'project_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: