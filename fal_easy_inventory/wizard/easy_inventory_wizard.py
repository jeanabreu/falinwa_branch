# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class easy_inventory_wizard(orm.TransientModel):
    _name = "easy.inventory.wizard"
    _description = "Easy Inventory Wizard"
    
    _columns = {
        'state': fields.selection([('page1', 'page1'), ('page2', 'page2')], 'State'),
        'name': fields.char('Inventory Reference', size=64, required=True),
        'ean13': fields.char('EAN13 Barcode', size=13, help="International Article Number used for product identification."),
        'product_id' : fields.many2one('product.product', 'Product'),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure'),
        'inventory_line_wizard_ids' : fields.one2many('easy.inventory.line.wizard', 'easy_inventory_wizard_id', 'Inventories'),
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
                'inventory_line_wizard_ids': [(0, 0,  {
                    'product_id': data_wizard.product_id.id,  
                    'product_qty': data_wizard.product_qty,
                    'product_uom': data_wizard.product_uom.id or data_wizard.product_id.uom_id.id
                    })]}, context)
        else: 
            raise orm.except_orm(_("Warning"), _('Please Provide Product and Quantity Information to validate..')) 
        return {
             'type': 'ir.actions.act_window',
             'name': "Easy Inventory",
             'res_model': 'easy.inventory.wizard',
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
        if data_wizard.inventory_line_wizard_ids:
            for inventory_line_wizard_id in data_wizard.inventory_line_wizard_ids:
                temp_inventory_line.append((0,0,{
                    'product_id' : inventory_line_wizard_id.product_id.id,
                    'product_uom' : inventory_line_wizard_id.product_uom.id,
                    'product_qty' : inventory_line_wizard_id.product_qty,
                    }))
        else :
            raise orm.except_orm(_("Warning"), _('Please Provide Physical Inventory Line Information to save..')) 
        res_id = stock_inventory_obj.create(cr, uid, {
            'name' : data_wizard.name,
            'inventory_line_id' : temp_inventory_line
            } ,context)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.inventory',
            'view_type': 'form',
            'view_mode': 'form',
            'name': 'Physical Inventories',
            'res_id': res_id,
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

#end of easy_inventory_wizard()

class easy_inventory_line_wizard(orm.TransientModel):
    _name = "easy.inventory.line.wizard"
    _description = "Easy Inventory Line Wizard"
    
    _columns = {
        'easy_inventory_wizard_id' : fields.many2one('easy.inventory.wizard', 'Easy Inventory'),
        'product_id' : fields.many2one('product.product', 'Product', required=True),
        'product_qty': fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'product_uom': fields.many2one('product.uom', 'Product Unit of Measure', required=True),
    }
#end of easy_inventory_line_wizard()