# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    _columns = {
        'fal_invoice_term' : fields.char('Invoice Term',size=128),
    }
        
#end of purchase_order()