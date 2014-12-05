# encoding: utf-8
{
    "name" : "MRP-16_Production Planning EXT",
    "version" : "0.1",
    "description" : """This module add extends feature of production planning.""",
    "author" : "Falinwa Hans",
    "website" : "http://www.falinwa.com",
    "depends" : [ 
        'mrp',
        'mrp_operations',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        'mrp_view.xml',
    ],
    "active": False,
    "installable": True
}
