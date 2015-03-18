# encoding: utf-8
{
    "name" : "MRP-14_MRP EXT",
    "version" : "0.1",
    "description" : """This module add a wizard on produce wizard form.""",
    "author" : "Falinwa Hans",
    "website" : "http://www.falinwa.com",
    "depends" : [ 
        'mrp',
        'mrp_consume_produce',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 
        'wizard/mrp_production_detail_wizard_view.xml',
        'mrp_view.xml',
    ],
    "active": False,
    "installable": True
}
