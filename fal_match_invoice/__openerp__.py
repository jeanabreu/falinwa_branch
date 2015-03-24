# -*- coding: utf-8 -*-
{
    "name": "ACC-28_Match Invoice",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Make a matching between supplier invoice and customer invoice.
    """,
    "depends" : ['account', 'sale', 'purchase', 'procurement_extends', 'fal_order_sheet_invoice'],
    'init_xml': [],
    'update_xml': [
        'account_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: