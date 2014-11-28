# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"

    _columns = {
        'date_expected': fields.date('Expected Date of Departure', states={'done': [('readonly', True)]},required=True, select=True, help="Scheduled date for the processing of this move"),
    }
    
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
        
#end of stock_move()