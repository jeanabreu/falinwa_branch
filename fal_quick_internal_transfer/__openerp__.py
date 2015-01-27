# -*- coding: utf-8 -*-
{
    "name": "STC-05_Quick Internal Transfer",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add quick internal transfer feature in warehouse module.
    """,
    "depends" : ['sale_stock', 'stock', 'purchase'],
    'init_xml': [],
    'update_xml': [
        'views/fal_quick_internal_transfer.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/quick_internal_transfer_wizard_view.xml',
    ],
    'css': [],
    'js' : [],
    'qweb': ['static/src/xml/lib.xml'],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: