# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
        
    def _get_net_margin(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        margin = 0.00
        for product_id in self.browse(cr, uid, ids, context=context):
            if product_id.bom_ids:
                margin = product_id.list_price - product_id.fal_bom_costs
            else:
                margin = product_id.list_price - product_id.standard_price            
            res[product_id.id] = margin
        return res
    
    def _get_bom(self, cr, uid, ids, context=None):
        result = {}
        for bom in self.pool.get('mrp.bom').browse(cr, uid, ids, context=context):
            result[bom.product_id.id] = True
        return result.keys()
        
    _columns = {
        'fal_net_margin' : fields.function(_get_net_margin, type='float', string='Net Margin',
            help="Net Margin",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'product.product' :  (lambda self, cr, uid, ids, c={}: ids, [], 20),
                'mrp.bom' : (_get_bom, [], 20),
            },
            ),
    }

#end of product_product()