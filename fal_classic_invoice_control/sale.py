# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def action_invoice_create(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        if context is None:
            context = {}
        
        for sale_order_id in self.browse(cr, uid, ids, context=context):
            if sale_order_id.order_policy == 'prepaid':
                self.action_ship_create(cr, uid, ids, context)
                return False
        return super(sale_order, self).action_invoice_create(cr, uid, ids, grouped, states, date_invoice, context)
    
    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(sale_order, self)._prepare_order_picking( cr, uid, order, context)
        res['invoice_state'] = ((order.order_policy=='picking' or order.order_policy=='prepaid') and '2binvoiced') or 'none'
        return res
        
#end of sale_order()