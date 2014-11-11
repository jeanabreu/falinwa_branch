# -*- encoding: utf-8 -*-

import time
from openerp.osv import fields, orm
from openerp import netsvc
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class hr_expense_expense(orm.Model):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"
    
    def expense_canceled(self, cr, uid, ids, context=None):
        obj_move_line = self.pool.get('account.move.line')
        obj_move = self.pool.get('account.move')
        res = super(hr_expense_expense,
                        self).expense_canceled(cr, uid, ids, context=context)
        for expense in self.browse(cr, uid, ids, context=context):
            if expense.account_move_id:
                obj_move_line._remove_move_reconcile(cr, uid,
                    [move_line.id
                        for move_line in expense.account_move_id.line_id],
                    context=context)
                obj_move.unlink(cr, uid, [expense.account_move_id.id],
                                context=context)
        return res
        
#end of hr_expense_expense()