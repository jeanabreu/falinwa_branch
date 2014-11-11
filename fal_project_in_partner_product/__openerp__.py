# -*- coding: utf-8 -*-
{
    "name": "PRO-09_Project in Partner and Product",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to define a project in partner and product and it will be default value of each document.
    """,
    "depends" : ['account','sale','purchase','fal_project_in_product','fal_statement_product'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'res_partner_view.xml',
        'purchase_view.xml',
        'account_view.xml',
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