# -*- coding: utf-8 -*-
{
    "name": "PUR-04_Purchase Contact Invoice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to have contact invoice on purchase
    """,
    "depends" : ['base','purchase','account'],
    'init_xml': [],
    'update_xml': [
        'purchase_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: