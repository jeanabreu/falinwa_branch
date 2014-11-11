# -*- coding: utf-8 -*-
{
    "name": "REP-02_Easy Reporting",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to easily  export record
    """,
    "depends" : ['base'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'views/easy_reporting.xml',
        'wizard/easy_exporting_wizard_view.xml',        
    ],
    'css': [],
    'js' : [
        'static/src/js/click.js'
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: