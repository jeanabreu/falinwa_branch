import time

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class hr_expense_line(orm.Model):
    _name = "hr.expense.line"
    _inherit = "hr.expense.line"
    
    _columns = {
        'fal_reason_why' : fields.selection([('customer','With Customer'), ('manager','With Manager'), ('Director Approve','Approved by Pascal before booking'), ('director','Require Refund To Director'), ('employee','Require at Employee Charge')], string="Reason"),
    }

#end of hr_expense_line()