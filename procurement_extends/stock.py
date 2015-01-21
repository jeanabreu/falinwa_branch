# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    _columns = {
        #'fal_projects' : fields.many2one('account.analytic.account', 'Project'),
    }
#end of stock_picking()

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    _columns = {
        'fal_project_id' : fields.many2one('account.analytic.account', 'Project'),
    }
    
    def _prepare_procurement_from_move(self, cr, uid, move, context=None):
        res = super(stock_move, self)._prepare_procurement_from_move(cr, uid, move, context)
        res['sale_line_id'] = move.procurement_id and move.procurement_id.sale_line_id.id
        return res
        
#end of stock_move