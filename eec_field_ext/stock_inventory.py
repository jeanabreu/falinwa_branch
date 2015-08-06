# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def open_move(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr,uid ,ids)[0]
        return {
            'type': 'ir.actions.act_window',
            'name': data.name,
            'res_model': 'stock.move',
            'res_id' : data.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'current',
            'nodestroy': True,
        }
    
    _columns = {        
        'fal_partner_id' : fields.related('picking_id', 'partner_id', type='many2one', relation='res.partner', string='Partner', readonly=True),
    }

#end of stock_move()

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"


    def _get_fal_order_date(self, cr, uid, ids, name, attribute, context=None):
        res = {}
        for picking in self.browse(cr, uid, ids):
            if picking.move_lines:
                res[picking.id] = picking.move_lines[0].purchase_line_id.order_id.date_order
        return res

    _columns = {   
        'fal_order_date' : fields.function(_get_fal_order_date, type='date', string='Purchase Order Date', store=False),
    }
    
#end of stock_picking()