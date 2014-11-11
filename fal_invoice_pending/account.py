# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
    
    _columns = {
        'state': fields.selection([
            ('draft','Draft'),
            ('proforma','Pro-forma'),
            ('proforma2','Pro-forma'),
            ('open','Open'),
            ('paid','Paid'),
            ('cancel','Cancelled'),
            ('pending','Pending'),
            ],'Status', select=True, readonly=True, track_visibility='onchange',
            help=' * The \'Draft\' status is used when a user is encoding a new and unconfirmed Invoice. \
            \n* The \'Pro-forma\' when invoice is in Pro-forma status,invoice does not have an invoice number. \
            \n* The \'Open\' status is used when user create invoice,a invoice number is generated.Its in open status till user does not pay invoice. \
            \n* The \'Paid\' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled. \
            \n* The \'Cancelled\' status is used when user cancel invoice.'),
    }
    
    def action_button_pending(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for sale_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'pending',
                }, context=context)
        return True
        
    def action_button_unpending(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for sale_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'open',
                }, context=context)
        return True
        
#end of account_invoice()
