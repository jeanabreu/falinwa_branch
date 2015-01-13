import time

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class hr_expense_line(orm.Model):
    _name = "hr.expense.line"
    _inherit = "hr.expense.line"
    
    def _fal_reason_why_selection(self, cr, uid, context=None):
        res= super(hr_expense_line, self)._fal_reason_why_selection(cr, uid, context=context)
        res.append(('Director Approve','Approved by Pascal before booking'))
        return res

    _columns = {
        'fal_reason_why' : fields.selection(_fal_reason_why_selection, string="Reason"),
    }

#end of hr_expense_line()