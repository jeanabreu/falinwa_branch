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
    fal_expected_delivery_date = fields.Datetime('Delivery Date')
    #end here

    @api.model
    def _get_date_planned(self, order, line, start_date):
        date_planned = False
        if order.fal_expected_delivery_date:
            return datetime.strptime(order.fal_expected_delivery_date, DEFAULT_SERVER_DATETIME_FORMAT)
        return super(sale_order, self)._get_date_planned(order, line, start_date)
    
    @api.model
    def _prepare_invoice(self, order, lines):
        res = super(sale_order, self)._prepare_invoice(order, lines)
        res['fal_expected_delivery_date'] = order.fal_expected_delivery_date
        return res
    
#end of sale_order()
