# -*- coding: utf-8 -*-
{
    "name": "SAL-04_Quotation Follower",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give action on quotation follower.
    """,
    "depends" : ['sale'],
    'init_xml': [],
    'update_xml': [
        'wizard/quotation_follower_wizard_view.xml',
        'sale_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: