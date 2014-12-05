# encoding: utf-8
{
    "name" : "GEN-22_Multi Cancel",
    "version" : "0.1",
    "description" : """This module adds a new wizard that allows multiple cancel.""",
    "author" : "Falinwa",
    "website" : "http://www.falinwa.com",
    "depends" : [ 
        'stock',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 
        'wizard/multi_cancel_picking_view.xml',
        'picking_view.xml',
    ],
    "active": False,
    "installable": True
}
