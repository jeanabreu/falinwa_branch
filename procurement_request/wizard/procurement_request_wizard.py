# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from dateutil.relativedelta import relativedelta
from datetime import date

class procurement_request_wizard(orm.TransientModel):
    _name = "procurement.request.wizard"
    _description = "Procurement Request Wizard"
    
    _columns = {
        'product_id' : fields.many2one('product.product','Product',required=True),
        'product_qty' : fields.float('Quantity', digits_compute=dp.get_precision('Product Unit of Measure')),
        'date_order': fields.date('Order Date', required=True),
        'partner_id' : fields.many2one('res.partner', 'Supplier', required=True),
        'date_planned' : fields.date('Expected Date'),
    }

    def _get_supplier(self, cr, uid, context=None):
        if context is None:
            context = {}
        product_obj = self.pool.get('product.product')
        supplier_obj = self.pool.get('res.partner')
        res = supplier_obj.search(cr, uid, [('name', '=', 'SUPPLIER TO BE DEFINED'),
                                        ('supplier', '=', True)],
                                            limit=1)
        if context.get('active_id',False):
            product_id  = product_obj.browse(cr, uid, context.get('active_id',False))
            if product_id.seller_ids:
                res = [product_id.seller_ids[0].name.id]
        return res and res[0] or False 
        
    _defaults = {
        'date_order': fields.date.context_today,
        'product_qty': lambda *args: 1.0,
        'partner_id': _get_supplier,
    }
    
    def make_procurement_request(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0] 
        purchase_order_obj = self.pool.get('purchase.order')
        warehouse_obj = self.pool.get('stock.warehouse')
        warehouse_id = warehouse_obj.search(cr, uid, [], context=context)[0]
        wh = warehouse_obj.browse(cr ,uid ,warehouse_id , context=context)
        purchase_order_obj.create(cr, uid, {
            'req_product_id' : data_wizard.product_id.id,
            'req_product_description' : data_wizard.product_id.name,
            'req_uom_id' : data_wizard.product_id.uom_po_id.id,
            'req_product_qty' : data_wizard.product_qty,
            'location_id' : wh.wh_input_stock_loc_id.id,
            'date_order' : data_wizard.date_order,
            'partner_id' : data_wizard.partner_id.id,
            'pricelist_id' : data_wizard.partner_id.property_product_pricelist_purchase.id,
            'origin' : 'Direct from Product',
            'minimum_planned_date' : data_wizard.date_planned,
        },context=context)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Procurement Request',
            'res_model': 'purchase.order',
            'view_mode': 'tree',
            'view_type': 'form',
            'view_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'procurement_request', 'fal_procurement_request_tree')[1],
            'target': 'current',
            'nodestroy': False,
            'domain': '[("state","=","procurement_request")]',
             }
#end of procurement_request_wizard()