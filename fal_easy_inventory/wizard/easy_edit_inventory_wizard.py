# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class easy_edit_inventory_wizard(orm.TransientModel):
    _name = "easy.edit.inventory.wizard"
    _description = "Easy Edit Inventory Wizard"
    
    _columns = {
        'state': fields.selection([('page1', 'page1'), ('page2', 'page2')], 'State'),
        'inventory_id': fields.many2one('stock.inventory','Stock Inventory'),
        'ean13': fields.char('EAN13 Barcode', size=13, help="International Article Number used for product identification."),
        'product_id' : fields.many2one('product.product', 'Product'),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure'),
        'inventory_edit_line_wizard_ids' : fields.one2many('easy.edit.inventory.line.wizard', 'easy_edit_inventory_wizard_id', 'Inventories'),
    }
    
    def _get_inventory_id(self, cr, uid, context):
        if context is None:
            context = {}
        return context.get('active_id', False)
        
    def _get_inventory_line_ids(self, cr, uid, context):
        if context is None:
            context = {}
        temp = []
        inventory_obj = self.pool.get('stock.inventory')
        inventory_id =  inventory_obj.browse(cr ,uid, context.get('active_id', False))
        for inventory_line_id in inventory_id.inventory_line_id:   
            temp.append((0,0,{
                'inventory_line_id' : inventory_line_id.id,
                'product_id' : inventory_line_id.product_id.id,
                'product_qty' : inventory_line_id.product_qty,
                'product_uom' : inventory_line_id.product_uom.id,
            }))
        return temp 
    
    _defaults = {
        'inventory_id' : _get_inventory_id,
        'inventory_edit_line_wizard_ids' : _get_inventory_line_ids
    }
    
    def validate_product(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]
        if data_wizard.product_id.id and data_wizard.product_qty : 
            self.write(cr, uid , ids , {
                'ean13' : '',
                'product_id' : False,
                'product_qty' : 0.000,
                'product_uom' : False,
                'inventory_edit_line_wizard_ids': [(0, 0,  {
                    'product_id': data_wizard.product_id.id,  
                    'product_qty': data_wizard.product_qty,
                    'product_uom': data_wizard.product_uom.id or data_wizard.product_id.uom_id.id
                    })]}, context)
        else: 
            raise osv.except_osv(_("Warning"), _('Please Provide Product and Quantity Information to validate..')) 
        return {
             'type': 'ir.actions.act_window',
             'name': "Easy Edit Inventory",
             'res_model': 'easy.edit.inventory.wizard',
             'res_id': ids[0],
             'view_type': 'form',
             'view_mode': 'form',
             'target': 'new',
             'nodestroy': True,
        }
       
    def save_easy_inventory(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0]
        stock_inventory_obj = self.pool.get('stock.inventory')
        temp_inventory_line = []
        if data_wizard.inventory_edit_line_wizard_ids:
            for inventory_line_wizard_id in data_wizard.inventory_edit_line_wizard_ids:
                if inventory_line_wizard_id.inventory_line_id:
                    temp_inventory_line.append((1, inventory_line_wizard_id.inventory_line_id.id, {
                        'product_id' : inventory_line_wizard_id.product_id.id,
                        'product_uom' : inventory_line_wizard_id.product_uom.id,
                        'product_qty' : inventory_line_wizard_id.product_qty,
                        }))                    
                else:
                    temp_inventory_line.append((0,0,{
                        'product_id' : inventory_line_wizard_id.product_id.id,
                        'product_uom' : inventory_line_wizard_id.product_uom.id,
                        'product_qty' : inventory_line_wizard_id.product_qty,
                        }))
        else :
            raise osv.except_osv(_("Warning"), _('Please Provide Physical Inventory Line Information to save..')) 
        stock_inventory_obj.write(cr, uid, data_wizard.inventory_id.id, {
            'inventory_line_id' : temp_inventory_line,
            } ,context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inventory',
            'view_type': 'form',
            'view_mode': 'form',
            'name': 'Physical Inventories',
            'res_id': data_wizard.inventory_id.id,
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
        
    def onchange_product(self, cr, uid, ids, product_id, context=None):
        if context is None:
            context = {}
        res = {}
        product_obj = self.pool.get('product.product') 
        if product_id:
            product =  product_obj.browse(cr, uid, product_id, context)
            res['value'] = {'product_uom' : product.uom_id.id}
        return res

#end of easy_edit_inventory_wizard()

class easy_edit_inventory_line_wizard(orm.TransientModel):
    _name = "easy.edit.inventory.line.wizard"
    _description = "Easy Edit Inventory Line Wizard"
    
    _columns = {
        'inventory_line_id': fields.many2one('stock.inventory.line','Stock Inventory Line'),
        'easy_edit_inventory_wizard_id' : fields.many2one('easy.edit.inventory.wizard', 'Easy Edit Inventory'),
        'product_id' : fields.many2one('product.product', 'Product', required=True),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
    }
#end of easy_edit_inventory_line_wizard()