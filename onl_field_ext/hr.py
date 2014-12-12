# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class hr_expense_expense(orm.Model):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    
    def onchange_currency_id(self, cr, uid, ids, currency_id=False, company_id=False, context=None):
        res =  {}
        return res
    
#end of hr_expense_expense()

class hr_expense_line(orm.Model):
    _name = "hr.expense.line"
    _inherit = "hr.expense.line"
    _order = "id asc"
    _columns = {
        'analytic_account': fields.many2one('account.analytic.account','Project Number'),
    }
    
#end of hr_expense_line()