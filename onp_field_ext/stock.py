# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    _columns = {
        'date_done': fields.datetime('Date of Transfer', help="Date of Completion"),
    }
#end of stock_picking_in()
