# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp

class mrp_production_detail_wizard(orm.TransientModel):
    _name = "mrp.production.detail.wizard"
    _description = "Production Detail Wizard"

    _columns = {
        'mode': fields.selection([('consume_produce', 'Consume & Produce'),
                                  ('consume', 'Consume Only')], 'Mode', required=True,
                                  help="'Consume only' mode will only consume the products with the quantity selected.\n"
                                        "'Consume & Produce' mode will consume as well as produce the products with the quantity selected "
                                        "and it will finish the production order when total ordered quantities are produced."),
        'product_qty': fields.float('Select Quantity', digits_compute=dp.get_precision('Product Unit of Measure'), required=True),
        'production_detail_line_ids': fields.one2many('mrp.production.detail.line', 'wizard_id',
            'Acreation'),
    }

    def _get_product_qty(self, cr, uid, context=None):
        """ To obtain product quantity
        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param context: A standard dictionary
        @return: Quantity
        """
        if context is None:
            context = {}
        prod = self.pool.get('mrp.production').browse(cr, uid,
                                context['active_id'], context=context)
        done = 0.0
        for move in prod.move_created_ids2:
            if move.product_id == prod.product_id:
                if not move.scrapped:
                    done += move.product_qty
        return (prod.product_qty - done) or prod.product_qty

    _defaults = {
         'mode': lambda *x: 'consume_produce',
         'product_qty' : _get_product_qty,
    }

    def do_produce(self, cr, uid, ids, context=None):
        production_id = context.get('active_id', False)
        assert production_id, "Production Id should be specified in context as a Active ID."
        data = self.browse(cr, uid, ids[0], context=context)
        self.pool.get('mrp.production').action_produce(cr, uid, production_id,
                            data.product_qty, data.mode, context=context)
        return {}
        
#end of mrp_production_detail_wizard()

class mrp_production_detail_line(orm.TransientModel):
    _name = 'mrp.production.detail.line'
    _rec_name = 'product_id'

    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(mrp_request_return_line, self).default_get(
            cr, uid, fields, context=context)
        mrp_ids = context.get('act_ids', [])
        if not mrp_ids or len(mrp_ids) != 1:
            return res
        mrp_id, = mrp_ids
        mrp = self.pool.get('mrp.production').browse(
            cr, uid, mrp_id, context=context)
        res.update({
            'location_id': mrp.location_src_id.id,
            'location_dest_id': mrp.location_src_id.id,
            'production_id': mrp.id})
        return res

    _columns = {
        'product_id': fields.many2one('product.product', string="Product",
            required=True),
        'product_qty': fields.float("Quantity",
            digits_compute=dp.get_precision('Product UoM'), required=True),
        'product_uom': fields.many2one('product.uom', 'Unit of Measure',
            required=True,),
        'location_id': fields.many2one('stock.location', 'Location',
            required=True),
        'location_dest_id': fields.many2one('stock.location', 'Dest. Location',
            required=True),
        'move_id': fields.many2one('stock.move', "Move"),
        'production_id': fields.many2one('mrp.production', 'Production'),
        'product_uos': fields.many2one('product.uom', 'Product UOS'),
        'product_uos_qty': fields.float('Quantity UoS'),
        'wizard_id': fields.many2one('mrp.production.detail.wizard', string="Wizard"),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
