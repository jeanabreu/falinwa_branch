# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"

    def _get_move_ids_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('stock.move').browse(cr, uid, ids, context=context):
            result[line.picking_id.id] = True
        return result.keys()
    
    def _get_projects(self, cr, uid, ids, name, args, context=None):
        result = {}
        for picking in self.browse(cr, uid, ids, context=context):
            temp = []
            for line in picking.move_lines:
                if line.fal_project_id.id and line.fal_project_id.code not in temp:
                    temp.append(line.fal_project_id.code or line.fal_project_id.name)
            if temp:
                result[picking.id] = "; ".join(temp)
            else:
                result[picking.id] = ""
        return result
        
    _columns = {
        'fal_project_numbers' : fields.function(_get_projects, type='char',string='Project numbers',
            store={
                'stock.move': (_get_move_ids_fal, [], 20),
            }, help="The projects."),
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