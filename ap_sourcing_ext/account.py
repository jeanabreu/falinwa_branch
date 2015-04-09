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

class res_partner_bank(models.Model):
    _name = "res.partner.bank"
    _inherit = "res.partner.bank"
    
    #fields start here
    fal_bank_street = fields.Char('Bank Street')
    fal_bank_zip = fields.Char('Bank Zip', change_default=True, size=24)
    fal_bank_city = fields.Char('Bank City')
    fal_bank_country_id = fields.Many2one('res.country', 'Bank Country',
       change_default=True)
    fal_bank_state_id = fields.Many2one("res.country.state", 'Bank Fed. State',
       change_default=True, domain="[('country_id','=',country_id)]")
    #end here

#end of res_partner_bank()
