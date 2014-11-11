# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def _get_order_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    def _get_invoice_ids_fal(self, cr, uid, ids, context=None):
        invoices = {}
        for invoice_ids in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):            
            invoices[invoice_ids.id] = True
        sale_ids = []
        if invoices:
            sale_ids = self.pool.get('sale.order').search(cr, uid, [('invoice_ids','in',invoices.keys())], context=context)
        return sale_ids

    def _percentage_invoice(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr,uid,ids,context=context):
            total_invoice_amount = 0.00
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ['cancel','draft']:
                    total_invoice_amount += invoice_id.amount_total
            if total_invoice_amount and order.amount_total :
                res[order.id] =  total_invoice_amount / order.amount_total * 100
            else:
                res[order.id] = 0.00
        return res
        
    def _percentage_invoice_paid(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for order in self.browse(cr,uid,ids,context=context):
            total_invoice_amount_paid = 0.0
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ['cancel','draft']:
                    total_invoice_amount_paid += invoice_id.amount_total - invoice_id.residual
            if total_invoice_amount_paid and order.amount_total :
                res[order.id] = total_invoice_amount_paid / order.amount_total * 100
            else:
                res[order.id] = 0.00
        return res

    _columns = {
        'percentage_of_invoice': fields.function(_percentage_invoice, digits_compute=dp.get_precision('Account'), string='Percentage of invoiced (validated)',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state'], 20),
            }, help="The percentage of invoice."),
        'percentage_of_invoice_paid': fields.function(_percentage_invoice_paid, digits_compute=dp.get_precision('Account'), string='Percentage of paid',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state'], 20),
            }, help="The percentage of invoice paid."),
    }

#end of sale_order()