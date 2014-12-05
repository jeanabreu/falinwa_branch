# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

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
    }
    
#end of stock_move()