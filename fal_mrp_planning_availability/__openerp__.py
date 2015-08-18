# -*- coding: utf-8 -*-
{
    "name": "MRP-19_MRP Planning Availability",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to check availablity for manufacture based on floating production date planning.
    """,
    "depends" : ['base', 'sale', 'mrp'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'wizard/mrp_production_fixed_view.xml',
        'views/calendar.xml',
        'mrp_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb': [
        'static/src/xml/*.xml',
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: