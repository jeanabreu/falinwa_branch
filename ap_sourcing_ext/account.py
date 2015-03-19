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
    fal_incoterm = fields.Many2one('stock.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.", required=True)
    payment_term = fields.Many2one(required=True)
    #end here
        
#end of account_invoice()

