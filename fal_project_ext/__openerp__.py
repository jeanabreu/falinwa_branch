# -*- coding: utf-8 -*-
{
    "name": "PJC-02_Project Extension",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
     Project for final customer Level1: 
     the name and the whole project is defined by the car company usually. 1 project can have only 1 final customer Level1 and several final customer Level2 (but not given in OpenERP). 
     No need description / details at this level because it’s given at subproject level.
     -
     Subproject for final customer Level2: for 1 project, we can have several subprojects. 1 subproject = 1 final customer Level2.
    """,
    "depends" : ['base','account','sale','purchase','project','project_long_term','project_gtd'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'views/fal_project_ext.xml',
        'res_partner_view.xml',
        'project_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': ['static/src/js/fal_project.js'],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: