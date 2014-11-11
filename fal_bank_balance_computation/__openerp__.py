# -*- coding: utf-8 -*-
{
    "name": "ACC-08_Bank Balance Computation",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to provided the information of bank balance computation 
    """,
    "depends" : [
        'account',
        ],
    'init_xml': [],
    'update_xml': [  
        'wizard/bank_balance_computation_wizard_view.xml',
        'bank_balance_computation_view.xml',
        ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: