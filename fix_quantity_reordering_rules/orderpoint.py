# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class stock_warehouse_orderpoint(orm.Model):
    _name = "stock.warehouse.orderpoint"
    _inherit = "stock.warehouse.orderpoint"

    def _compute_product_order_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for orderpoint in self.browse(cr, uid, ids, context=context):
            res[orderpoint.id] = orderpoint.product_max_qty - orderpoint.product_min_qty
        return res

    _columns = {
        'logic': fields.selection([('max','Order to Max'),('price','Best price (not yet active!)'),('fix','Order Quantity')], 'Reordering Mode', required=True),
        'product_order_label_qty': fields.function(_compute_product_order_qty, type='float',string='Re-ordering Quantity',store=False),
    }
#end of stock_warehouse_orderpoint()