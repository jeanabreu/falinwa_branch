# -*- coding: utf-8 -*-
{
    "name": "GEN-16_Order Sheet on Invoice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add order sheet on Invoice form
    """,
    "depends" : ['base', 'account', 'purchase', 'sale'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml'
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: