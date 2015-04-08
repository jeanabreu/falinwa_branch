# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(models.Model):
    _name = 'stock.picking'
    _inherit = 'stock.picking'

    @api.model
    def _get_invoice_vals(self, key, inv_type, journal_id, move):
        res = super(stock_picking, self)._get_invoice_vals(key, inv_type, journal_id, move)
        res['origin'] = (move.picking_id.name or '') + (move.picking_id.origin and (':' + move.picking_id.origin) or '')
        return res

    
#end of stock_picking()