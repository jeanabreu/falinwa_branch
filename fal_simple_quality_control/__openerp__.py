# -*- coding: utf-8 -*-
{
    "name": "STC-06_Simple QC",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to manage Quality Control in Simple Way.
    """,
    "depends" : ['stock','fal_warehouse_double_approval','stock_picking_reopen'],
    'init_xml': [],
    'update_xml': [
        'security/stock_security.xml',
        'stock_view.xml'
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: