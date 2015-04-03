# -*- coding: utf-8 -*-
{
    "name": "AP Sourcing Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for AP SOURCING
    """,
    "depends" : ['sale', 'purchase', 'sale_stock', 'account', 'fal_delivery_date_manual', 'fal_address_textbox'],
    'init_xml': [],
    'update_xml': [
        'views/qweb_view.xml',
        'sale_view.xml',
        'account_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: