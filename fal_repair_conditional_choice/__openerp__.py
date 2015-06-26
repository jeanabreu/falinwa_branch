# -*- coding: utf-8 -*-
{
    "name": "MRP-18_Repair Conditional Choice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give conditional choice on Repair Order.
    """,
    "depends" : ['base', 'fal_sale_condition_choice', 'mrp_repair'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'mrp_view.xml',
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