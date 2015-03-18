# -*- coding: utf-8 -*-
{
    "name": "HPS Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for HPS
    """,
    "depends" : ['base', 'stock', 'purchase', 'sale', 'hr_expense', 'sale_stock', 'mrp', 'crm', 'fal_bom_reader', 'procurement_request', 'fal_invoice_delivery_fee', 'purchase_discount', 'fal_order_sheet_invoice', 'account_asset'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'report.xml',
        'purchase_view.xml',
        'sale_view.xml',
        'product_view.xml',
        'stock_view.xml',
        'account_invoice_view.xml',
        'mrp_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: