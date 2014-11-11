# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from datetime import datetime, timedelta
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from dateutil.relativedelta import relativedelta

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    _columns = {
        'x_expectingdate_departure' : fields.date('Expecting Date of Departure'),
    }
    
    def _prepare_order_line_procurement(self, cr, uid, order, line, move_id, date_planned, context=None):
        res = super(sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, move_id, date_planned, context)
        res['sale_order_line_id'] = line.id
        res['location_id'] = order.shop_id.warehouse_id.lot_input_id.id 
        return res
    
    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        date_planned = False
        if order.x_expectingdate_departure:
            return order.x_expectingdate_departure
        return super(sale_order, self)._get_date_planned(cr, uid, order, line, order.date_confirm, context)
        
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context)
        if not res.get('final_quotation_number', False): 
            res['final_quotation_number'] = order and order.quotation_number or order.name
        return res
        
#end of sale_order()