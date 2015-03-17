# -*- coding: utf-8 -*-
{
    "name": "GEN-39_Default Discount",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give default discount
    """,
    "depends" : ['base','account','sale','purchase'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'res_partner_view.xml',
        'sale_view.xml',
        'account_view.xml',        
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: