# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=context)
        if part:
            part_id = self.pool.get('res.partner').browse(cr, uid, part, context=context)
            if part_id.fal_project_id:
                res['value']['project_id'] = part_id.fal_project_id and part_id.fal_project_id.id
        return res
        
#end of sale_order()
