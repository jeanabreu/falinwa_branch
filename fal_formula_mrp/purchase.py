# -*- coding: utf-8 -*-
import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, orm
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class procurement_order(orm.Model):
    _inherit = 'procurement.order'
    
    _columns = {
        'sale_order_line_formula_id': fields.many2one('sale.order.line','Sale Order Line for MRP Formula'),
        'fal_stroke' : fields.integer('Stroke (mm)'),
    }

    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context)
        res['sale_order_line_formula_id'] =  procurement.sale_order_line_formula_id.id # and procurement.sale_order_line_formula_id.id
        print procurement.fal_stroke
        print procurement.sale_line_id.fal_stroke
        #to fix the conflict between fal_mrp_sale_conditional_choice with fal_formula_mrp
        if not res.get('fal_stroke',False):
            res['fal_stroke'] =  procurement.fal_stroke or procurement.sale_line_id.fal_stroke
        
        """
        self.write(cr, uid, procurement.id, {
            'sale_order_line_formula_id' : procurement.sale_order_line_formula_id and procurement.sale_order_line_formula_id.id, 
            'fal_stroke':procurement.fal_stroke or (procurement.sale_line_id and procurement.sale_line_id.fal_stroke),
            })
        """
        return res
    
    def _run_move_create(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        res['sale_order_line_formula_id'] =  procurement.sale_order_line_formula_id.id # and procurement.sale_order_line_formula_id.id
        res['fal_stroke'] =  procurement.fal_stroke or procurement.sale_line_id.fal_stroke
        return res
        
        
    """
    def make_mo(self, cr, uid, ids, context=None):
        mrp_obj = self.pool.get('mrp.production')
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        for po in self.browse(cr, uid, ids):
            mrp_obj.write(cr, uid, res[po.id], {'sale_order_line_formula_id' : po.sale_order_line_formula_id and po.sale_order_line_formula_id.id, 'fal_stroke':po.fal_stroke or (po.sale_line_id and po.sale_line_id.fal_stroke)})
            proc_ids = self.search(cr, uid, [('fal_parent_mo_id','=', res[po.id])], context=context)
            self.write(cr, uid, proc_ids, {'sale_order_line_formula_id' : po.sale_order_line_formula_id and po.sale_order_line_formula_id.id, 'fal_stroke':po.fal_stroke or (po.sale_line_id and po.sale_line_id.fal_stroke)})
        return res
    """    
#end of procurement_order()