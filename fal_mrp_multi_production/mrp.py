# -*- encoding: utf-8 -*-
import datetime
from openerp.osv import fields, orm
from openerp.tools.translate import _

class mrp_production(orm.Model):
    _inherit = 'mrp.production'

    def _force_production(self, cr, uid, ids, context):
        self.force_production(cr, uid, ids, [])
        for mrp_id in self.browse(cr, uid, ids):
            self.action_produce(cr, uid, mrp_id.id, mrp_id.product_qty, 'consume_produce', context)
        return True
    
    
#end of mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
