# -*- coding: utf-8 -*-
{
    "name": "GEN-20_Invoice Sheet on Order",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add invoice sheet on Order form
    """,
    "depends" : ['base', 'account', 'purchase', 'sale'],
    'init_xml': [],
    'update_xml': [
        'purchase_view.xml',
        'sale_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: