# -*- coding: utf-8 -*-
{
    "name": "GEN-25_Serial Number Extends",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional functionality to serial number.
    """,
    "depends" : ['base', 'stock', 'product_expiry'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/security.xml',
        'product_view.xml',
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