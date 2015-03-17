# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime, timedelta

class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    #fields start here
    fal_delivery_address = fields.Text('Delivery Address')
    #end here

    @api.multi
    def onchange_partner_id(self, type, partner_id, date_invoice=False,
            payment_term=False, partner_bank_id=False, company_id=False):
        res = super(account_invoice, self).onchange_partner_id(type, partner_id, date_invoice=date_invoice,
            payment_term=payment_term, partner_bank_id=partner_bank_id, company_id=company_id)
        delivery_partner_id = self.env['res.partner'].browse(partner_id)
        if partner_id:
            res['value']['fal_delivery_address'] = delivery_partner_id.contact_address
        return res
        
#end of account_invoice()
