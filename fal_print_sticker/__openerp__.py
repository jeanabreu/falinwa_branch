# -*- coding: utf-8 -*-
{
    "name": "REP-05_Print Sticker",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to print sticker on sale order.
    """,
    "depends" : ['base', 'fal_sale_condition_choice', 'fal_finished_product_sequence'],
    'init_xml': [],
    'update_xml': [
        'print_report.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: