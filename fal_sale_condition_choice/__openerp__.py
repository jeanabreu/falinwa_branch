# -*- coding: utf-8 -*-
{
    "name": "SAL-08_Sale Conditional Choice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give conditional choice on Sale Order.
    """,
    "depends" : ['base', 'sale', 'mrp'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'sale_view.xml',
        'base_data.xml',
        'security/ir.model.access.csv',
        'fal.stroke.max.csv',
        'fal.ref.data.csv',
        'fal.standard.stroke.csv',
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