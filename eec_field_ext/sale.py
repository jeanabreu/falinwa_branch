# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'x_expected_date_of_departure' : fields.date('Expected Date of Departure'),
    }

    def _get_date_planned(self, cr, uid, order, line, start_date, context=None):
        date_planned = False
        if order.x_expected_date_of_departure:
            return order.x_expected_date_of_departure + ' 00:00:00'
        return super(sale_order, self)._get_date_planned(cr, uid, order, line, order.date_confirm + ' 00:00:00', context)
        
#end of sale_order()

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'bank_account_number' : fields.char('Bank Account Number', size=128),
    }
    
#end of res_partner()