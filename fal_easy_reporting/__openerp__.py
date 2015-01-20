# -*- coding: utf-8 -*-
{
    "name": "REP-02_Easy Reporting",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to easily  export records without loading any records from tree.
    """,
    "depends" : ['base'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'wizard/easy_exporting_wizard_view.xml',
        'views/easy_reporting.xml',
        'export_view.xml', 
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: