# -*- coding: utf-8 -*-
{
    "name": "HPG Field Extends Module",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional field for HPG
    """,
    "depends" : [
        'base', 'report', 'stock', 
        'purchase', 'sale', 'hr_expense', 
        'sale_stock', 'mrp', 'crm', 
        'fal_bom_reader', 'procurement_extends', 
        'procurement_request', 'fal_invoice_delivery_fee', 'purchase_discount', 
        'fal_order_sheet_invoice', 'account_asset', 'fal_l10n_cn_payroll', 
        'website', 'fal_finished_product_sequence', 'fal_mrp_conditional_choice',
        ],
    'init_xml': [],
    'update_xml': [
        'security/ir.model.access.csv',
        'sale_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: