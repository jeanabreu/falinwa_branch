# -*- coding: utf-8 -*-
{
    "name": "SAL-02_Sale Stopped Order",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give stopped state on sale order
    """,
    "depends" : ['sale'],
    'init_xml': [],
    'update_xml': [
        'sale_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: