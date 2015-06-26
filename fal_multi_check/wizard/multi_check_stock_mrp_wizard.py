from openerp.osv import fields, orm
from openerp.tools.translate import _

class multi_check_stock_mrp_wizard(orm.TransientModel):
    _name = "multi.check.stock.mrp.wizard"
    
    def action_check(self, cr, uid, ids, context):
        if context.get('active_ids', False):        
            mrp_obj = self.pool.get('mrp.production')
            temp = []
            for mrp in mrp_obj.browse(cr, uid, context.get('active_ids', False), context):
                if mrp.state == 'confirmed':                    
                    temp.append(mrp.id)
            if temp:
                mrp_obj.action_assign(cr, uid, temp, context)
        return True
        
#end of multi_check_stock_mrp_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
