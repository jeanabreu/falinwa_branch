# -*- coding: utf-8 -*-
{
    "name": "MRP-01_HPS Report",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add MRP report based on HPS template.
    """,
    "depends" : ['base', 'fal_mrp_sale_conditional_choice', 'fal_finished_product_sequence'],
    'init_xml': [],
    'update_xml': [
        'fal_report.xml',
        'views/fal_mrp_report.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: