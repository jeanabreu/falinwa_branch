# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice_line(orm.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    def compute_unit_price_after_discount(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}

        res = {}        
        if not ids:
            return res
        for invoice_line in self.browse(cr, uid, ids, context=context):
            res[invoice_line.id] = float(invoice_line.price_unit * (100.00 - invoice_line.discount) / 100.00)        
        return res
        
    _columns = {
        'unit_price_after_discount' : fields.function(compute_unit_price_after_discount, type='float',string='Unit Price (After Discount)',
            store={
                'account.invoice.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
    }
    
#end of account_invoice_line()