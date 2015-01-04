# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    def _get_default_project(self, cr, uid, context=None):
        project_id = False
        if context.get('partner', False):            
            partner_id = self.pool.get('res.partner').browse(cr, uid, context['partner'], context)
            project_id = partner_id.fal_project_id.id
        return project_id
        
    _defaults = {
        'account_analytic_id' : _get_default_project,
    }
    
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, state='draft', context=None):
        
        if context is None:
            context = {}       
        
        res = super(purchase_order_line, self).onchange_product_id(cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=date_order, fiscal_position_id=fiscal_position_id, date_planned=date_planned,
            name=name, price_unit=price_unit, state=state, context=context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr ,uid, partner_id, context)
            if partner.fal_project_id:
                return res
        if product_id:
            product = self.pool.get('product.product').browse(cr ,uid, product_id, context)
            res['value']['account_analytic_id'] = product.project_id.id
        return res


#end of purchase_order_line()