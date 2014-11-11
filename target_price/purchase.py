# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class purchase_order(orm.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    _description = 'Purchases Order'

    def _compute_total_gross_margin(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order in self.browse(cr, uid, ids, context=context):
            val = 0.00
            for order_line in order.order_line:
                val += order_line.gross_margin
            res[order.id] = val
        return res

    def _compute_total_supplier_target_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order in self.browse(cr, uid, ids, context=context):
            val = 0.00
            for order_line in order.order_line:
                val += order_line.supplier_target_unit_price
            res[order.id] = val
        return res
    
    def _compute_total_markup(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order in self.browse(cr, uid, ids, context=context):
            val = 0.00
            if order.total_gross_margin and order.total_supplier_target_price:
                val = (order.total_gross_margin / order.total_supplier_target_price) * 100
            res[order.id] = val
        return res

    def _get_purchase_order_line_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
        
    _columns = {
        'total_gross_margin' : fields.function(_compute_total_gross_margin, string='Total Gross Margin', digits_compute= dp.get_precision('Account')),
        'total_supplier_target_price' : fields.function(_compute_total_supplier_target_price, string='Total Supplier Target Price', digits_compute= dp.get_precision('Account'),
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'purchase.order.line' : (_get_purchase_order_line_fal, None, 20),
            }
        ),
        'total_markup' : fields.function(_compute_total_markup, string='Total Mark-up %',
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'purchase.order.line' : (_get_purchase_order_line_fal, None, 20),
            }
        ),
    }
    
#end of purchase_order()    

class purchase_order_line(orm.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'
    _description = 'Purchases Order Line'
    

    def _compute_gross_margin(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order_line in self.browse(cr, uid, ids, context=context):
            res[order_line.id] = order_line.price_unit - order_line.supplier_target_unit_price
        return res

    def _compute_markup(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order_line in self.browse(cr, uid, ids, context=context):
            markup = 0.00
            if order_line.gross_margin and order_line.supplier_target_unit_price:
                markup = float(order_line.gross_margin / order_line.supplier_target_unit_price) * 100
            res[order_line.id] = markup
        return res
        
    def _compute_supplier_target_subtotal(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order_line in self.browse(cr, uid, ids, context=context):
            res[order_line.id] = order_line.product_qty * order_line.supplier_target_unit_price
        return res
 
    _columns = {
        'supplier_target_unit_price' : fields.float('Supplier Target Unit Price (In Customer Currency)' ,digits_compute= dp.get_precision('Product Price')),
        'supplier_target_subtotal' : fields.function(_compute_supplier_target_subtotal, string='Supplier Target Subtotal (In Customer Currency)', digits_compute= dp.get_precision('Account'),
            store={
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
        'gross_margin' : fields.function(_compute_gross_margin, type='float',string='Gross Margin', digits_compute= dp.get_precision('Account'),
            store={
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
        'mark_up' : fields.function(_compute_markup, type='float',string='Mark-up %',
            store={
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
    }
    
#end of purchase_order_line()