# -*- coding: utf-8 -*-
{
    "name": "CRM-01_Supplier Follow-up in Opportunities",
    "version": "1.0",
    'author': 'Falinwa Hans',
    "description": """
This module is to quickly record in each opportunity which supplier is required for a quotation and what the status for his answer.
For trading projects in opportunity stage (ie without any quotation / order), a general requirement from sales is to get supplier feedback in order to make good proposition to the customer.
The aim of this module is to improve the communication between sales and purchase department for opportunity management.
With this module:
Purchaser will be able to record which supplier is related to which opportunity.
    """,
    "depends" : ['crm','sale','purchase','procurement','account'],
    'init_xml': [],
    'update_xml': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'crm_lead_data.xml',
        'crm_lead_view.xml',
    ],
    'css': [],
    'js' : [],
    'installable': True,
    'active': False,
    'application' : False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: