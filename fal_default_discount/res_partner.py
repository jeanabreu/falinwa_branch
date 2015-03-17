# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class res_partner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    fal_discount = fields.Float(string='Discount (%)', digits= dp.get_precision('Discount'),
        default=0.0)
    
#end of res_partner()