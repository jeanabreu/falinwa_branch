# -*- coding: utf-8 -*-
{
    "name": "REP-01_Product label",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to create product label report in RML type
    """,
    "depends" : ['base','procurement','fix_quantity_reordering_rules'],
    'init_xml': [],
    'update_xml': [
        'product_report.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: