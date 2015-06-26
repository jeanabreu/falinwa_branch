# encoding: utf-8
{
    "name" : "GEN-42_Multi Check",
    "version" : "0.1",
    "description" : """This module adds a new wizard that allows multiple check.""",
    "author" : "Falinwa Hans",
    "website" : "http://www.falinwa.com",
    "depends" : [ 
        'stock',
        'mrp',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 
        'wizard/multi_check_stock_mrp_view.xml',
        'picking_view.xml',
    ],
    "active": False,
    "installable": True
}
