# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    def _get_stock_move_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True
        return result.keys()
    
    def _get_products(self, cr, uid, ids, name, args, context=None):
        result = {}
        for stock_picking_id in self.browse(cr, uid, ids, context=context):
            temp = []
            for line in stock_picking_id.move_lines:
                if line.product_id.name not in temp:
                    temp.append(line.product_id.name)
            result[stock_picking_id.id] = "; ".join(temp)
        return result
    
    _columns = {
        'product_names_list' : fields.function(_get_products, type='char',string='Products',
            store={
                'stock.move': (_get_stock_move_fal, [], 20),
            }, help="The projects."),
    }
    
#end of stock_picking()