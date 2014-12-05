# -*- coding: utf-8 -*-
{
    "name": "REP-04_Print Delivery Order",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to create delivery order report in RML type based on template.
    """,
    "depends" : ['base','sale_stock'],
    'init_xml': [],
    'update_xml': [
        'stock_report.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: