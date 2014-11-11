# -*- coding: utf-8 -*-
{
    "name": "HRD-05_Leave Management Ext",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add extention functional in Leave Management
    """,
    "depends" : ['base', 'hr', 'fal_hr_ext','hr_holidays'],
    'init_xml': [],
    'update_xml': [
        'hr_holidays_view.xml',
        'ir.model.access.csv',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: