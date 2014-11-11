# -*- coding: utf-8 -*-
from openerp.osv import orm, fields
from openerp.tools.translate import _
from openerp import netsvc

class fal_expense_line_reason_wizard(orm.TransientModel):
    _name = "fal.expense.line.reason.wizard"
    _description = "Falinwa Expense Line Reason Wizard"
    
    _column = {
        'fal_reason_why' : fields.selection([('customer','With Customer'), ('manager','With Manager'), ('director','Require Refund To Director'), ('employee','Require at Employee Charge')], string="Reason", required=True),
        'fal_reason' : fields.char('Explanation', size=256),    
    }

#end of fal_expense_line_reason_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
