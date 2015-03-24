# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class product_template(orm.Model):
    _name = "product.template"
    _inherit = "product.template"
    
    _defaults = {
        'company_id' : False,
    }

#end of product_template()