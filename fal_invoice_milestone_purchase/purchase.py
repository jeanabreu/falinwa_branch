# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
        
    _columns = {
        'invoice_method': fields.selection([('manual','Based on Purchase Order lines'),('order','Based on generated draft invoice'),('picking','Based on incoming shipments'),('demand','On Demand')], 'Invoicing Control', required=True,
                    readonly=True, states={'draft':[('readonly',False)], 'sent':[('readonly',False)]},
                    help="Based on Purchase Order lines: place individual lines in 'Invoice Control > Based on P.O. lines' from where you can selectively create an invoice.\n" \
                        "Based on generated invoice: create a draft invoice you can validate later.\n" \
                        "Bases on incoming shipments: let you create an invoice when receptions are validated.\n" \
                        "Based on Demand: Let you create an invoice based on percentage"
                ),
    }
    
    def view_invoice(self, cr, uid, ids, context=None):
        wizard_obj = self.pool.get('purchase.order.line_invoice')
        for po in self.browse(cr, uid, ids, context=context):
            if po.invoice_method == 'demand':
                if not po.invoice_ids:
                    context.update({'active_ids' :  [line.id for line in po.order_line]})
                    wizard_obj.makeInvoices(cr, uid, [], context=context)
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Invoice Advance management'),
                    'res_model': 'purchase.advance.payment.inv',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'nodestroy': True,
                }
        return super(purchase_order, self).view_invoice(cr, uid, ids, context)
        
#end of purchase_order()