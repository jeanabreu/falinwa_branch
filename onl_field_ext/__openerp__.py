# -*- coding: utf-8 -*-
{
    "name": "ONL Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for onl
    """,
    "depends" : ['base', 'account', 'purchase', 'sale', 'crm', 'hr_expense'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'account_view.xml',
        'purchase_view.xml',
        'sale_view.xml',
        'crm_view.xml',
        'res_partner_view.xml',
        'stock_view.xml',
        'hr_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: