# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_company(orm.Model):
    _name = "res.company"
    _inherit = "res.company"
    _columns = {
        'color': fields.selection([('aliceblue','aliceblue'),
                                      ('antiquewhite','antiquewhite'),
                                      ('aqua','aqua'),
                                      ('bisque','bisque'),
                                      ('cornsilk','cornsilk'),
                                      ('lightblue','lightblue'),
                                      ('white','white'),
                                      ],'Color'),
    }
#end of res_company()