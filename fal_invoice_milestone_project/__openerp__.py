# -*- coding: utf-8 -*-
{
    "name": "GEN-19_Invoice Milestone Project",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give invoice control by project milestone
    """,
    "depends" : ['sale', 'account', 'project', 'fal_invoice_milestone'],
    'init_xml': [],
    'update_xml': [
        'project_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: