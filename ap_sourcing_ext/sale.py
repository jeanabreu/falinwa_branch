# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"    
        
    @api.depends('order_line.discount')
    def _fal_discount_exists(self):
        for rec in self:
            self.fal_discount_exists = False
            for line in rec.order_line:
                if line.discount:                    
                    self.fal_discount_exists = True
                        
    #fields start here
    payment_term = fields.Many2one(required=True)
    incoterm = fields.Many2one(required=True)
    fal_discount_exists = fields.Boolean(string='Discount Exists', compute='_fal_discount_exists',
            help='It indicates that sales order has at least one discount.')
    #end here

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(sale_order, self)._prepare_invoice(order, lines)
        res['fal_incoterm'] = order.incoterm.id
        return res
        
        
#end of sale_order()
