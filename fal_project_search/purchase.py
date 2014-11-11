# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class purchase_order(orm.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    
    def _get_purchase_ids_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    def _get_projects(self, cr, uid, ids, name, args, context=None):
        result = {}
        for purchase in self.browse(cr, uid, ids, context=context):
            temp = []
            for line in purchase.order_line:
                if line.account_analytic_id and line.account_analytic_id.code not in temp:
                    temp.append(line.account_analytic_id.code or line.account_analytic_id.name)
            if temp:
                result[purchase.id] = "; ".join(temp)
            else:
                result[purchase.id] = ""
        return result
 
    _columns = {
        'fal_project_numbers' : fields.function(_get_projects, type='char',string='Projects',
            store={
                'purchase.order.line': (_get_purchase_ids_fal, [], 20),
            }, help="The projects."),
    }
#end of purchase_order()