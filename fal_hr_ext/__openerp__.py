# -*- coding: utf-8 -*-
{
    "name": "HRD-06_HR Ext",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add extention functional in HRM
    """,
    "depends" : ['base', 'hr'],
    'init_xml': [],
    'update_xml': [
        'security/hr_security.xml',
        'security/ir.model.access.csv',
        'hr_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: