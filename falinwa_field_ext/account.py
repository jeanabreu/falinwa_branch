# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    def _get_payment_ids_fal(self, cr, uid, ids, context=None):
        result = {}
        for move in self.pool.get('account.move.line').browse(cr, uid, ids, context=context):
            result[move.invoice.id] = True
        return result.keys()
    
    def _get_effective_payment_dates(self, cr, uid, ids, name, args, context=None):
        result = {}
        for invoice in self.browse(cr, uid, ids, context=context):
            temp = []
            for payment in invoice.payment_ids:
                temp.append(payment.date)
            result[invoice.id] = ";".join(temp)
        return result
        
    _columns = {
        'fal_risk_level'  : fields.integer('Risk Level', size= 1, help="Risk Level define in number 1 - 9"),
        'fal_risk_level_name'  : fields.char('Risk Level Name', size= 64, help="Risk Level Name"),
        'fal_effective_payment_dates' : fields.function(_get_effective_payment_dates, type='char',string='Effective Payment Dates',
            store={
                'account.move.line': (_get_payment_ids_fal, [], 20),
            }, help="The efective payment dates."),
    }
#end of account_invoice()

class account_bank_statement(orm.Model):
    _name = 'account.bank.statement'
    _inherit = 'account.bank.statement'
    _columns = {
        'fal_description' : fields.text('Description'),
        'fal_remark' : fields.text('Remark'),
    }
#end of account_bank_statement()

class account_bank_statement_line(orm.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'
    _columns = {
        'ref': fields.char('Reference', size=64),
    }
#end of account_bank_statement_line()

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
            symbol = 'HK$'
            res = {}
            res['fal_debit_hk'] = 0.0
            res['fal_credit_hk'] = 0.0            
            rate_ids = currency_pool.search(cr, uid,[('symbol', '=', symbol),('company_id','=',company_id)] , context=ctx, limit=1)
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
            store={'account.move.line': (lambda self, cr, uid, ids, c={}: ids, [], 20)},
            multi='hk',
            help="Debit in HK Dollar."),
        'fal_credit_hk': fields.function(_amount_all_to_hk, type='float',digits_compute=dp.get_precision('Account'), string='Credit (HKD)',
            store={'account.move.line': (lambda self, cr, uid, ids, c={}: ids, [], 20)},
            multi='hk',
            help="Credit in HK Dollar."),
    }
#end of account_move_line()