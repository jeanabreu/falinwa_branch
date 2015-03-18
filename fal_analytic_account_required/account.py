# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning

class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    
    """
    @api.multi
    def invoice_validate(self):
        for invoice in self:
            for invoice_line in invoice.invoice_line:
                if not invoice_line.account_analytic_id:
                    raise Warning(_('Please filled the analytic account on invoice  line.'))
        return super(account_invoice, self).invoice_validate()
    """    
#end of account_invoice()