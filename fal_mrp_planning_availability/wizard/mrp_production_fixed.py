from openerp.osv import fields, orm
from openerp.tools.translate import _

class mrp_production_fixed(orm.TransientModel):
    _name = "mrp.production.fixed.wizard"
    
    def production_fixed(self, cr, uid, ids, context):
        
        new_production_id = self.pool.get('mrp.production')._production_fixed(cr, uid, context.get('active_ids',False), context)
        return True
        
#end of mrp_production_fixed()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
