# -*- coding: utf-8 -*-
{
    "name": "MRP-02_BOM Reader",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to define a simple view for warehouse manager designed on a hard touch screen for reading BOM + making easy physical inventory.
    """,
    "depends" : ['base', 'mrp','fal_finished_product_sequence'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'mrp_bom_view.xml',
        'wizard/bom_reader_wizard_view.xml'
    ],
    'css': [],
    'js' : [
        'static/src/js/click.js'
    ],
    'qweb': ['static/src/xml/lib.xml'],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: