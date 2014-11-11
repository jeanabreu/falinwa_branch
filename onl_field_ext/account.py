# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class account_invoice(orm.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _columns = {
        'fal_risk_level'  : fields.integer('Risk Level', size= 1, help="Risk Level Code define in number 1 - 9"),
        'fal_risk_level_name'  : fields.char('Risk Level Name', size= 64, help="Risk Level Name"),
        'authorized_id' : fields.many2one('res.partner','Authorized'),
        'date_due': fields.date('Due Date', select=True,
            help="If you use payment terms, the due date will be computed automatically at the generation "\
                "of accounting entries. The payment term may compute several due dates, for example 50% now and 50% in one month, but if you want to force a due date, make sure that the payment term is not set on the invoice. If you keep the payment term and the due date empty, it means direct payment."),
    }
    
    def onchange_payment_term_date_invoice(self, cr, uid, ids, payment_term_id, date_invoice):
        res = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        for invoice in self.browse(cr, uid, ids):
            if invoice.date_due :
                return res
            else :
                res = super(account_invoice, self).onchange_payment_term_date_invoice(cr, uid, ids, payment_term_id, date_invoice)
        return res    
    
#end of account_invoice()