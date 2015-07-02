# -*- coding: utf-8 -*-
{
    "name": "PJC-06_Project Planning",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
     
    """,
    "depends" : ['project'],
    'init_xml': [],
    'data': [
        'security/ir.model.access.csv',
    ],
    'update_xml': [
        'views/hr_timesheet_sheet.xml',
        'project_view.xml',        
    ],
    'qweb': ['static/src/xml/timesheet.xml',],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: