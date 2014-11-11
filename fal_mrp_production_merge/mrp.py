# -*- encoding: latin-1 -*-
import datetime

from openerp.osv import orm, fields
from openerp.tools.translate import _

class mrp_production(orm.Model):
    _inherit = 'mrp.production'

    _columns = {
        'merged_into_id': fields.many2one('mrp.production', 'Merged into', required=False, readonly=True, help='Production order in which this production order has been merged into.'),
        'merged_from_ids': fields.one2many('mrp.production', 'merged_into_id', 'Merged from', help='List of production orders that have been merged into the current one.'),
    }

    def _merge(self, cr, uid, ids, context):
        """
        Cancels two or more production orders and merges them into a new one. Productions
        must be in 'confirmed' state in order to be merged.
        """

        if len(ids) <= 1:
            return False

        main = self.browse(cr, uid, ids[0], context)
        if main.state != 'confirmed':
            raise osv.except_osv(_('Error !'), _('Production order "%s" is not in "Waiting Goods" state.') % main.name)

        # Create new production, but ensure product_lines is kept empty.
        new_production_id = self.copy(cr, uid, ids[0], {
            'product_lines': [],
            'move_prod_id': False,
        }, context=context)
        new_production = self.browse(cr, uid, new_production_id, context)
        new_move_lines = {}
        new_move_created_ids = {}

        # Consider fields that are NOT required.
        new_bom_id = new_production.bom_id and new_production.bom_id.id or False
        new_routing_id = new_production.routing_id and new_production.routing_id.id or False
        new_product_uos = new_production.product_uos and new_production.product_uos.id or False

        product_qty = 0
        product_uos_qty = 0
        picking_ids = []
        temp_origin = []
        for production in self.browse(cr, uid, ids, context):
            if production.state != 'confirmed':
                raise osv.except_osv(_('Error !'), _('Production order "%s" is not in "Waiting Goods" state.') % production.name)
            # Check required fields are equal
            if production.product_id != new_production.product_id:
                raise osv.except_osv(_('Error !'), _('Production order "%s" product is different from the one in the first selected order.') % production.name)
            if production.product_uom != new_production.product_uom:
                raise osv.except_osv(_('Error !'), _('Production order "%s" UOM is different from the one in the first selected order.') % production.name)

            # Check not required fields are equal
            bom_id = production.bom_id and production.bom_id.id or False
            if bom_id != new_bom_id:
                raise osv.except_osv(_('Error !'), _('Production order "%s" BOM is different from the one in the first selected order.') % production.name)

            routing_id = production.routing_id and production.routing_id.id or False
            if routing_id != new_routing_id:
                raise osv.except_osv(_('Error !'), _('Production order "%s" routing is different from the one in the first selected order.%s - %s') % (production.name, production.routing_id, new_production.routing_id) )

            product_uos = production.product_uos and production.product_uos.id or False
            if product_uos != new_product_uos:
                raise osv.except_osv(_('Error !'), _('Production order "%s" UOS is different from the one in the first selected order.') % production.name)

            product_qty += production.product_qty
            product_uos_qty += production.product_uos_qty

            picking_ids.append( production.picking_id.id )
            temp_origin.append(production.origin)

        self.write(cr, uid, [new_production_id], {
            'product_qty': product_qty,
            'product_uos_qty': product_uos_qty,
            'origin': ": ".join(temp_origin),
        }, context )

        # As workflow calls may commit to db we do it at the very end of the process
        # so we minimize the probabilities of problems.

        self.action_compute(cr, uid, [new_production_id])
        workflow = netsvc.LocalService("workflow")
        workflow.trg_validate(uid, 'mrp.production', new_production_id, 'button_confirm', cr)

        self.write(cr, uid, ids, {
            'merged_into_id': new_production_id,
        }, context)

        # Cancel 'old' production: We must cancel pickings before cancelling production orders
        for id in picking_ids:
            workflow.trg_validate(uid, 'stock.picking', id, 'button_cancel', cr)
        for id in ids:
            workflow.trg_validate(uid, 'mrp.production', id, 'button_cancel', cr)

        return new_production_id

#end of mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
