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
                val += self._amount_line_tax(cr, uid, line, context=context)
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
            total_invoice_ammount = total_order_tax = total_invoice_tax = total_order_subtotal = total_invoice_subtotal = 0.0
            origin_currency = order.currency_id
            temp = []
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    if order.order_policy == 'manual':
                        total_invoice_ammount += invoice_id.amount_total
                    else:
                        temp.append(invoice_id.id)
            for order_line in order.order_line:
                total_order_subtotal += order_line.price_subtotal
                total_order_tax += self._amount_line_tax(cr, uid, order_line, context=context)
                if order.order_policy != 'manual':
                    for invoice_line in order_line.invoice_lines:
                        if invoice_line.invoice_id.id in temp:
                            total_invoice_subtotal += invoice_line.price_subtotal
                            total_invoice_tax += invoice_obj._amount_line_tax(cr, uid, invoice_line, context=context)
                    total_invoice_ammount = total_invoice_subtotal + total_invoice_tax
            res[order.id] = cur_obj.round(cr, uid, origin_currency, (total_order_subtotal + total_order_tax)  - total_invoice_ammount)
        return res
    
    def _total_uninvoice_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        invoice_obj = self.pool.get('account.invoice')
        res = {}
        ctx = context.copy()
        for order in self.browse(cr,uid,ids,context=context):
            ctx.update({'date': order.date_order})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',order.company_id.id)] , context=ctx, limit=1)
            total_invoice_ammount = total_order_tax = total_invoice_tax = result = total_order_subtotal = total_invoice_subtotal = 0.0
            origin_currency = order.currency_id
            temp = []
            for invoice_id in order.invoice_ids:
                if invoice_id.state not in ('draft', 'cancel'):
                    if order.order_policy == 'manual':
                        total_invoice_ammount += invoice_id.amount_total
                    else:
                        temp.append(invoice_id.id)
            for order_line in order.order_line:
                total_order_subtotal += order_line.price_subtotal
                total_order_tax += self._amount_line_tax(cr, uid, order_line, context=context)
                if order.order_policy != 'manual':
                    for invoice_line in order_line.invoice_lines:
                        if invoice_line.invoice_id.id in temp:
                            total_invoice_subtotal += invoice_line.price_subtotal
                            total_invoice_tax += invoice_obj._amount_line_tax(cr, uid, invoice_line, context=context)
                    total_invoice_ammount = total_invoice_subtotal + total_invoice_tax
            result = (total_order_subtotal + total_order_tax)  - total_invoice_ammount
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if origin_currency != rate_id:
                    result = cur_obj.compute(cr, uid, origin_currency.id, rate_id.id, result, context=ctx)
            res[order.id] = cur_obj.round(cr, uid, origin_currency, result)
        return res

    _columns = {
        'untaxed_amount_hkd': fields.function(_amount_untaxed_hkd, digits_compute=dp.get_precision('Account'), string='Untaxed Amount (HKD)',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'sale.order.line': (_get_order_fal, None, 10),
            },
            help="The amount without tax in HKD.", track_visibility='always'),
        'amount_total_hkd': fields.function(_amount_all_hkd, digits_compute=dp.get_precision('Account'), string='Total (HKD)',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'sale.order.line': (_get_order_fal, None, 10),
            }, help="The total amount in HKD."),
        'total_uninvoice': fields.function(_total_uninvoice, digits_compute=dp.get_precision('Account'), string='Total Uninvoice',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state','currency_id'], 20),
            }, help="The total uninvoice."),
        'total_uninvoice_hkd': fields.function(_total_uninvoice_hkd, digits_compute=dp.get_precision('Account'), string='Total Uninvoice (HKD)',
            store={
                'sale.order' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'account.invoice' : (_get_invoice_ids_fal, ['invoice_line','tax_line','state','currency_id'], 20),
            }, help="The total uninvoice in HKD."),
    }

#end of sale_order()