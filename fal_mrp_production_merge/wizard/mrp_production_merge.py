from openerp.osv import fields, orm
from openerp.tools.translate import _

class mrp_production_merge(orm.TransientModel):
    _name = "mrp.production.merge.wizard"
    
    def merge(self, cr, uid, ids, context):
        
        if not context.get('active_ids',False) or len(context.get('active_ids',False)) <= 1:
            raise osv.except_osv(_('Error !'), _('You must select at least two production orders!'))
        new_production_id = self.pool.get('mrp.production')._merge(cr, uid, context.get('active_ids',False), context)
        return {
            'domain': "[('id','=',%d)]" % new_production_id,
            'name': _('Production Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'mrp.production',
            'view_id': False,
            'type': 'ir.actions.act_window'
        }
        
#end of mrp_production_merge()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
