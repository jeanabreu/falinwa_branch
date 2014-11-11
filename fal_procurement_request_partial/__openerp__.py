# -*- coding: utf-8 -*-
{
    "name": "PRO-06_Procurement Request Partial",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add procurement request 
    """,
    "depends" : ['purchase','procurement','procurement_request'],
    'init_xml': [],
    'update_xml': [
        'wizard/procurement_request_partial_wizard_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: