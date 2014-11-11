# -*- coding: utf-8 -*-
{
    "name": "MUL-02_Multi Company Popup",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give a popup to give an option on multi company.
    """,
    "depends" : ['base'],
    'init_xml': [],
    'update_xml': [
        'multi_company_popup_config_view.xml'
    ],
    'css': [],
    'js' : [
        'static/src/js/popup.js',
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: