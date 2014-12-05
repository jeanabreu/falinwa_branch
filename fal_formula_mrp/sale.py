# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def _prepare_order_line_procurement(self, cr, uid, order, line, move_id, date_planned, context=None):
        res = super(sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, move_id, date_planned, context)
        res['sale_order_line_formula_id'] = line.id
        return res

#end of sale_order()

class sale_order_line(orm.Model):
    _name = "sale.order.line"
    _inherit = "sale.order.line"
    
    _columns = {
        'fal_stroke' : fields.integer('Stroke (mm)'),
    }
#end of sale_order_line()

class product_category(orm.Model):
    _name = "product.category"
    _inherit = "product.category"
    
    _columns = {
        'isfal_formula' : fields.boolean('Formula MRP Activated'),
        'fal_formula_parameter_categ1' : fields.float('Extra Length'),
        'fal_formula_parameter_categ2' : fields.float('Saw Thickness'),
    }
#end of product_category()

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'fal_formula_parameter0' : fields.float('DimA'),
        'fal_formula_parameter1' : fields.float('Extra Length'),
        'fal_formula_parameter2' : fields.float('Saw Thickness'),
    }
#end of product_product()