# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    _columns = {
        'fal_warehouse_manager_comment': fields.text('Warehouse Manager Comment'),
    }
#end of stock_move()