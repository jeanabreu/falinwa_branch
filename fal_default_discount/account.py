# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime, timedelta

class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    
    @api.model
    def _get_default_discount(self):
        discount = False
        if self._context.get('partner', False):            
            partner_id = self.env['res.partner'].browse(self._context['partner'])
            discount = partner_id.fal_discount
        return discount
        
    _defaults = {
        'discount' : _get_default_discount,
    } 
    
#end of account_invoice_line()
