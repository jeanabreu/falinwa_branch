# -*- coding: utf-8 -*-
{
    "name": "PRO-10_Procurement No Purchase Order",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add feature disable procurement Purchase order on product. 
    """,
    "depends" : [
        'sale',
        'purchase',
        'procurement',
        'stock',
        'product'
        ],
    'init_xml': [],
    'update_xml': [
        'product_view.xml'
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: