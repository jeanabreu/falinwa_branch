# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    #
    payment_term = fields.Many2one(required=True)
    incoterm = fields.Many2one(required=True)
    #

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(sale_order, self)._prepare_invoice(order, lines)
        res['fal_incoterm'] = order.incoterm.id
        return res
        
        
#end of sale_order()
