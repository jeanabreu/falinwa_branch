# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class account_invoice_line(orm.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    def _get_account_invoice(self, cr, uid, ids, context=None):
        result = {}
        for invoice_id in self.pool.get('account.invoice').browse(cr, uid, ids, context):
            for invoice_line_id in invoice_id.invoice_line:
                result[invoice_line_id.id] = True
        return result.keys()

    _columns = {
        'fal_status'  : fields.related('invoice_id','state',string="State",type='char',
            store={
                'account.invoice' : (_get_account_invoice,['state'],10),
            },readonly=True
            ),
    }
#end of account_invoice_line()
