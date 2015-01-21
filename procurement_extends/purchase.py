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

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    def _get_sale_order_invoiceterm(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for order in self.browse(cr, uid, ids, context=context):
            val_order_policy = ''
            if order.sale_order_line_id.order_id is False:
                break
            elif order.sale_order_line_id.order_id.order_policy == 'manual' :
                val_order_policy = 'On Demand'
            elif order.sale_order_line_id.order_id.order_policy == 'picking' :
                val_order_policy = 'On Delivery Order'
            else:
                val_order_policy = 'Before Delivery'
            res[order.id] = val_order_policy
        return res
    
    _columns = {
        'sale_order_line_id': fields.many2one('sale.order.line','Sale Order Line'),
        'sale_order_line_order_id' : fields.related('sale_order_line_id','order_id',type="many2one",relation="sale.order",string="Sale Order",readonly=True),
        'sale_order_line_order_currency' : fields.related('sale_order_line_id','order_id','currency_id', type="many2one",relation="res.currency",string="Sale Order Currency",readonly=True),
        'sale_order_line_order_paymentterm' : fields.related('sale_order_line_id','order_id','payment_term', type="many2one",relation="account.payment.term",string="Sale Order Payment Term",readonly=True),
        'sale_order_line_order_invoiceterm' : fields.function(_get_sale_order_invoiceterm,type="char", string='Sale Order Invoice Term'),
        'fal_incoterm_id' : fields.many2one('stock.incoterms','Incoterm'),
    }

    def action_invoice_create(self, cr, uid, ids, context=None):
        order_id = self.pool.get('purchase.order').browse(cr, uid, ids, context)[0]
        res = super(purchase_order, self).action_invoice_create(cr, uid, ids, context)
        if not self.pool.get('account.invoice').browse(cr, uid, res).final_quotation_number:
            self.pool.get('account.invoice').write(cr, uid, res, {'final_quotation_number': order_id.quotation_number or order_id.name}, context)
        return res
        
    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, group_id, context=None):
        res = super(purchase_order, self)._prepare_order_line_move(cr, uid, order, order_line, picking_id, group_id, context=context)
        for rex in res:
            rex['fal_project_id'] = order_line.account_analytic_id.id
        return res
            
#end of purchase_order()


class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"

    
#end of purchase_order_line()
   

class procurement_order(orm.Model):
    _inherit = 'procurement.order'

    def _get_po_line_values_from_proc(self, cr, uid, procurement, partner, company, schedule_date, context=None):
        res = super(procurement_order, self)._get_po_line_values_from_proc(cr, uid, procurement, partner, company, schedule_date, context)
        
        if procurement.product_id.generic_product and procurement.sale_line_id.id:
            name = procurement.sale_line_id and procurement.sale_line_id.name
            res['name'] = name
        res['account_analytic_id'] = procurement.sale_line_id and procurement.sale_line_id.order_id.project_id.id
        res['supplier_target_unit_price'] =  procurement.sale_line_id and procurement.sale_line_id.supplier_target_unit_price
        
        return res

    def make_po(self, cr, uid, ids, context=None):
        res = super(procurement_order, self).make_po(cr, uid, ids, context)
        purchase_obj = self.pool.get('purchase.order')
        purchase_line_obj = self.pool.get('purchase.order.line')
        for procurement in self.browse(cr, uid, ids, context=context):
            po_line_id = purchase_line_obj.browse(cr, uid, res[procurement.id])
            if po_line_id.order_id:
                purchase_obj.write(cr, uid, [po_line_id.order_id.id],{
                    'sale_order_line_id' : procurement.sale_line_id and procurement.sale_line_id.id,
                    'fal_incoterm_id' : procurement.sale_line_id and procurement.sale_line_id.order_id.incoterm.id,
                })
        return res

    def _run_move_create(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        res['fal_project_id'] = procurement.sale_line_id.order_id.project_id.id
        return res
        
#end of procurement_order()