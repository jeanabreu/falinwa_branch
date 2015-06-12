# -*- coding: utf-8 -*-

import base64
from cStringIO import StringIO
import csv
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit='mrp.bom'
    
    _columns = {
        'product_id_loc_rack' : fields.related('product_id', 'loc_rack', type='char', string='Shelf', readonly=True),
        'product_id_loc_row' : fields.related('product_id', 'loc_row', type='char', string='Layer', readonly=True),
        'product_id_loc_case' : fields.related('product_id', 'loc_case', type='char', string='Box', readonly=True),
        'product_id_standard_price' : fields.related('product_id', 'standard_price', type='float', digits_compute=dp.get_precision('Product Price'), string='Cost Price', readonly=True),
    }
    
    def open_product(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr,uid ,ids)[0]
        return {
            'type': 'ir.actions.act_window',
            'name': data.product_id.name,
            'res_model': 'product.product',
            'res_id' : data.product_id.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
            'nodestroy': True,
        }
        
#end of mrp_bom()

class mrp_bom_line(orm.Model):
    _name = 'mrp.bom.line'
    _inherit='mrp.bom.line'
    
    _columns = {
        'product_id_loc_rack' : fields.related('product_id', 'loc_rack', type='char', string='Shelf', readonly=True),
        'product_id_loc_row' : fields.related('product_id', 'loc_row', type='char', string='Layer', readonly=True),
        'product_id_loc_case' : fields.related('product_id', 'loc_case', type='char', string='Box', readonly=True),
        'product_id_standard_price' : fields.related('product_id', 'standard_price', type='float', digits_compute=dp.get_precision('Product Price'), string='Cost Price', readonly=True),
    }
#end of mrp_bom_line()

class product_product(orm.Model):
    _name = 'product.product'
    _inherit='product.product'
    
    def search(self, cr, uid, args, offset=0, limit=None, order=None, context=None, count=False):
        if context is None:
            context = {}
        if context and context.get('search_barcode', False):
            args.append((('ean13', 'ilike', context['search_barcode'])))
        return super(product_product, self).search(cr, uid, args, offset=offset, limit=limit, order=order, context=context, count=count)
    
    def name_search(self, cr, uid, name='', args=None, operator='ilike', context=None, limit=100):
        if context is None:
            context = {}
        mrp_obj = self.pool.get('mrp.production')
        product_obj = self.pool.get('product.product')
        res = super(product_product, self).name_search(cr, uid, name, args, operator, context, limit=100)
        if not res:
            mrp_ids = mrp_obj.search(cr, uid, [('fal_of_number','ilike',name)], limit=1, context=context)
            for mrp_id in mrp_obj.browse(cr, uid, mrp_ids, context):
                res = product_obj.name_get(cr, uid, [mrp_id.product_id.id], context=context)
        return res
        
#end of product_product()