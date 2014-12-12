# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
        'client_order_ref': fields.char('Customer PO Number', size=64),
    }
    
    
    def action_ship_create(self, cr, uid, ids, context=None):
        for order in self.browse(cr, uid, ids, context=context):
            for picking in order.picking_ids:
                if picking.state != 'cancel':
                    return False
        res =  super(sale_order, self).action_ship_create(cr, uid, ids, context=context)
        return True
        
    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        res = super(sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, group_id=group_id, context=context)
        res['fal_remark'] = line.fal_remark
        res['fal_client_order_ref'] = order.client_order_ref
        return res
    
#end of sale_order()

class sale_order_line(orm.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
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
                'sale.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
        'fal_full_reference' : fields.char('Full Reference',size=128),
        'fal_remark' : fields.char('Remark', size=64),
    }
        
#end of sale_order_line()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'
        
    _columns = {
        'fal_remark' : fields.char('Remark', size=64),
        'fal_client_order_ref': fields.char('Customer PO Number', size=64),
    }
    
    def _run_move_create(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        res['fal_remark'] = procurement.fal_remark
        res['fal_client_order_ref'] = procurement.fal_client_order_ref
        return res
        
#end of procurement_order()