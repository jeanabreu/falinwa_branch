from openerp.osv import fields, orm
from openerp.tools.translate import _

class multi_transfer_picking_wizard(orm.TransientModel):
    _name = "multi.transfer.picking.wizard"
    
    def action_transfer(self, cr, uid, ids, context):
        if context.get('active_ids', False):        
            stock_picking_obj = self.pool.get('stock.picking')
            for picking in stock_picking_obj.browse(cr, uid, context.get('active_ids', False), context):
                if picking.state != 'assigned':
                    raise orm.except_orm(_("Warning"), _('The picking must in Ready To Transfer State.'))
            self.pool.get('stock.picking').do_transfer(cr, uid, context.get('active_ids',False), context)
        return True
        
#end of multi_transfer_picking_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
