# -*- coding: utf-8 -*-
{
    "name": "GEN-30_MRP Sale Conditional Choice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give conditional choice information on sale order line to MO.
    """,
    "depends" : ['base', 'sale_mrp', 'procurement_extends', 'fal_sale_condition_choice', 'fal_mrp_conditional_choice'],
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