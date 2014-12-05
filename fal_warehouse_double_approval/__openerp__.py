# -*- coding: utf-8 -*-
{
    "name": "STC-02_Warehouse Double Approval",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add additional state To Be Delivered
    """,
    "depends" : ['sale_stock','stock'],
    'init_xml': [],
    'update_xml': [
        'stock_view.xml'
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: