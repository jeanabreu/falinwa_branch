# -*- coding: utf-8 -*-
{
    "name": "GEN-43_BoM conditional of choice Wizard",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to give wizard to create sale, manufacture or repair based on conditional of choice on BoM
    
    """,
    "depends" : ['fal_sale_condition_choice', 'fal_mrp_conditional_choice', 'fal_bom_reader'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'wizard/bom_conditional_choice_wizard_view.xml',
    ],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
    'js': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: