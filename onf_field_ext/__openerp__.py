# -*- coding: utf-8 -*-
{
    "name": "ONF Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for onf
    """,
    "depends" : ['base', 'account', 'purchase', 'sale','procurement_extends'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'account_view.xml',
        'purchase_view.xml',
        'sale_view.xml',
        'mrp_view.xml',
        'stock_view.xml',
        'res_partner_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: