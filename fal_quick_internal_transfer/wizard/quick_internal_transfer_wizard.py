# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class quick_internal_transfer_wizard(orm.TransientModel):
    _name = "quick.internal.transfer.wizard"
    _description = "Quick Internal Transfer Wizard"

    _columns = {
        'state' : fields.selection([('page1', 'page1'), ('page2', 'page2')], 'State'),
        'name' : fields.char('Internal Transfer Reference', size=64),
        'ean13' : fields.char('Product Barcode', size=13, help="International Article Number used for product identification."),
        'product_id' : fields.many2one('product.product', 'Product'),
        'product_qty' : fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom' : fields.many2one('product.uom', 'Product Unit of Measure'),
        'source_ean13' : fields.char('Source Location Barcode', size=13, help="International Article Number used for source location identification."),
        'source_location_id' : fields.many2one('stock.location', 'Source Location', help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations."),
        'destination_ean13' : fields.char('Destination Location Barcode', size=13, help="International Article Number used for desination location identification."),
        'destination_location_id' : fields.many2one('stock.location', 'Destination Location', help="Location where the system will stock the finished products."),
        'picking_type_id': fields.many2one('stock.picking.type', 'Picking Type'),
        'quick_internal_transfer_line_wizard_ids' : fields.one2many('quick.internal.transfer.line.wizard', 'quick_internal_transfer_wizard_id', 'Operation'),
    }

    def _default_picking_type(self, cr, uid, context=None):
        context = context or {}
        pick_type_ids = self.pool.get('stock.picking.type').search(cr, uid, [
            ('code', '=', 'internal')], context=context)
        
        if pick_type_ids:
            return pick_type_ids[0]
        return False
        
    _defaults = {
        'picking_type_id' : _default_picking_type,
    }
    
    def validate_product(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]
        if data_wizard.product_id.id and data_wizard.product_qty and data_wizard.source_location_id.id and data_wizard.destination_location_id.id : 
            self.write(cr, uid , ids , {
                'ean13' : '',
                'product_id' : False,
                'product_qty' : 0.000,
                'product_uom' : False,
                'source_ean13' : '',
                'source_location_id' : data_wizard.picking_type_id.default_location_src_id.id,
                'destination_ean13' : '',
                'destination_location_id' : data_wizard.picking_type_id.default_location_dest_id.id,
                'quick_internal_transfer_line_wizard_ids': [(0, 0,  {
                    'product_id': data_wizard.product_id.id,  
                    'product_qty': data_wizard.product_qty,
                    'product_uom': data_wizard.product_uom.id or data_wizard.product_id.uom_id.id,
                    'source_location_id': data_wizard.source_location_id.id,
                    'destination_location_id':  data_wizard.destination_location_id.id,
                    })]}, context)
        else: 
            raise orm.except_orm(_("Warning"), _('Please Provide Product, Quantity, and location Information to validate..')) 
        return {
             'type': 'ir.actions.act_window',
             'name': "Quick Internal Transfer",
             'res_model': 'quick.internal.transfer.wizard',
             'res_id': ids[0],
             'view_type': 'form',
             'view_mode': 'form',
             'target': 'new',
             'nodestroy': True,
        }
       
    def save_quick_transfer(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]
        stock_picking_obj = self.pool.get('stock.picking')
        temp_quick_transfer_line = []
        temp_internal_transfer = []
        if data_wizard.quick_internal_transfer_line_wizard_ids:
            
            for quick_internal_transfer_line_wizard_id in data_wizard.quick_internal_transfer_line_wizard_ids:
                temp_quick_transfer_line.append((0,0,{
                    'product_id' : quick_internal_transfer_line_wizard_id.product_id.id,
                    'product_uom' : quick_internal_transfer_line_wizard_id.product_uom.id,
                    'product_uom_qty' : quick_internal_transfer_line_wizard_id.product_qty,
                    'location_id': quick_internal_transfer_line_wizard_id.source_location_id.id,
                    'location_dest_id':  quick_internal_transfer_line_wizard_id.destination_location_id.id,
                    'picking_type_id': data_wizard.picking_type_id.id,
                    'name': quick_internal_transfer_line_wizard_id.product_id.partner_ref,
                    }))
        else :
            raise orm.except_orm(_("Warning"), _('Please Provide Operation information to save..')) 
        for line in temp_quick_transfer_line:
            res_id = stock_picking_obj.create(cr, uid, {
                'origin' : data_wizard.name or 'Quick Internal Transfer',
                'picking_type_id': data_wizard.picking_type_id.id,
                'move_lines' : [line],
                } ,context)            
            temp_internal_transfer.append(res_id)
            #mark to do
            stock_picking_obj.action_confirm(cr, uid, temp_internal_transfer, context=context)
            #force assign
            stock_picking_obj.force_assign(cr, uid, temp_internal_transfer, context=context)
            #do_transfer
            stock_picking_obj.do_transfer(cr, uid, temp_internal_transfer, context=context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'name': 'Internal Transfer',
            'domain' : [('id','in',temp_internal_transfer)],
        }

    def onchange_ean13(self, cr, uid, ids, ean13, context=None):
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool.get('product.product')
        if ean13:
            product_id = product_obj.search(cr, uid, [('ean13', '=', ean13)], limit=1)
            if product_id:
                for i in product_obj.browse(cr, uid, product_id, context):
                    res['value'] = { 'product_id' : i.id, 'product_uom' : i.uom_id.id}
        return res
        
    def onchange_source_ean13(self, cr, uid, ids, source_ean13, context=None):
        if context is None:
            context = {}
        res = {}
        stock_location_obj = self.pool.get('stock.location')
        if source_ean13:
            location_id = stock_location_obj.search(cr, uid, [('loc_barcode', '=', source_ean13)], limit=1)
            if location_id:
                for i in location_id:
                    res['value'] = { 'source_location_id' : i}
        return res
        
    def onchange_destination_ean13(self, cr, uid, ids, destination_ean13, context=None):
        if context is None:
            context = {}
        res = {}
        stock_location_obj = self.pool.get('stock.location')
        if destination_ean13:
            location_id = stock_location_obj.search(cr, uid, [('loc_barcode', '=', destination_ean13)], limit=1)
            if location_id:
                for i in location_id:
                    res['value'] = { 'destination_location_id' : i}
        return res

    def onchange_picking_type(self, cr, uid, ids, picking_type, context=None):
        if context is None:
            context = {}
        res = {}
        picking_type_obj = self.pool.get('stock.picking.type')
        if picking_type:
            picking_type_id = picking_type_obj.browse(cr, uid, picking_type, context=context)
            res['value'] = { 'source_location_id' : picking_type_id.default_location_src_id.id, 'destination_location_id' : picking_type_id.default_location_dest_id.id}
        return res
        
    def onchange_product(self, cr, uid, ids, product_id, context=None):
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool.get('product.product') 
        if product_id:
            product =  product_obj.browse(cr, uid, product_id, context)
            res['value'] = {'product_uom' : product.uom_id.id}
        return res

#end of quick_internal_transfer_wizard()

class quick_internal_transfer_line_wizard(orm.TransientModel):
    _name = "quick.internal.transfer.line.wizard"
    _description = "Quick Internal Transfer Line Wizard"
    
    _columns = {
        'quick_internal_transfer_wizard_id' : fields.many2one('quick.internal.transfer.wizard', 'Quick Internal Transfer'),
        'product_id' : fields.many2one('product.product', 'Product', required=True),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
        'source_location_id' : fields.many2one('stock.location', 'Source Location', required=True, select=True, help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations."),
        'destination_location_id' : fields.many2one('stock.location', 'Destination Location', required=True, select=True, help="Location where the system will stock the finished products."),
    }
#end of quick_internal_transfer_line_wizard()