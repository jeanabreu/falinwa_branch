# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import SUPERUSER_ID, api

class stock_move(orm.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'
    
    _columns = {
        'sale_order_line_formula_id': fields.many2one('sale.order.line','Sale Order Line for MRP Formula'),
        'fal_stroke' : fields.integer('Stroke (mm)'),
    }

    def _prepare_procurement_from_move(self, cr, uid, move, context=None):
        res = super(stock_move, self)._prepare_procurement_from_move(cr, uid, move, context)
        res['sale_order_line_formula_id'] = move.sale_order_line_formula_id.id or move.raw_material_production_id.sale_order_line_formula_id.id
        res['fal_stroke'] = move.fal_stroke or move.raw_material_production_id.fal_stroke
        return res
        
#end of stock_move()

