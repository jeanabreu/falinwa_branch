# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from datetime import datetime, timedelta

class purchase_order(models.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'

    #fields start here
    fal_delivery_address = fields.Text('Delivery Address', track_visibility='onchange')
    #end here

    @api.multi
    def onchange_dest_address_id(self, address_id, related_usage):
        res = super(purchase_order, self).onchange_dest_address_id(address_id)
        delivery_partner_id = self.env['res.partner'].browse(address_id)
        if delivery_partner_id:
            res['value']['fal_delivery_address'] = delivery_partner_id.contact_address
            if related_usage != 'customer':
                res['value']['location_id'] = False
        return res

    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(purchase_order, self)._prepare_invoice(order, lines)
        res['fal_delivery_address'] = order.fal_delivery_address
        return res
        
#end of purchase_order()
