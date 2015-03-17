# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime, timedelta

class sale_order(models.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    #fields start here
    fal_delivery_address = fields.Text('Delivery Address')
    #end here
    
    @api.multi
    def onchange_delivery_id(self, company_id, partner_id, delivery_id, fiscal_position):
        res = super(sale_order, self).onchange_delivery_id(company_id, partner_id, delivery_id, fiscal_position)
        delivery_partner_id = self.env['res.partner'].browse(delivery_id)
        if delivery_partner_id:
            res['value']['fal_delivery_address'] = delivery_partner_id.contact_address
        return res

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(sale_order, self)._prepare_invoice(order, lines)
        res['fal_delivery_address'] = order.fal_delivery_address
        return res
        
#end of sale_order()
