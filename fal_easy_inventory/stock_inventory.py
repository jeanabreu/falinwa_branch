# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_inventory_line(orm.Model):
    _name = "stock.inventory.line"
    _inherit = "stock.inventory.line"
    
    _columns = {
        'product_id_category' : fields.related('product_id', 'categ_id', type='many2one', relation='product.category', string='Product Category', readonly=True),
    }
        
#end of stock_inventory_line()