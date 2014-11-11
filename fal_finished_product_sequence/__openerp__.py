# -*- coding: utf-8 -*-
{
    "name": "MRP-09_Finished Product Sequence",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to define a sequence on manufacture when the product is finished product.
    """,
    "depends" : ['base', 'mrp'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'finished_product_sequence.xml',
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