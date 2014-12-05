# -*- coding: utf-8 -*-
{
    "name": "GEN-03_Order Sequence",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
Customize for sequence, not only request sequence for Customer / Supplier Order number, but also  request sequence for Customer / Supplier quotation order number,and after  confirm quotation order, field of source document will show the quotation  number.
    """,
    "depends" : ['base','purchase','sale'],
    'init_xml': [],
    'update_xml': ['order_sequence.xml','sale_view.xml','purchase_view.xml'],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: