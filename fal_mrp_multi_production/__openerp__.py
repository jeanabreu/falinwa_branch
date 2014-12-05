# encoding: utf-8
{
    "name" : "MRP-10_Multi Production",
    "version" : "0.1",
    "description" : """This module adds a new wizard that allows multi production.""",
    "author" : "Falinwa Hans",
    "website" : "http://www.falinwa.com",
    "depends" : [ 
        'mrp',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 
        'wizard/mrp_production_multi_view.xml',
        'mrp_view.xml',
    ],
    "active": False,
    "installable": True
}
