from openerp.osv import fields, orm
from openerp.tools.translate import _

class mrp_production_multi(orm.TransientModel):
    _name = "mrp.production.multi.wizard"
    
    def force_production(self, cr, uid, ids, context):
        
        new_production_id = self.pool.get('mrp.production')._force_production(cr, uid, context.get('active_ids',False), context)
        return True
        
#end of mrp_production_multi()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
