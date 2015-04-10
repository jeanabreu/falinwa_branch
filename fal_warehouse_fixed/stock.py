# -*- coding: utf-8 -*-
from openerp import fields, models


class stock_move(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    propagate = fields.Boolean(default=False)
    
#end of stock_move()