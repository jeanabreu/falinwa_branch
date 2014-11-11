# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from datetime import date

class procurement_request_partial_wizard(orm.TransientModel):
    _name = "procurement.request.partial.wizard"
    _inherit = "procurement.request.partial.wizard"
    
    def approve_procurement_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        data_wizard = self.browse(cr, uid, ids)[0]
        if context.get('active_id',False):
            purchase_id = purchase_obj.browse(cr, uid, context.get('active_id',False))
            for order_line in purchase_id.order_line:
                if order_line.product_id.third_party_id:
                    raise osv.except_osv(_('Warning!'), _('This is third party component. You cannot purchase the third party component, please cancel this request and make a manual incoming shipment for this component.'))
        return super(procurement_request_partial_wizard,self).approve_procurement_request(cr, uid, ids, context=context)
    
#end of procurement_request_partial_wizard()