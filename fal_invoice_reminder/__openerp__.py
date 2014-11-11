# -*- coding: utf-8 -*-
{
    "name": "REP-03_Invoice Reminder",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to reminder the invoice due date
    """,
    "depends" : ['base','account','mail'],
    'init_xml': [],
    'update_xml': ['res_partner_view.xml','cron_configuration.xml'],
    'css': [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: