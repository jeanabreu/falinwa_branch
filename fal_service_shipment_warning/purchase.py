# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
        
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        todo = []
        for po in self.browse(cr, uid, ids, context=context):
            for line in po.order_line :
                if line.product_id.type == 'service' and po.invoice_method == 'picking':                
                    raise orm.except_orm(_('Warning!'), _("Service product cannot have based on incoming shipment invoice control..!"))
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)
    
        
#end of purchase_order()