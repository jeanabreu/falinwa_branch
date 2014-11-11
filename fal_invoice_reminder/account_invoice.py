# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta

from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    
    def _create_invoice_reminder(self, cr, uid, ids=False, advance_date=3, context=None):
        if not ids:
            ids = self.search(cr, uid, [])
        return self.create_invoice_reminder(cr, uid, ids,advance_date=advance_date ,context=context)

    def create_invoice_reminder(self, cr, uid, ids, advance_dates=[3], context=None):
        mail_obj = self.pool.get('mail.mail')
        ir_attachment_obj = self.pool.get('ir.attachment')
        for advance_date in advance_dates:
            advance_date =  date.today() + timedelta(advance_date)
            invoice_due_ids = self.search(cr, uid, [('date_due', '=', advance_date),('type','=','out_invoice'),('state','not in',['draft','cancel','paid'])], context)
            template_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fal_invoice_reminder', 'email_template_invoice_reminder')[1]
            if invoice_due_ids:
                for invoice_due_id in self.browse(cr, uid, invoice_due_ids, context):
                    if invoice_due_id.partner_id.invoice_reminder and invoice_due_id.partner_id.email:
                        self.pool.get('email.template').send_mail(cr, uid, template_id, invoice_due_id.id, force_send=True, context=context)
        return True
        
#end of account_invoice()