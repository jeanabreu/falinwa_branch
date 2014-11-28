# -*- coding: utf-8 -*-
{
    "name": "MRP-03_Formula MRP",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to define a formula for MRP.
    """,
    "depends" : ['base', 'mrp', 'sale', 'purchase', 'fal_mrp_conditional_choice'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'sale_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: