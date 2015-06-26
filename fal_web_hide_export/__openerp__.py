# -*- coding: utf-8 -*-
{
    "name": "WEB-02_Hide Export",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
    Module to hide export.
    """,
    "depends" : ['base', 'website'],
    'init_xml': [],
    'data': [
    ],
    'update_xml': [
        'security/web_security.xml',
    ],
    'css': [],
    'js' : [
    ],
    'qweb' : [
        "static/src/xml/*.xml",
    ],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: