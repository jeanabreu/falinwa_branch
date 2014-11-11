# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'generic_product' : fields.boolean('Generic Product'),
    }
    _defaults = {
        'generic_product' : 1,
    }
#end of product_product()