# -*- coding: utf-8 -*-
{
    "name": "STC-08_Adjustment Inventory By Product Category",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to provided adujstment inventory method by product category.
    """,
    "depends" : ['sale_stock', 'stock', 'purchase'],
    'init_xml': [],
    'update_xml': [
        'stock_view.xml'
    ],
    'css': [],
    'js' : [],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: