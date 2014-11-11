# -*- coding: utf-8 -*-
{
    "name": "ONP Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for onp
    """,
    "depends" : ['base', 'account','purchase','sale'],
    'init_xml': [],
    'update_xml': ['account_view.xml','res_partner_view.xml'],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: