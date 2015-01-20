# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    

#end of sale_order()

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"

    def action_done(self, cr, uid, ids, context=None):
        return self.write(cr, uid, ids, {'state': 'done'}, context=context)    

#end of purchase_order()