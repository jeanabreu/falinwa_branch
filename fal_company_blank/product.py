# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _defaults = {
        'company_id' : False,
    }

#end of product_product()