# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0
        for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, line.order_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val
        
    def _get_order_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    def _get_invoice_ids_fal(self, cr, uid, ids, context=None):
        invoices = {}
        for invoice_ids in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):            
            invoices[invoice_ids.id] = True
        purchase_ids = []
        if invoices:
            purchase_ids = self.pool.get('purchase.order').search(cr, uid, [('invoice_ids','in',invoices.keys())], context=context)
        return purchase_ids

    def _amount_untaxed_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        for order in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': order.date_order})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',order.company_id.id)] , context=ctx, limit=1)
            temp = val = val1 = amount_tax = amount_untaxed = 0.0
            cur = order.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
            val1 = cur_obj.round(cr, uid, cur, val1)
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    val1 = cur_obj.compute(cr, uid, cur.id, rate_id.id, val1, context=ctx)
            res[order.id] = cur_obj.round(cr, uid, cur, val1)
        return res
        
    def _amount_all_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        for order in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': order.date_order})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',order.company_id.id)] , context=ctx, limit=1)
            temp = val = val1 = amount_tax = amount_untaxed = 0.0
            cur = order.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, line.price_unit, line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            temp = ( cur_obj.round(cr, uid, cur, val) + cur_obj.round(cr, uid, cur, val1) )
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    temp = cur_obj.compute(cr, uid, cur.id, rate_id.id, temp, context=ctx)
            res[order.id] = cur_obj.round(cr, uid, cur, temp)
        return res

    def _total_uninvoice(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj = self.pool.get('res.currency')
        invoice_obj = self.pool.get('account.invoice')
        ctx = context.copy()
        for order in self.browse(cr,uid,ids,context=context):
            ctx.update({'date': order.date_order})
            total_order_tax = total_invoice_tax = total_order_subtotal = total_invoice_subtotal = 0.0
            origin_currency = order.currency_id
            temp = []
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    temp.append(invoice_id.id)
            for order_line in order.order_line:
                total_order_subtotal += order_line.price_subtotal
                total_order_tax += self._amount_line_tax(cr, uid, order_line, context=context)
                for invoice_line in order_line.invoice_lines:
                    if invoice_line.invoice_id.id in temp:
                        total_invoice_subtotal += invoice_line.price_subtotal
                        total_invoice_tax += invoice_obj._amount_line_tax(cr, uid, invoice_line, context=context)
            res[order.id] = cur_obj.round(cr, uid, origin_currency, (total_order_subtotal + total_order_tax)  - (total_invoice_subtotal + total_invoice_tax))
        return res
    
    def _total_uninvoice_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        invoice_obj = self.pool.get('account.invoice')
        for order in self.browse(cr,uid,ids,context=context):
            ctx.update({'date': order.date_order})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',order.company_id.id)] , context=ctx, limit=1)
            total_order_tax = total_invoice_tax = result = total_order_subtotal = total_invoice_subtotal = 0.0
            origin_currency = order.currency_id
            temp = []
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    temp.append(invoice_id.id)
            for order_line in order.order_line:
                total_order_subtotal += order_line.price_subtotal
                total_order_tax += self._amount_line_tax(cr, uid, order_line, context=context)
                for invoice_line in order_line.invoice_lines:
                    if invoice_line.invoice_id.id in temp:
                        total_invoice_subtotal += invoice_line.price_subtotal
                        total_invoice_tax += invoice_obj._amount_line_tax(cr, uid, invoice_line, context=context)
            result = (total_order_subtotal + total_order_tax)  - (total_invoice_subtotal + total_invoice_tax)
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if origin_currency != rate_id:
                    result = cur_obj.compute(cr, uid, origin_currency.id, rate_id.id, result, context=ctx)
            res[order.id] = cur_obj.round(cr, uid, origin_currency, result)
        return res
        
    _columns = {
        'untaxed_amount_hkd': fields.function(_amount_untaxed_hkd, digits_compute=dp.get_precision('Account'), string='Untaxed Amount (HKD)',
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'purchase.order.line': (_get_order_fal, None, 10),
            }, help="The untaxed amount in HKD."),
        'amount_total_hkd': fields.function(_amount_all_hkd, digits_compute=dp.get_precision('Account'), string='Total (HKD)',
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'purchase.order.line': (_get_order_fal, None, 10),
            }, help="The total amount in HKD."),
        'total_uninvoice': fields.function(_total_uninvoice, digits_compute=dp.get_precision('Account'), string='Total Uninvoice',
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state','currency_id'], 20),
            }, help="The total uninvoice."),
        'total_uninvoice_hkd': fields.function(_total_uninvoice_hkd, digits_compute=dp.get_precision('Account'), string='Total Uninvoice (HKD)',
            store={
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state','currency_id'], 20),
            }, help="The total uninvoice in HKD."),
    }

#end of purchase_order()