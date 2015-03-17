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
    fal_expected_delivery_date = fields.Datetime('Delivery Date')
    #end here
        
#end of account_invoice()
