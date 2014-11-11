# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from datetime import date

class procurement_request_partial_wizard(orm.TransientModel):
    _name = "procurement.request.partial.wizard"
    _description = "Procurement Request Partial Wizard"
    
    _columns = {
        'product_qty' : fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
    }

    def _get_product_qty(self, cr, uid, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        res = False
        if context.get('active_id',False):
            purchase_id = purchase_obj.browse(cr, uid, context.get('active_id',False))
            res = purchase_id.req_product_qty
        return res

    _defaults = {
        'product_qty': _get_product_qty,
    }
    
    def approve_procurement_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        data_wizard = self.browse(cr, uid, ids)[0]
        res = False
        if context.get('active_id',False):
            purchase_id = purchase_obj.browse(cr, uid, context.get('active_id',False))
            if purchase_id.req_product_qty == data_wizard.product_qty:
                purchase_obj.action_mark_rfq(cr, uid, context.get('active_id',False))
            elif purchase_id.req_product_qty < data_wizard.product_qty:
                raise osv.except_osv(_('Warning!'), _('The quantity cannot be more than default quantity.'))
            else:
                margin_qty = purchase_id.req_product_qty - data_wizard.product_qty
                purchase_obj.write(cr, uid, context.get('active_id',False), {
                    'req_product_qty' : margin_qty,
                })
                origin = (purchase_id.origin or '').split(':')[0] +':Split from '+purchase_id.name 
                purchase_id_copy = purchase_obj.copy(cr, uid, context.get('active_id',False),default={'req_product_qty':data_wizard.product_qty,'origin':origin}, context=context)
                purchase_obj.action_mark_rfq(cr, uid, purchase_id_copy)
        return res
    
#end of procurement_request_partial_wizard()