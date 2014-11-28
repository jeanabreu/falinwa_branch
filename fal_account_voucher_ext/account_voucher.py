# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import workflow
import time
from openerp import netsvc

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
        #comment on v7,will revised again if there's a bug in here (Hans)
        #if line_ids:
        #    line_pool.unlink(cr, uid, line_ids)

        for line in line_pool.browse(cr, uid, line_ids, context=context):
            if line.type == 'cr':
                default['value']['line_cr_ids'].append((2, line.id))
            else:
                default['value']['line_dr_ids'].append((2, line.id))
                
        if not partner_id or not journal_id:
            return default

        journal = journal_pool.browse(cr, uid, journal_id, context=context)
        partner = partner_pool.browse(cr, uid, partner_id, context=context)
        currency_id = currency_id or journal.company_id.currency_id.id

        total_credit = 0.0
        total_debit = 0.0
        #comment on v7,will revised again if there'a a bug in here (Hans)
        #account_type = 'receivable'
        #if ttype == 'payment':
        #    account_type = 'payable'
        #    total_debit = price or 0.0
        #else:
        #    total_credit = price or 0.0
        #    account_type = 'receivable'
        account_type = None
        if context.get('account_id'):
            account_type = self.pool['account.account'].browse(cr, uid, context['account_id'], context=context).type
        if ttype == 'payment':
            if not account_type:
                account_type = 'payable'
            total_debit = price or 0.0
        else:
            total_credit = price or 0.0
            if not account_type:
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
                    #commented on v7, will revised again if there's a bug
                    #break
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
        
        #this is new code from v8, neet to fix if there's a bug
        remaining_amount = price
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
            
            #modify start in here, the reason of full ovveride
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

    #override real openERP method
    def reconcile(self, cr, uid, ids, type='auto', writeoff_acc_id=False, writeoff_period_id=False, writeoff_journal_id=False, context=None):
        account_obj = self.pool.get('account.account')
        move_obj = self.pool.get('account.move')
        move_rec_obj = self.pool.get('account.move.reconcile')
        partner_obj = self.pool.get('res.partner')
        currency_obj = self.pool.get('res.currency')
        lines = self.browse(cr, uid, ids, context=context)
        unrec_lines = filter(lambda x: not x['reconcile_id'], lines)
        credit = debit = 0.0
        currency = 0.0
        account_id = False
        partner_id = False
        if context is None:
            context = {}
        company_list = []
        for line in self.browse(cr, uid, ids, context=context):
            if company_list and not line.company_id.id in company_list:
                raise osv.except_osv(_('Warning!'), _('To reconcile the entries company should be the same for all entries.'))
            company_list.append(line.company_id.id)
        for line in unrec_lines:
            if line.state <> 'valid':
                raise osv.except_osv(_('Error!'),
                        _('Entry "%s" is not valid !') % line.name)
            credit += line['credit']
            debit += line['debit']
            currency += line['amount_currency'] or 0.0
            account_id = line['account_id']['id']
            partner_id = (line['partner_id'] and line['partner_id']['id']) or False
        writeoff = debit - credit

        # Ifdate_p in context => take this date
        if context.has_key('date_p') and context['date_p']:
            date=context['date_p']
        else:
            date = time.strftime('%Y-%m-%d')

        cr.execute('SELECT account_id, reconcile_id '\
                   'FROM account_move_line '\
                   'WHERE id IN %s '\
                   'GROUP BY account_id,reconcile_id',
                   (tuple(ids), ))
        r = cr.fetchall()
        #modify in here: remove constraint
        #
        if not unrec_lines:
            raise osv.except_osv(_('Error!'), _('Entry is already reconciled.'))
        account = account_obj.browse(cr, uid, account_id, context=context)
        if not account.reconcile:
            raise osv.except_osv(_('Error'), _('The account is not defined to be reconciled !'))
        if r[0][1] != None:
            raise osv.except_osv(_('Error!'), _('Some entries are already reconciled.'))

        if (not currency_obj.is_zero(cr, uid, account.company_id.currency_id, writeoff)) or \
           (account.currency_id and (not currency_obj.is_zero(cr, uid, account.currency_id, currency))):
            if not writeoff_acc_id:
                raise osv.except_osv(_('Warning!'), _('You have to provide an account for the write off/exchange difference entry.'))
            if writeoff > 0:
                debit = writeoff
                credit = 0.0
                self_credit = writeoff
                self_debit = 0.0
            else:
                debit = 0.0
                credit = -writeoff
                self_credit = 0.0
                self_debit = -writeoff
            # If comment exist in context, take it
            if 'comment' in context and context['comment']:
                libelle = context['comment']
            else:
                libelle = _('Write-Off')

            cur_obj = self.pool.get('res.currency')
            cur_id = False
            amount_currency_writeoff = 0.0
            if context.get('company_currency_id',False) != context.get('currency_id',False):
                cur_id = context.get('currency_id',False)
                for line in unrec_lines:
                    if line.currency_id and line.currency_id.id == context.get('currency_id',False):
                        amount_currency_writeoff += line.amount_currency
                    else:
                        tmp_amount = cur_obj.compute(cr, uid, line.account_id.company_id.currency_id.id, context.get('currency_id',False), abs(line.debit-line.credit), context={'date': line.date})
                        amount_currency_writeoff += (line.debit > 0) and tmp_amount or -tmp_amount

            writeoff_lines = [
                (0, 0, {
                    'name': libelle,
                    'debit': self_debit,
                    'credit': self_credit,
                    'account_id': account_id,
                    'date': date,
                    'partner_id': partner_id,
                    'currency_id': cur_id or (account.currency_id.id or False),
                    'amount_currency': amount_currency_writeoff and -1 * amount_currency_writeoff or (account.currency_id.id and -1 * currency or 0.0)
                }),
                (0, 0, {
                    'name': libelle,
                    'debit': debit,
                    'credit': credit,
                    'account_id': writeoff_acc_id,
                    'analytic_account_id': context.get('analytic_id', False),
                    'date': date,
                    'partner_id': partner_id,
                    'currency_id': cur_id or (account.currency_id.id or False),
                    'amount_currency': amount_currency_writeoff and amount_currency_writeoff or (account.currency_id.id and currency or 0.0)
                })
            ]

            writeoff_move_id = move_obj.create(cr, uid, {
                'period_id': writeoff_period_id,
                'journal_id': writeoff_journal_id,
                'date':date,
                'state': 'draft',
                'line_id': writeoff_lines
            })

            writeoff_line_ids = self.search(cr, uid, [('move_id', '=', writeoff_move_id), ('account_id', '=', account_id)])
            if account_id == writeoff_acc_id:
                writeoff_line_ids = [writeoff_line_ids[1]]
            ids += writeoff_line_ids

        # marking the lines as reconciled does not change their validity, so there is no need
        # to revalidate their moves completely.
        reconcile_context = dict(context, novalidate=True)
        r_id = move_rec_obj.create(cr, uid, {
            'type': type,
            'line_id': map(lambda x: (4, x, False), ids),
            'line_partial_ids': map(lambda x: (3, x, False), ids)
        }, context=reconcile_context)
        # the id of the move.reconcile is written in the move.line (self) by the create method above
        # because of the way the line_id are defined: (4, x, False)
        for id in ids:
            workflow.trg_trigger(uid, 'account.move.line', id, cr)

        if lines and lines[0]:
            partner_id = lines[0].partner_id and lines[0].partner_id.id or False
            if partner_id and not partner_obj.has_something_to_reconcile(cr, uid, partner_id, context=context):
                partner_obj.mark_as_reconciled(cr, uid, [partner_id], context=context)

        #modify for hr_expense
        #when making a full reconciliation of account move lines 'ids', we may need to recompute the state of some hr.expense
        account_move_ids = [aml.move_id.id for aml in self.browse(cr, uid, ids, context=context)]
        expense_obj = self.pool.get('hr.expense.expense')
        currency_obj = self.pool.get('res.currency')
        if account_move_ids:
            expense_ids = expense_obj.search(cr, uid, [('account_move_id', 'in', account_move_ids)], context=context)
            for expense in expense_obj.browse(cr, uid, expense_ids, context=context):
                if expense.state == 'done':
                    #making the postulate it has to be set paid, then trying to invalidate it
                    new_status_is_paid = True
                    for aml in expense.account_move_id.line_id:
                        if aml.account_id.type == 'payable' and not currency_obj.is_zero(cr, uid, expense.company_id.currency_id, aml.amount_residual):
                            new_status_is_paid = False
                    if new_status_is_paid:
                        expense_obj.write(cr, uid, [expense.id], {'state': 'paid'}, context=context)
                        
        return r_id
        
        
#end of account_voucher_line()