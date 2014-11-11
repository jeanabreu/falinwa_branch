# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    _columns = {
        'related_sale_order' : fields.char('Related Sale Order', size=128),
    }
    
#end of purchase_order()

class purchase_order_line(orm.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'
    
    def compute_unit_price_after_discount(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}

        res = {}        
        if not ids:
            return res
        for order_line in self.browse(cr, uid, ids, context=context):
            res[order_line.id] = float(order_line.price_unit * (100.00 - order_line.discount) / 100.00)        
        return res


    _columns = {
        'unit_price_after_discount' : fields.function(compute_unit_price_after_discount, type='float',string='Unit Price (After Discount)',
            store={
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
    }
    
#end of purchase_order_line()