# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import SUPERUSER_ID, api

class stock_picking(orm.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'
    
    _columns = {
        'fal_client_order_ref' : fields.char('Customer PO Number', size=64),
    }
    
#end of stock_picking()

class stock_move(orm.Model):
    _name = 'stock.move'
    _inherit = 'stock.move'
    
    _columns = {
        'fal_remark' : fields.char('Remark', size=64),
        'fal_client_order_ref' : fields.char('Customer PO Number', size=64),
    }

    @api.cr_uid_ids_context
    def _picking_assign(self, cr, uid, move_ids, procurement_group, location_from, location_to, context=None):
        res = super(stock_move, self)._picking_assign(cr, uid, move_ids, procurement_group, location_from, location_to, context=context)
        pick_obj = self.pool.get("stock.picking")
        move = self.browse(cr, uid, move_ids, context=context)[0]
        print 'jalansx'
        if move.picking_id:
            print 'jalans'
            print move.fal_client_order_ref
            pick_obj.write(cr, uid, [move.picking_id.id], {
                'fal_client_order_ref': move.fal_client_order_ref
            })
        return res
        
#end of stock_move()

class product_template(orm.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    
    _columns = {
        'fal_in_stock' : fields.boolean('In Stock'),
    }
#end of product_product()