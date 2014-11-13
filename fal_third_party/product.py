# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
        
    _columns = {
        'third_party_id' : fields.many2one('res.partner', 'Third Party'),
    }

#end of product_product()