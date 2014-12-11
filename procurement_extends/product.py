# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_template(orm.Model):
    _name = "product.template"
    _inherit = "product.template"
    
    _columns = {
        'generic_product' : fields.boolean('Generic Product'),
    }
    _defaults = {
        'generic_product' : 1,
    }
#end of product_product()