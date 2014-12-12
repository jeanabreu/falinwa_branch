import time

from openerp import netsvc
from openerp.osv import fields, orm
from openerp.tools.translate import _

import openerp.addons.decimal_precision as dp

class hr_expense_expense(orm.Model):
    _name = "hr.expense.expense"
    _inherit = "hr.expense.expense"

    def move_line_get_item(self, cr, uid, line, context=None):
        if line.supplier_invoice_line_id:
            return False
        return super(hr_expense_expense, self).move_line_get_item(cr, uid, line, context)

#end of hr_expense_expense()

class hr_expense_line(orm.Model):
    _name = "hr.expense.line"
    _inherit = "hr.expense.line"
        
    _columns = {
        'supplier_invoice_line_id' : fields.many2one('account.invoice.line', 'Supplier Invoice Line'),
        'paid_by_company' : fields.boolean('Paid By Company'),
    }
        
    def onchange_supplier_invoice_line_id(self, cr, uid, ids, supplier_invoice_line_id, context=None):
        res = {'value' : {}}
        if supplier_invoice_line_id:
            invoice_line_id = self.pool.get('account.invoice.line').browse(cr, uid, supplier_invoice_line_id, context=context)
            res['value']['fal_real_amount'] = invoice_line_id.price_subtotal_vat
            res['value']['fal_quantity'] = invoice_line_id.quantity
            res['value']['fal_real_currency'] = invoice_line_id.invoice_id.currency_id.id
        return res
        
#end of hr_expense_line()