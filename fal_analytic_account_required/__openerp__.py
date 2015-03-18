# -*- coding: utf-8 -*-
{
    "name": "ACC-28_Analytic Account Required",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Make analytic account required to filled.
    """,
    "depends" : ['account', 'hr_expense', 'account_bank_statement_reconciliation'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'account_view.xml',
    ],
    'css': [],
    'js' : [
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: