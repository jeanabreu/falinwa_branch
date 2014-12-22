# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, orm
from openerp.tools.translate import _

class account_bank_statement(orm.Model):
    
    _inherit = 'account.bank.statement'
    
    def onchange_journal_id(self, cr, uid, statement_id, journal_id, context=None):
        if not journal_id:
            return {}
        res = super(account_bank_statement, self).onchange_journal_id(cr, uid, statement_id, journal_id, context=context)
        account_id = self.pool.get('account.journal').read(cr, uid, journal_id, ['default_debit_account_id'], context=context)['default_debit_account_id']
        res['value'].update({'account_id': account_id})
        return res
    
    def _end_balance(self, cursor, user, ids, name, attr, context=None):
        if context is None:
            context = {}
        res = {}
        res_currency_obj = self.pool.get('res.currency')
        res_users_obj = self.pool.get('res.users')
        company_currency_id = res_users_obj.browse(cursor, user, user, context=context).company_id.currency_id.id
        for statement in self.browse(cursor, user, ids, context=context):
            res[statement.id] = statement.balance_start
            stmt_currency_id = statement.currency.id
            for line in statement.line_ids:
                res[statement.id] += line.amount

            for move_line in statement.move_line_ids:
                if move_line.currency_id.id == stmt_currency_id and move_line.amount_currency != 0:
                    if move_line.debit > 0 and move_line.account_id.id == \
                                statement.journal_id.default_debit_account_id.id:
                        res[statement.id] += move_line.amount_currency
                    if move_line.credit > 0 and move_line.account_id.id == \
                                statement.journal_id.default_credit_account_id.id:
                        res[statement.id] += move_line.amount_currency
                else:
                    ctx = context.copy()
                    ctx.update({'date': move_line.date})
                    if move_line.debit > 0:
                        if move_line.account_id.id == \
                                statement.journal_id.default_debit_account_id.id:
                            res[statement.id] += res_currency_obj.compute(cursor,
                                    user, company_currency_id, stmt_currency_id,
                                    move_line.debit, context=ctx)
                    else:
                        if move_line.account_id.id == \
                                statement.journal_id.default_credit_account_id.id:
                            res[statement.id] -= res_currency_obj.compute(cursor,
                                    user, company_currency_id, stmt_currency_id,
                                    move_line.credit, context=ctx)
        return res
        
    def _margin_compute(self, cursor, user, ids, name, attr, context=None):
        res = {}
        res_currency_obj = self.pool.get('res.currency')
        res_users_obj = self.pool.get('res.users')
        company_currency_id = res_users_obj.browse(cursor, user, user, context=context).company_id.currency_id.id
        for statement in self.browse(cursor, user, ids, context=context):
            res[statement.id] = statement.balance_end_real - statement.balance_end
        return res
    
    def _get_statement(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('account.bank.statement.line').browse(cr, uid, ids, context=context):
            result[line.statement_id.id] = True
        return result.keys()
    
    _columns = {
            'margin_compute' : fields.function(_margin_compute,
                    store = {
                        'account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['line_ids','move_line_ids','balance_start','temp_state','balance_end_real'], 100),
                        'account.bank.statement.line': (_get_statement, ['amount'], 100),
                    },
                    string="Computed Margin", help='Margin as calculated Ending balance minuse Computed Balance'),
            'temp_state' : fields.char('Temp',size=64),
            'balance_end': fields.function(_end_balance,
                    store = {
                        'account.bank.statement': (lambda self, cr, uid, ids, c={}: ids, ['line_ids','move_line_ids','balance_start','temp_state'], 100),
                        'account.bank.statement.line': (_get_statement, ['amount'], 100),
                    },
                    string="Computed Balance", help='Balance as calculated based on Starting Balance and transaction lines'),
    }

    def button_dummy(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        for statement in self.browse(cr, uid, ids, context=context):
            if statement.temp_state and statement.temp_state == '1' :
                self.write(cr, uid, ids, {'temp_state':'2'}, context=context)
            else:
                self.write(cr, uid, ids, {'temp_state':'1'}, context=context)
        return self.write(cr, uid, ids, {}, context=context)
        
    def button_line_delete(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        for statement in self.browse(cr, uid, ids, context=context):
            if statement.move_line_ids:    
                self.write(cr, uid, ids, 
                {
                    'move_line_ids' : [ (5, False, False) ],
                })
        return self.write(cr, uid, ids, {}, context=context)

    def button_confirm_bank(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
            
        res = super(account_bank_statement, self).button_confirm_bank(cr, uid, ids, context=context)
        for statement in self.browse(cr, uid, ids, context=context):
            for statement_line in statement.line_ids:
                if not statement_line.account_id:
                    raise orm.except_orm(_('Error!'),_('There\'s still bank statement line that has no account yet, please filled it or click reconcile button.'))
        return res

    def _prepare_move_line_vals(self, cr, uid, st_line, move_id, debit, credit, currency_id=False,
                amount_currency=False, account_id=False, partner_id=False, context=None):
        res = super(account_bank_statement, self)._prepare_move_line_vals(cr, uid, st_line, move_id, debit, credit, currency_id=currency_id,
                amount_currency=amount_currency, account_id=account_id, partner_id=partner_id, context=context)
        res['analytic_account_id'] = st_line.analytic_account_id.id
        return res
        
#end of account_bank_statement()

class account_bank_statement_line(orm.Model):
    _name = "account.bank.statement.line"
    _inherit = "account.bank.statement.line"
    
    _columns = {
        'analytic_account_id': fields.many2one('account.analytic.account', 'Analytic Account'),
    }
    
#end of account_bank_statement_line()


class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    def cancel_voucher(self, cr, uid, ids, context=None):
        
        reconcile_pool = self.pool.get('account.move.reconcile')
        move_pool = self.pool.get('account.move')

        for voucher in self.browse(cr, uid, ids, context=context):
            # refresh to make sure you don't unlink an already removed move
            voucher.refresh()
            recs = []
            for line in voucher.move_ids:
                if line.statement_id and line.statement_id.state == 'confirm':
                    raise orm.except_orm(_("Warning"), _('Can\'t be unreconciled because the bank statement: "%s" is already closed, Please open the bank statement first!') % line.statement_id.name)

        return super(account_voucher, self).cancel_voucher(cr, uid, ids, context)
    
#end of account_voucher()