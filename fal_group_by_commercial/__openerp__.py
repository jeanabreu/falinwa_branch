# -*- coding: utf-8 -*-
{
    "name": "GEN-15_Group By Commercial",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
     Module to define group by Commercial Partner on Sale/Purchase(Quotation,Order), Invoice/Payment(Supplier,Customer)
    """,
    "depends" : ['base','sale','purchase','account','account_voucher'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'res_partner_view.xml',
        'sale_view.xml',
        'purchase_view.xml',
        'account_invoice_view.xml',
        'account_voucher_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: