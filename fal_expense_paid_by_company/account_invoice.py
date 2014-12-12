from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class account_invoice_line(orm.Model):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
        
    _columns = {
        'is_expense':  fields.boolean('Is Expense'),
        'expense_line_ids' : fields.one2many('hr.expense.line', 'supplier_invoice_line_id', 'Expense Line'),
    }

#end of account_invoice_line()
