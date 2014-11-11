# -*- coding: utf-8 -*-
{
    "name": "MRP-11_BoM External Information",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to define an external information of BoM.
    """,
    "depends" : ['base', 'stock', 'mrp', 'procurement_extends'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/ir.model.access.csv',
        'mrp_bom_view.xml'
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: