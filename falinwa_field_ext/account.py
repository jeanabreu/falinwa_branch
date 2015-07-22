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