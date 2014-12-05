# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    _columns = {
        'project_id': fields.many2one('account.analytic.account', 'Project', help="The analytic account related to a MO."),    
    }
    
#end of mrp_production()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'

    def make_mo(self, cr, uid, ids, context=None):
        mrp_obj = self.pool.get('mrp.production')
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        for po in self.browse(cr, uid, ids):
            if po.sale_order_line_id:
                mrp_obj.write(cr, uid, res[po.id], {'project_id': po.sale_order_line_id.order_id.project_id.id})
        return res
        
#end of procurement_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
