# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class stock_picking(orm.Model):
    _name = "stock.picking"
    _inherit = "stock.picking"
    
    _columns = {
        'purchase_id' : fields.many2one('purchase.order', 'Purchase Order',
            ondelete='set null', select=True),
        'fal_project_id_in': fields.related('purchase_id', 'sale_order_line_order_id', 'project_id', 'code', type='char', string="Project Number from Sale Order", readonly=True),
        'fal_project_number': fields.char('Project Number from Purchase Order',size=526),
        'sale_id' : fields.many2one('sale.order', 'Sales Order', ondelete='set null', select=True),
        'fal_project_id_out': fields.related('sale_id', 'project_id', 'code', type='char', string='Project Number from Sale Order', readonly=True),
    }
#end of stock_picking()