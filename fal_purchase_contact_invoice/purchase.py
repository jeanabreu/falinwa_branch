# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    _columns = {
        'partner_invoice_id': fields.many2one('res.partner', 'Invoice Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="Invoice address for current purchase order."),
    }
    
    def onchange_partner_id(self, cr, uid, ids, partner_id):
        partner = self.pool.get('res.partner')
        res = super(purchase_order, self).onchange_partner_id(cr, uid, ids, partner_id)
        if not partner_id:
            return {'value': {
                'fiscal_position': False,
                'payment_term_id': False,
                }}
        contact_invoice = partner.address_get(cr, uid, [partner_id], ['invoice'])
        res['value']['partner_invoice_id'] = contact_invoice['invoice']
        return res
   
    def action_invoice_create(self, cr, uid, ids, context=None):
        invoice_obj = self.pool.get('account.invoice')
        res = super(purchase_order, self).action_invoice_create(cr, uid, ids, context)
        for purchase in self.browse(cr, uid, ids):
            if purchase.partner_invoice_id:
                invoice_obj.write(cr, uid, res, {'partner_id':purchase.partner_invoice_id.id})
        return res
        
#end of purchase_order()