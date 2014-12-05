# -*- coding: utf-8 -*-
{
    "name": "STC-01_Easy Inventory",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to make an easy view for end-user on a touchscreen pad with bar code reader to make the physical inventory.
    """,
    "depends" : ['web', 'base', 'stock'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'views/fal_easy_inventory.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/easy_inventory_wizard_view.xml',
        'wizard/easy_edit_inventory_wizard_view.xml',
        'stock_inventory_view.xml'
    ],
    'css': [],
    'js' : [
        'static/src/js/easy_inventory.js'
    ],
    'qweb': ['static/src/xml/lib.xml'],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: