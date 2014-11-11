# -*- coding: utf-8 -*-
{
    "name": "GEN-02_Target Price",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add target price both on purchases and sales
    """,
    "depends" : ['base','purchase','sale'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'purchase_view.xml',
        'sale_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: