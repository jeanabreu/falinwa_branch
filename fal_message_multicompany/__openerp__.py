# -*- coding: utf-8 -*-
{
    "name": "MUL-05_Message Multi Company",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to add company field on message object and create an access rule of it.
    """,
    "depends" : ['base','mail'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'mail_data.xml',
        'mail_message_view.xml',
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