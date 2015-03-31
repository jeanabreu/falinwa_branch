from openerp.osv import fields, orm
from openerp.tools.translate import _

class multi_cancel_procurement_wizard(orm.TransientModel):
    _name = "multi.cancel.procurement.wizard"
    
    def action_cancel(self, cr, uid, ids, context):
        self.pool.get('procurement.order').cancel(cr, uid, context.get('active_ids',False), context)
        return True
        
#end of multi_cancel_procurement_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
