# -*- coding: utf-8 -*-
{
    "name": "PRO-01_Procurement Extends",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to customize Procurement 
    """,
    "depends" : [
        'sale',
        'purchase',
        'procurement',
        'account',
        'order_sequence',
        'target_price',
        'stock',
        'product'
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'purchase_view.xml',
        'account_invoice_view.xml',
        'stock_view.xml',
        'product_view.xml'
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: