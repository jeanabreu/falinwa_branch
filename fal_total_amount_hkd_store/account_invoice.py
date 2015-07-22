from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    
    def _amount_line_tax(self, cr, uid, line, context=None):
        val = 0.0
        for c in self.pool.get('account.tax').compute_all(cr, uid, line.invoice_line_tax_id, line.price_unit * (1-(line.discount or 0.0)/100.0), line.quantity, line.product_id, line.invoice_id.partner_id)['taxes']:
            val += c.get('amount', 0.0)
        return val
        
    def _get_invoice_line_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.invoice.line').browse(cr, uid, ids, context=context):
            result[line.invoice_id.id] = True
        return result.keys()

    def _get_invoice_tax_fal(self, cr, uid, ids, context=None):
        result = {}
        for tax in self.pool.get('account.invoice.tax').browse(cr, uid, ids, context=context):
            result[tax.invoice_id.id] = True
        return result.keys()

    def _get_invoice_from_line_fal(self, cr, uid, ids, context=None):
        move = {}
        for line in self.pool.get('account.move.line').browse(cr, uid, ids, context=context):
            if line.reconcile_partial_id:
                for line2 in line.reconcile_partial_id.line_partial_ids:
                    move[line2.move_id.id] = True
            if line.reconcile_id:
                for line2 in line.reconcile_id.line_id:
                    move[line2.move_id.id] = True
        invoice_ids = []
        if move:
            invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('move_id','in',move.keys())], context=context)
        return invoice_ids

    def _get_invoice_from_reconcile_fal(self, cr, uid, ids, context=None):
        move = {}
        for r in self.pool.get('account.move.reconcile').browse(cr, uid, ids, context=context):
            for line in r.line_partial_ids:
                move[line.move_id.id] = True
            for line in r.line_id:
                move[line.move_id.id] = True

        invoice_ids = []
        if move:
            invoice_ids = self.pool.get('account.invoice').search(cr, uid, [('move_id','in',move.keys())], context=context)
        return invoice_ids
        
    def _amount_all_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        for invoice in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': invoice.date_invoice})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',invoice.company_id.id)] , context=ctx, limit=1)
            cur = invoice.currency_id
            temp = amount_tax = amount_untaxed = 0.0
            for line in invoice.invoice_line:
                amount_untaxed += line.price_subtotal
            for line in invoice.tax_line:
                amount_tax += line.amount
            temp = amount_untaxed + amount_tax
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    temp = cur_obj.compute(cr, uid, cur.id, rate_id.id, temp, context=ctx)
            res[invoice.id] = cur_obj.round(cr, uid, cur, temp)
        return res
        
    def _amount_untaxed_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        for invoice in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': invoice.date_invoice})
            rate_ids = cur_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',invoice.company_id.id)] , context=ctx, limit=1)
            cur = invoice.currency_id
            temp = amount_tax = amount_untaxed = 0.0
            for line in invoice.invoice_line:
                amount_untaxed += line.price_subtotal
            amount_untaxed = cur_obj.round(cr, uid, cur, amount_untaxed)
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    amount_untaxed = cur_obj.compute(cr, uid, cur.id, rate_id.id, amount_untaxed, context=ctx)
            res[invoice.id] = cur_obj.round(cr, uid, cur, amount_untaxed)
        return res
        
    def _amount_ballance_hkd(self, cr, uid, ids, name, args, context=None):
        """Function of the field residua. It computes the residual amount (balance) for each invoice"""
        if context is None:
            context = {}
        ctx = context.copy()
        result = {}
        currency_obj = self.pool.get('res.currency')
        for invoice in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': invoice.date_invoice})
            nb_inv_in_partial_rec = max_invoice_id = 0
            temp = result[invoice.id] = 0.0
            rate_ids = currency_obj.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',invoice.company_id.id)] , context=ctx, limit=1)
            cur = invoice.currency_id
            if invoice.move_id:
                for aml in invoice.move_id.line_id:
                    if aml.account_id.type in ('receivable','payable'):
                        if aml.currency_id and aml.currency_id.id == invoice.currency_id.id:
                            result[invoice.id] += aml.amount_residual_currency
                        else:
                            ctx['date'] = aml.date
                            result[invoice.id] += currency_obj.compute(cr, uid, aml.company_id.currency_id.id, invoice.currency_id.id, aml.amount_residual, context=ctx)

                        if aml.reconcile_partial_id.line_partial_ids:
                            #we check if the invoice is partially reconciled and if there are other invoices
                            #involved in this partial reconciliation (and we sum these invoices)
                            for line in aml.reconcile_partial_id.line_partial_ids:
                                if line.invoice:
                                    nb_inv_in_partial_rec += 1
                                    #store the max invoice id as for this invoice we will make a balance instead of a simple division
                                    max_invoice_id = max(max_invoice_id, line.invoice.id)
            if nb_inv_in_partial_rec:
                #if there are several invoices in a partial reconciliation, we split the residual by the number
                #of invoice to have a sum of residual amounts that matches the partner balance
                new_value = currency_obj.round(cr, uid, invoice.currency_id, result[invoice.id] / nb_inv_in_partial_rec)
                if invoice.id == max_invoice_id:
                    #if it's the last the invoice of the bunch of invoices partially reconciled together, we make a
                    #balance to avoid rounding errors
                    result[invoice.id] = result[invoice.id] - ((nb_inv_in_partial_rec - 1) * new_value)
                else:
                    result[invoice.id] = new_value
            temp = max(result[invoice.id], 0.0)
            #prevent the residual amount on the invoice to be less than 0
            for rate_id in currency_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    temp = currency_obj.compute(cr, uid, cur.id, rate_id.id, temp, context=ctx)
            result[invoice.id] = currency_obj.round(cr, uid, cur, temp)
        return result
        
    _columns = {
        'untaxed_amount_hkd': fields.function(_amount_untaxed_hkd, digits_compute=dp.get_precision('Account'), string='Subtotal (HKD)', track_visibility='always',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line','move_id','date_invoice'], 20),
                'account.invoice.tax': (_get_invoice_tax_fal, None, 20),
                'account.invoice.line': (_get_invoice_line_fal, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
            }),
        'amount_total_hkd': fields.function(_amount_all_hkd, type='float',digits_compute=dp.get_precision('Account'), string='Total (HKD)',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line','move_id','date_invoice'], 20),
                'account.invoice.tax': (_get_invoice_tax_fal, None, 20),
                'account.invoice.line': (_get_invoice_line_fal, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 20),
            }, help="The total amount in HKD."),
        'amount_ballance_hkd': fields.function(_amount_ballance_hkd, digits_compute=dp.get_precision('Account'), string='Balance (HKD)',
            store={
                'account.invoice': (lambda self, cr, uid, ids, c={}: ids, ['invoice_line','move_id','date_invoice'], 50),
                'account.invoice.tax': (_get_invoice_tax_fal, None, 50),
                'account.invoice.line': (_get_invoice_line_fal, ['price_unit','invoice_line_tax_id','quantity','discount','invoice_id'], 50),
                'account.move.line': (_get_invoice_from_line_fal, None, 50),
                'account.move.reconcile': (_get_invoice_from_reconcile_fal, None, 50),
            }, help="The balance amount in HKD."),
    }

#end of account_invoice()

class account_move_line(orm.Model):
    _name = 'account.move.line'
    _inherit = 'account.move.line'
    
    def _amount_all_to_hk(self, cr, uid, ids, field_name, arg, context=None):
        currency_pool = self.pool.get('res.currency')
        rs_data = {}
        for line in self.browse(cr, uid, ids, context=context):
            ctx = context.copy()
            ctx.update({'date': line.date})
            company_id = line.company_id.id
            res = {}
            res['fal_debit_hk'] = 0.0
            res['fal_credit_hk'] = 0.0            
            rate_ids = currency_pool.search(cr, uid,[('name', '=', 'HKD'),('company_id','=',company_id)] , context=ctx, limit=1)
            for rate_id in currency_pool.browse(cr, uid, rate_ids, ctx):
                rate_hk = rate_id
                origin_currency = line.journal_id.company_id.currency_id
                if origin_currency == rate_id:
                    res['fal_debit_hk'] = abs(line.debit)
                    res['fal_credit_hk'] = abs(line.credit)
                else:
                    #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                    res['fal_debit_hk'] = currency_pool.compute(cr, uid, origin_currency.id, rate_hk.id, abs(line.debit), context=ctx)
                    res['fal_credit_hk'] = currency_pool.compute(cr, uid, origin_currency.id, rate_hk.id, abs(line.credit), context=ctx)

                rs_data[line.id] = res
        return rs_data
        
    _columns = {
        'fal_debit_hk': fields.function(_amount_all_to_hk, type='float',digits_compute=dp.get_precision('Account'), string='Debit (HKD)',
            store={'account.move.line': (lambda self, cr, uid, ids, c={}: ids, ['debit', 'credit', 'date'], 20)},
            multi='hk',
            help="Debit in HKD."),
        'fal_credit_hk': fields.function(_amount_all_to_hk, type='float',digits_compute=dp.get_precision('Account'), string='Credit (HKD)',
            store={'account.move.line': (lambda self, cr, uid, ids, c={}: ids, ['debit', 'credit', 'date'], 20)},
            multi='hk',
            help="Credit in HKD."),
    }
#end of account_move_line()