# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(models.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    #fields start here
    payment_term_id = fields.Many2one(required=True)
    incoterm_id = fields.Many2one(required=True)
    #end here
        
        
#end of purchase_order()
