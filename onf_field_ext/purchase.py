# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    STATE_SELECTION = [
        ('procurement_request', 'Procurement Request'),
        ('draft', 'Draft PO'),
        ('sent', 'RFQ Sent'),
        ('confirmed', 'Waiting Approval'),
        ('approved', 'Purchase Order'),
        ('except_picking', 'Shipping Exception'),
        ('except_invoice', 'Invoice Exception'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]
    
    _columns = {
        'state': fields.selection(STATE_SELECTION, 'Status', readonly=True, help="The status of the purchase order or the quotation request. A quotation is a purchase order in a 'Draft' status. Then the order has to be confirmed by the user, the status switch to 'Confirmed'. Then the supplier must confirm the order to change the status to 'Approved'. When the purchase order is paid and received, the status becomes 'Done'. If a cancel action occurs in the invoice or in the reception of goods, the status becomes in exception.", select=True, track_visibility='onchange'),
        'fal_invoice_term' : fields.char('Invoice Term', size=128),
    }
    
    _defaults = {
        'invoice_method' : 'demand'
    }
    
    def wkf_approve_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for po in self.browse(cr, uid, ids, context=context):
            for line in po.order_line:
                if not line.account_analytic_id.id:
                    raise osv.except_osv(_('Error!'),_('You cannot approve a purchase order without define a projects.'))
        return super(purchase_order, self).wkf_approve_order(cr, uid, ids, context)
        
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for po in self.browse(cr, uid, ids, context=context):
            for line in po.order_line:
                if not line.account_analytic_id.id:
                    raise osv.except_osv(_('Error!'),_('You cannot confirm a purchase order without define a projects.'))
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)
        
#end of purchase_order()

class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
        
    _columns = {
        'account_analytic_id':fields.many2one('account.analytic.account', 'Project Number',),
    }
        
#end of purchase_order_line()