# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'state': fields.selection([
            ('draft', 'Draft Quotation'),
            ('sent', 'Quotation Sent'),
            ('cancel', 'Cancelled'),
            ('validated','validated'),
            ('waiting_date', 'Waiting Schedule'),
            ('progress', 'Sales Order'),
            ('manual', 'Sale to Invoice'),
            ('shipping_except', 'Shipping Exception'),
            ('invoice_except', 'Invoice Exception'),
            ('done', 'Done'),
            ('stopped', 'Stopped'),
            ], 'Status', readonly=True,help="Gives the status of the quotation or sales order.\
              \nThe exception status is automatically set when a cancel operation occurs \
              in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
               but waiting for the scheduler to run on the order date. The 'Stopped' status is set when the sale order is just to stop", select=True),
    }
    
    def action_button_stop(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for sale_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'stopped',
                }, context=context)
        return True
        
    def action_button_unstop(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for sale_id in self.browse(cr, uid, ids, context=context):
            self.write(cr, uid, ids, {
                'state' : 'progress',
                }, context=context)
        return True
        
#end of sale_order()
