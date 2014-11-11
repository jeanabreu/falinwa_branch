# -*- coding: utf-8 -*-
import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class procurement_order(osv.Model):
    _inherit = 'procurement.order'
    
    _columns = {
        'sale_order_line_formula_id': fields.many2one('sale.order.line','Sale Order Line for MRP Formula'),
    }
    
    #overide real openERP method
    def make_mo(self, cr, uid, ids, context=None):
        """ Make Manufacturing(production) order from procurement
        @return: New created Production Orders procurement wise 
        """
        res = {}
        company = self.pool.get('res.users').browse(cr, uid, uid, context).company_id
        production_obj = self.pool.get('mrp.production')
        move_obj = self.pool.get('stock.move')
        wf_service = netsvc.LocalService("workflow")
        procurement_obj = self.pool.get('procurement.order')
        for procurement in procurement_obj.browse(cr, uid, ids, context=context):
            res_id = procurement.move_id.id
            newdate = datetime.strptime(procurement.date_planned, '%Y-%m-%d %H:%M:%S') - relativedelta(days=procurement.product_id.produce_delay or 0.0)
            newdate = newdate - relativedelta(days=company.manufacturing_lead)
            produce_id = production_obj.create(cr, uid, {
                #change start here
                'sale_order_line_formula_id' : procurement.sale_order_line_formula_id.id,
                #end here
                'origin': procurement.origin,
                'product_id': procurement.product_id.id,
                'product_qty': procurement.product_qty,
                'product_uom': procurement.product_uom.id,
                'product_uos_qty': procurement.product_uos and procurement.product_uos_qty or False,
                'product_uos': procurement.product_uos and procurement.product_uos.id or False,
                'location_src_id': procurement.location_id.id,
                'location_dest_id': procurement.location_id.id,
                'bom_id': procurement.bom_id and procurement.bom_id.id or False,
                'date_planned': newdate.strftime('%Y-%m-%d %H:%M:%S'),
                'move_prod_id': res_id,
                'company_id': procurement.company_id.id,
            })
            
            res[procurement.id] = produce_id
            self.write(cr, uid, [procurement.id], {'state': 'running', 'production_id': produce_id})   
            bom_result = production_obj.action_compute(cr, uid,
                    [produce_id], properties=[x.id for x in procurement.property_ids])
            wf_service.trg_validate(uid, 'mrp.production', produce_id, 'button_confirm', cr)
        self.production_order_create_note(cr, uid, ids, context=context)
        return res
        
procurement_order()