import time

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _
import time

import openerp.addons.decimal_precision as dp

class hr_expense_expense(orm.Model):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"

    _columns = {
        'force_generate_accounting_entries_date': fields.date('Force Entries Date', select=True, readonly=True, states={'draft':[('readonly',False)], 'confirm':[('readonly',False)], 'accepted':[('readonly',False)]}),
        'fal_expense_number' : fields.char('Expense Number', size=64),
    }
    
    def account_move_get(self, cr, uid, expense_id, context=None):
        res = super(hr_expense_expense, self).account_move_get(cr, uid, expense_id, context)
        #modify start here
        date_mature = time.strftime('%Y-%m-%d')
        expense = self.browse(cr, uid, expense_id) 
        if expense.force_generate_accounting_entries_date:
            date_mature = expense.force_generate_accounting_entries_date
        #end here
        period_obj = self.pool.get('account.period')
        res['date'] = date_mature
        res['period_id'] = period_obj.find(cr, uid, date_mature, context)[0],
        self.write(cr, uid, [expense_id], {
            'force_generate_accounting_entries_date': date_mature,
        })
        return res

    def create(self, cr, uid, vals, context=None):
        vals['fal_expense_number'] = self.pool.get('ir.sequence').get(cr, uid, 'expense.fwa') or '/'
        return super(hr_expense_expense, self).create(cr, uid, vals, context=context) 

    def action_move_create(self, cr, uid, ids, context=None):
        res = super(hr_expense_expense, self).action_move_create(cr, uid, ids, context)
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        for exp in self.browse(cr, uid, ids, context=context):
            if exp.account_move_id:
                for line in exp.account_move_id.line_id:
                    if line.name == '/':
                        move_line_obj.write(cr ,uid, [line.id], {
                            'name': exp.fal_expense_number,
                        })
        return res
        
#end of hr_expense_expense()
