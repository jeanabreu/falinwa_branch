# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.exceptions import except_orm, Warning, RedirectWarning

class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'

    @api.one
    @api.depends('purchase_ids')
    def _get_related_customer_invoice_ids(self):
        self.related_customer_invoice_ids = self.env['account.invoice']
        purchase_order = self.env['purchase.order']
        for invoice in self:
            if invoice.purchase_ids:
                purchase_order = invoice.purchase_ids[0]
            if purchase_order.sale_order_line_order_id.invoice_ids:
                self.related_customer_invoice_ids = purchase_order.sale_order_line_order_id.invoice_ids
            else:
                self.related_customer_invoice_ids = self.env['account.invoice']
    
    related_customer_invoice_ids = fields.Many2many('account.invoice', compute='_get_related_customer_invoice_ids')
    
    
#end of account_invoice()