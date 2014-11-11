# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    def onclick_reconcile_all_credit(self, cr, uid, ids, context=None):
        voucher_line_obj = self.pool.get('account.voucher.line')
        for voucher in self.browse(cr, uid, ids, context):
            temp_checkbox = []
            temp_ids = []
            for voucher_line in voucher.line_cr_ids:
                temp_checkbox.append(voucher_line.reconcile)
                temp_ids.append(voucher_line.id)
            if False in temp_checkbox:
                for voucher_line in voucher.line_cr_ids:
                    voucher_line_obj.write(cr, uid, voucher_line.id, {'reconcile': True, 'amount': voucher_line.amount_unreconciled or 0.0}, context)
            else:
                for voucher_line in voucher.line_cr_ids:
                    voucher_line_obj.write(cr, uid, voucher_line.id, {'reconcile': False, 'amount': 0.0}, context)
        return True
    
    def onclick_reconcile_all_debit(self, cr, uid, ids, context=None):
        voucher_line_obj = self.pool.get('account.voucher.line')
        for voucher in self.browse(cr, uid, ids, context):
            temp_checkbox = []
            temp_ids = []
            for voucher_line in voucher.line_dr_ids:
                temp_checkbox.append(voucher_line.reconcile)
                temp_ids.append(voucher_line.id)
            
            if False in temp_checkbox:
                for voucher_line in voucher.line_dr_ids:
                    voucher_line_obj.write(cr, uid, voucher_line.id, {'reconcile': True, 'amount': voucher_line.amount_unreconciled or 0.0}, context)
            else:
                for voucher_line in voucher.line_dr_ids:
                    voucher_line_obj.write(cr, uid, voucher_line.id, {'reconcile': False, 'amount': 0.0}, context)
        return True
        
    #overide code from openerp
    def recompute_voucher_lines(self, cr, uid, ids, partner_id, journal_id, price, currency_id, ttype, date, context=None):
        """
        Returns a dict that contains new values and context

        @param partner_id: latest value from user input for field partner_id
        @param args: other arguments
        @param context: context arguments, like lang, time zone

        @return: Returns a dict which contains new values, and context
        """
        def _remove_noise_in_o2m():
            """if the line is partially reconciled, then we must pay attention to display it only once and
                in the good o2m.
                This function returns True if the line is considered as noise and should not be displayed
            """
            if line.reconcile_partial_id:
                if currency_id == line.currency_id.id:
                    if line.amount_residual_currency <= 0:
                        return True
                else:
                    if line.amount_residual <= 0:
                        return True
            return False

        if context is None:
            context = {}
        context_multi_currency = context.copy()

        currency_pool = self.pool.get('res.currency')
        move_line_pool = self.pool.get('account.move.line')
        partner_pool = self.pool.get('res.partner')
        journal_pool = self.pool.get('account.journal')
        line_pool = self.pool.get('account.voucher.line')

        #set default values
        default = {
            'value': {'line_dr_ids': [] ,'line_cr_ids': [] ,'pre_line': False,},
        }

        #drop existing lines
        line_ids = ids and line_pool.search(cr, uid, [('voucher_id', '=', ids[0])]) or False
        if line_ids:
            line_pool.unlink(cr, uid, line_ids)

        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id

        total_credit = 0.0
        total_debit = 0.0
        account_type = 'receivable'
        if ttype == 'payment':
            account_type = 'payable'
            total_debit = price or 0.0
        else:
            total_credit = price or 0.0
            account_type = 'receivable'

        if not context.get('move_line_ids', False):
            ids = move_line_pool.search(cr, uid, [('state','=','valid'), ('account_id.type', 'in', ['payable','receivable']), ('reconcile_id', '=', False), ('partner_id', '=', partner_id)], context=context)
        else:
            ids = context['move_line_ids']
        invoice_id = context.get('invoice_id', False)
        company_currency = journal.company_id.currency_id.id
        move_line_found = False

        #order the lines by most old first
        ids.reverse()
        account_move_lines = move_line_pool.browse(cr, uid, ids, context=context)

        #compute the total debit/credit and look for a matching open amount or invoice
        for line in account_move_lines:
            if _remove_noise_in_o2m():
                continue

            if invoice_id:
                if line.invoice.id == invoice_id:
                    #if the invoice linked to the voucher line is equal to the invoice_id in context
                    #then we assign the amount on that line, whatever the other voucher lines
                    move_line_found = line.id
                    break
            elif currency_id == company_currency:
                #otherwise treatments is the same but with other field names
                if line.amount_residual == price:
                    #if the amount residual is equal the amount voucher, we assign it to that voucher
                    #line, whatever the other voucher lines
                    move_line_found = line.id
                    break
                #otherwise we will split the voucher amount on each line (by most old first)
                total_credit += line.credit or 0.0
                total_debit += line.debit or 0.0
            elif currency_id == line.currency_id.id:
                if line.amount_residual_currency == price:
                    move_line_found = line.id
                    break
                total_credit += line.credit and line.amount_currency or 0.0
                total_debit += line.debit and line.amount_currency or 0.0

        #voucher line creation
        for line in account_move_lines:

            if _remove_noise_in_o2m():
                continue

            if line.currency_id and currency_id == line.currency_id.id:
                amount_original = abs(line.amount_currency)
                amount_unreconciled = abs(line.amount_residual_currency)
            else:
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                amount_original = currency_pool.compute(cr, uid, company_currency, currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
                amount_unreconciled = currency_pool.compute(cr, uid, company_currency, currency_id, abs(line.amount_residual), context=context_multi_currency)
            line_currency_id = line.currency_id and line.currency_id.id or company_currency
            
            #modify start in here
            if line.amount_currency or line.currency_id and currency_id == line.currency_id.id:
                origin_amount_original = abs(line.amount_currency)
                origin_amount_unreconciled = abs(line.amount_residual_currency)
            else:
                origin_amount_original = currency_pool.compute(cr, uid, company_currency, line_currency_id, line.credit or line.debit or 0.0, context=context_multi_currency)
                origin_amount_unreconciled = currency_pool.compute(cr, uid, company_currency, line_currency_id, abs(line.amount_residual), context=context_multi_currency)
            #end here
            
            rs = {
                'name':line.move_id.name,
                'type': line.credit and 'dr' or 'cr',
                'move_line_id':line.id,
                'account_id':line.account_id.id,
                'amount_original': amount_original,
                'amount': (move_line_found == line.id) and min(abs(price), amount_unreconciled) or 0.0,
                'date_original':line.date,
                'date_due':line.date_maturity,
                'amount_unreconciled': amount_unreconciled,
                'currency_id': line_currency_id,
                #modify start in here
                'fal_invoice_order_number' : line.invoice and line.invoice.origin or '',
                'fal_invoice_order_number' : line.invoice and line.invoice.fal_project_numbers or '',
                'fal_origin_origininal_amount' : origin_amount_original,
                'fal_origin_open_balance' : origin_amount_unreconciled,
                'fal_origin_amount' : 0.0,
                #end here
            }
            #in case a corresponding move_line hasn't been found, we now try to assign the voucher amount
            #on existing invoices: we split voucher amount by most old first, but only for lines in the same currency
            if not move_line_found:
                if currency_id == line_currency_id:
                    if line.credit:
                        amount = min(amount_unreconciled, abs(total_debit))
                        rs['amount'] = amount
                        total_debit -= amount
                    else:
                        amount = min(amount_unreconciled, abs(total_credit))
                        rs['amount'] = amount
                        total_credit -= amount

            if rs['amount_unreconciled'] == rs['amount']:
                rs['reconcile'] = True

            if rs['type'] == 'cr':
                default['value']['line_cr_ids'].append(rs)
            else:
                default['value']['line_dr_ids'].append(rs)

            if ttype == 'payment' and len(default['value']['line_cr_ids']) > 0:
                default['value']['pre_line'] = 1
            elif ttype == 'receipt' and len(default['value']['line_dr_ids']) > 0:
                default['value']['pre_line'] = 1
            default['value']['writeoff_amount'] = self._compute_writeoff_amount(cr, uid, default['value']['line_dr_ids'], default['value']['line_cr_ids'], price, ttype)
        return default
        
#end of account_voucher()

class account_voucher_line(orm.Model):
    _name = 'account.voucher.line'
    _inherit = 'account.voucher.line'

    def _origin_original_currency(self, cr, uid, ids, field_name, arg, context=None):
        currency_pool = self.pool.get('res.currency')
        rs_data = {}
        for line in self.browse(cr, uid, ids, context=context):
            ctx = context.copy()
            ctx.update({'date': line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(cr, uid, line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
            ctx.update({
                'voucher_special_currency': line.voucher_id.payment_rate_currency_id and line.voucher_id.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate': line.voucher_id.payment_rate * voucher_rate})
            res = {}
            company_currency = line.voucher_id.journal_id.company_id.currency_id.id
            voucher_currency = line.voucher_id.currency_id and line.voucher_id.currency_id.id or company_currency
            origin_currency = line.currency_id.id
            move_line = line.move_line_id or False

            if not move_line:
                res['fal_origin_origininal_amount'] = 0.0
                res['fal_origin_open_balance'] = 0.0
            elif move_line.amount_currency or move_line.currency_id and voucher_currency==move_line.currency_id.id:
                res['fal_origin_origininal_amount'] = abs(move_line.amount_currency)
                res['fal_origin_open_balance'] = abs(move_line.amount_residual_currency)
            else:
                #always use the amount booked in the company currency as the basis of the conversion into the voucher currency
                res['fal_origin_origininal_amount'] = currency_pool.compute(cr, uid, company_currency, origin_currency, move_line.credit or move_line.debit or 0.0, context=ctx)
                res['fal_origin_open_balance'] = currency_pool.compute(cr, uid, company_currency, origin_currency, abs(move_line.amount_residual), context=ctx)

            rs_data[line.id] = res
        return rs_data
        
    def _origin_amount(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        currency_pool = self.pool.get('res.currency')
        for voucher_line in self.browse(cr,uid,ids,context=context):
            ctx = context.copy()
            ctx.update({'date': voucher_line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(cr, uid, voucher_line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
            ctx.update({
                'voucher_special_currency': voucher_line.voucher_id.payment_rate_currency_id and voucher_line.voucher_id.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate': voucher_line.voucher_id.payment_rate * voucher_rate})
            
            company_currency = voucher_line.voucher_id.journal_id.company_id.currency_id.id    
            origin_currency_id = voucher_line.currency_id.id
            payment_method_currency = voucher_line.voucher_id.journal_id.currency.id
            voucher_currency = voucher_line.voucher_id.currency_id and voucher_line.voucher_id.currency_id.id or company_currency
            res[voucher_line.id] = currency_pool.compute(cr, uid, voucher_currency, origin_currency_id, voucher_line.amount or 0.0 , ctx)
        return res
        
    _columns = {
        'fal_invoice' : fields.related('move_line_id', 'invoice', type='many2one',relation='account.invoice', string='Invoice',store=False, select=True),
        'fal_invoice_order_number' : fields.related('move_line_id', 'invoice', 'origin', type='char', string='Origin\'s Source',store=False),
        'fal_invoice_projects_number' : fields.related('move_line_id', 'invoice', 'fal_project_numbers', type='char', string='Projects Number',store=False),
        'fal_origin_origininal_amount' : fields.function(_origin_original_currency, digits_compute=dp.get_precision('Account'), string='Original Amount (in Origin\'s Currency)',
            store={
                'account.voucher.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }, multi='dc', help="Original amount in origin's currency."),
        'fal_origin_open_balance' : fields.function(_origin_original_currency, digits_compute=dp.get_precision('Account'), string='Open Balance (in Origin\'s Currency)',
            store={
                'account.voucher.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }, multi='dc', help="Open Balance in origin's currency."),        
        'fal_origin_amount' : fields.function(_origin_amount, digits_compute=dp.get_precision('Account'), string='Allocation (in Origin\'s Currency)',
            store={
                'account.voucher.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }, help="Amount in origin's currency."),
    }
    
    def onchange_amount(self, cr, uid, ids, amount, amount_unreconciled, context=None):
        res = super(account_voucher_line, self).onchange_amount(cr, uid, ids, amount, amount_unreconciled, context)
        if ids  :
            voucher_line = self.browse(cr, uid, ids)[0]
            
            ctx = context.copy()
            ctx.update({'date': voucher_line.voucher_id.date})
            voucher_rate = self.pool.get('res.currency').read(cr, uid, voucher_line.voucher_id.currency_id.id, ['rate'], context=ctx)['rate']
            ctx.update({
                'voucher_special_currency': voucher_line.voucher_id.payment_rate_currency_id and voucher_line.voucher_id.payment_rate_currency_id.id or False,
                'voucher_special_currency_rate': voucher_line.voucher_id.payment_rate * voucher_rate})
                
            company_currency = voucher_line.voucher_id.journal_id.company_id.currency_id.id 
            currency_pool = self.pool.get('res.currency')
            origin_currency_id = voucher_line.currency_id.id
            payment_method_currency = voucher_line.voucher_id.journal_id.currency.id
            voucher_currency = voucher_line.voucher_id.currency_id and voucher_line.voucher_id.currency_id.id or company_currency
            res['value']['fal_origin_amount'] = currency_pool.compute(cr, uid, voucher_currency, origin_currency_id, amount or 0.0, ctx)
        return res
        
    def open_invoice(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr,uid ,ids)[0]
        return {
            'type': 'ir.actions.act_window',
            'name': data.fal_invoice.number,
            'res_model': 'account.invoice',
            'res_id' : data.fal_invoice.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
        }
        
        
#end of account_voucher_line()