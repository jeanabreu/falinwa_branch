# encoding: utf-8
{
    "name" : "Production Merge",
    "version" : "0.1",
    "description" : """This module adds a new wizard that allows merging two or more production orders.""",
    "author" : "NaN·tic, Falinwa",
    "website" : "http://www.NaN-tic.com, http://www.falinwa.com",
    "depends" : [ 
        'mrp',
    ],
    "category" : "Custom Modules",
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [ 
        'wizard/mrp_production_merge_view.xml',
        'mrp_view.xml',
    ],
    "active": False,
    "installable": True
}
