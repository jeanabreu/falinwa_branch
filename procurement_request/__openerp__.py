# -*- coding: utf-8 -*-
{
    "name": "PRO-02_Procurement Request",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional state Procurement Request 
    """,
    "depends" : ['purchase','procurement'],
    'init_xml': [],
    'update_xml': [
        'data/res.partner.csv',
        'wizard/procurement_request_wizard_view.xml',
        'purchase_view.xml',
        'stock_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: