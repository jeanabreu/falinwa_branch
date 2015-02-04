# -*- coding: utf-8 -*-
import time
from lxml import etree

from openerp import netsvc
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _
from openerp.tools import float_compare
from openerp.report import report_sxw


class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    _columns = {
        'fal_is_expense_employee' : fields.boolean('Employee Payment'),
        'fal_is_tax_employee' : fields.boolean('Tax Payment'),
        'fal_is_employee_receipt' : fields.boolean('Employee Receipt'),
        'fal_is_tax_receipt' : fields.boolean('Tax Receipt'),
        'fal_employee_ledger_account_id' : fields.many2one('account.account', 'Employee Ledger Account',  readonly=True, states={'draft':[('readonly',False)]}),
        'fal_employeer_ledger_account_id' : fields.many2one('account.account', 'Employeer Ledger Account', readonly=True, states={'draft':[('readonly',False)]}),
        'fal_employee_amount' : fields.float('Employee Amount', digits_compute=dp.get_precision('Account'),  readonly=True, states={'draft':[('readonly',False)]}),
        'fal_employeer_amount' : fields.float('Employer Amount', digits_compute=dp.get_precision('Account'), readonly=True, states={'draft':[('readonly',False)]}),
    }
    
    """
    def onchange_partner_id(self, cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context=None):
        res = super(account_voucher, self).onchange_partner_id(cr, uid, ids, partner_id, journal_id, amount, currency_id, ttype, date, context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
            if partner.property_employee_payable and partner.property_employeer_payable:
                res['value']['fal_employee_ledger_account_id'] = partner.property_employee_payable and partner.property_employee_payable.id
                res['value']['fal_employeer_ledger_account_id'] = partner.property_employeer_payable and partner.property_employeer_payable.id
        return res
        
    def onchange_emp_amount(self, cr, uid, ids, fal_employee_amount, fal_employeer_amount, context=None):
        res = {'value':{}}
        res['value']['amount'] = fal_employee_amount + fal_employeer_amount
        return res
    
    
    def voucher_move_line_create2(self, cr, uid, voucher_id, line_total, move_id, company_currency, current_currency, context=None):
        if context is None:
            context = {}
        move_line_obj = self.pool.get('account.move.line')
        voucher = self.pool.get('account.voucher').browse(cr,uid,voucher_id,context)
        debit = credit = debit2 = credit2 = 0.0
        if voucher.type in ('purchase', 'payment'):
            debit = voucher.fal_employee_amount
            debit2 = voucher.fal_employeer_amount
        elif voucher.type in ('sale', 'receipt'):
            credit = voucher.fal_employee_amount
            credit2 = voucher.fal_employeer_amount
        if debit < 0: credit = -debit; debit = 0.0
        if credit < 0: debit = -credit; credit = 0.0
        if debit2 < 0: credit2 = -debit2; debit2 = 0.0
        if credit2 < 0: debit2 = -credit2; credit2 = 0.0
        sign = debit - credit < 0 and -1 or 1
        sign2 = debit2 - credit2 < 0 and -1 or 1
        tot_line = voucher.amount
        rec_lst_ids = []
        move_line1 = {
                'name': voucher.name or '/',
                'debit': debit,
                'credit': credit,
                'account_id': voucher.fal_employee_ledger_account_id.id,
                'move_id': move_id,
                'journal_id': voucher.journal_id.id,
                'period_id': voucher.period_id.id,
                'partner_id': voucher.partner_id.id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': 0.0,
                'date': voucher.date,
                'date_maturity': voucher.date_due
            }
        move_line2 = {
                'name': voucher.name or '/',
                'debit': debit2,
                'credit': credit2,
                'account_id': voucher.fal_employeer_ledger_account_id.id,
                'move_id': move_id,
                'journal_id': voucher.journal_id.id,
                'period_id': voucher.period_id.id,
                'partner_id': voucher.partner_id.id,
                'currency_id': company_currency <> current_currency and  current_currency or False,
                'amount_currency': 0.0,
                'date': voucher.date,
                'date_maturity': voucher.date_due
            }
        id1 = move_line_obj.create(cr, uid, move_line1)
        id2 = move_line_obj.create(cr, uid, move_line2)
        return (tot_line, rec_lst_ids)
        
    def action_move_line_create(self, cr, uid, ids, context=None):
        for voucher_id in self.browse(cr, uid, ids, context):
            if voucher_id.fal_is_tax_employee:
                if context is None:
                    context = {}
                move_pool = self.pool.get('account.move')
                move_line_pool = self.pool.get('account.move.line')
                for voucher in self.browse(cr, uid, ids, context=context):
                    local_context = dict(context, force_company=voucher.journal_id.company_id.id)
                    if voucher.move_id:
                        continue
                    company_currency = self._get_company_currency(cr, uid, voucher.id, context)
                    current_currency = self._get_current_currency(cr, uid, voucher.id, context)
                    # we select the context to use accordingly if it's a multicurrency case or not
                    context = self._sel_context(cr, uid, voucher.id, context)
                    # But for the operations made by _convert_amount, we always need to give the date in the context
                    ctx = context.copy()
                    ctx.update({'date': voucher.date})
                    # Create the account move record.
                    move_id = move_pool.create(cr, uid, self.account_move_get(cr, uid, voucher.id, context=context), context=context)
                    # Get the name of the account_move just created
                    name = move_pool.browse(cr, uid, move_id, context=context).name
                    # Create the first line of the voucher
                    move_line_id = move_line_pool.create(cr, uid, self.first_move_line_get(cr,uid,voucher.id, move_id, company_currency, current_currency, local_context), local_context)
                    move_line_brw = move_line_pool.browse(cr, uid, move_line_id, context=context)
                    line_total = move_line_brw.debit - move_line_brw.credit
                    rec_list_ids = []
                    if voucher.type == 'sale':
                        line_total = line_total - self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
                    elif voucher.type == 'purchase':
                        line_total = line_total + self._convert_amount(cr, uid, voucher.tax_amount, voucher.id, context=ctx)
                    # Create one move line per voucher line where amount is not 0.0
                    line_total, rec_list_ids = self.voucher_move_line_create2(cr, uid, voucher.id, line_total, move_id, company_currency, current_currency, context)

                    # We post the voucher.
                    self.write(cr, uid, [voucher.id], {
                        'move_id': move_id,
                        'state': 'posted',
                        'number': name,
                    })
                    if voucher.journal_id.entry_posted:
                        move_pool.post(cr, uid, [move_id], context={})
                return True
        return super(account_voucher, self).action_move_line_create(cr, uid, ids, context)
    """    
#end of account_voucher()

class res_partner(orm.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    
    _columns = {
        'fal_is_salary_tax_partner' : fields.boolean('Salary Third Party Partner'),
        'property_employee_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Employee Payable",
            view_load=True,
            domain="[('type', '=', 'payable')]"),
        'property_employeer_payable': fields.property(
            type='many2one',
            relation='account.account',
            string="Account Employeer Payable",
            view_load=True,
            domain="[('type', '=', 'payable')]",),
    }
    
#end of res_partner()