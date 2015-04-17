# -*- coding: utf-8 -*-
{
    "name": "EEC Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for eec
    """,
    "depends" : ['sale', 'purchase', 'sale_stock', 'account', 'fal_expense_control', 'fal_product_falinwa_menu', 'fal_picking_menu_ext', 'fal_project_in_product'],
    'init_xml': [],
    'update_xml': [       
        'views/eec_sales_report_view.xml',
        'views/eec_purchase_report_view.xml',
        'views/eec_invoice_report_view.xml',
        'account_view.xml',
        'sale_view.xml',
        'stock_inventory_view.xml',
        'purchase_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
