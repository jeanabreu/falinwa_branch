from openerp.osv import fields, orm
from openerp.tools.translate import _

class multi_cancel_production_wizard(orm.TransientModel):
    _name = "multi.cancel.production.wizard"
    
    def action_cancel(self, cr, uid, ids, context):
        self.pool.get('mrp.production').action_cancel(cr, uid, context.get('active_ids',False), context)
        return True
        
#end of multi_cancel_production_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
