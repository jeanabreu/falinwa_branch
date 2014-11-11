# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    _columns = {
        'date_done': fields.datetime('Date of Transfer', help="Date of Completion", track_visibility='onchange'),
    }
    
    def action_done(self, cr, uid, ids, context=None):
        """Changes picking state to done.
        
        This method is called at the end of the workflow by the activity "done".
        @return: True
        """
        for picking in self.browse(cr, uid, ids):
            if picking.date_done:
                self.write(cr, uid, ids, {'state': 'done'})
            else:
                super(stock_picking, self).action_done(cr, uid ,ids ,context=context)  
        return True
        
#end of stock_picking()