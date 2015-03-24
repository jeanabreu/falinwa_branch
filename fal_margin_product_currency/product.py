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
        cur_obj = self.pool.get('res.currency')
        user_obj = self.pool.get('res.users')
        ctx = context.copy()
        for product_id in self.browse(cr, uid, ids, context=context):
            if product_id.bom_ids :
                if product_id.sale_currency_id and product_id.bom_cost_currency_id and product_id.net_currency_id:
                    sale_price_currency = product_id.sale_currency_id.id
                    bomcost_price_currency = product_id.bom_cost_currency_id.id
                    user = user_obj.browse(cr, uid, uid)
                    net_price_currency = product_id.net_currency_id.id
                    company_currency = product_id.company_id.currency_id.id or user.company_id.currency_id.id
                    ctx.update({'date': time.strftime('%Y-%m-%d')})
                    sale_price_in_net_currency = cur_obj.compute(cr, uid, sale_price_currency, net_price_currency, product_id.list_price, context=ctx)
                    bomcost_price_in_net_currency = cur_obj.compute(cr, uid, bomcost_price_currency, net_price_currency, product_id.fal_bom_costs, context=ctx)
                    margin = sale_price_in_net_currency - bomcost_price_in_net_currency
                else:
                    margin = product_id.list_price - product_id.fal_bom_costs
            else:
                if product_id.sale_currency_id and product_id.cost_currency_id and product_id.net_currency_id:
                    sale_price_currency = product_id.sale_currency_id.id
                    standard_price_currency = product_id.cost_currency_id.id
                    net_price_currency = product_id.net_currency_id.id
                    ctx.update({'date': time.strftime('%Y-%m-%d')})
                    sale_price_in_net_currency = cur_obj.compute(cr, uid, sale_price_currency, net_price_currency, product_id.list_price, context=ctx)
                    cost_price_in_net_currency = cur_obj.compute(cr, uid, standard_price_currency, net_price_currency, product_id.standard_price, context=ctx)
                    margin = sale_price_in_net_currency - cost_price_in_net_currency
                else:
                    margin = product_id.list_price - product_id.standard_price
            res[product_id.id] = margin
        return res
    
    def _get_bom(self, cr, uid, ids, context=None):
        result = {}
        for bom in self.pool.get('mrp.bom').browse(cr, uid, ids, context=context):
            result[bom.product_id.id] = True
        return result.keys()
   
    def get_cost(self, cr, uid, product_id, context=None):
        cost_of_bom = 0.00
        if not product_id:
            return cost_of_bom
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        ctx = context.copy()
        cur_obj = self.pool.get('res.currency')
        if product_id.bom_ids :
            bom_id = bom_obj.browse(cr, uid, product_id.bom_ids[0].id, context=context)
            for bom_line in bom_id.bom_line_ids:
                pro_qty = bom_line.product_qty
                if bom_line.product_uom.id != bom_line.product_uom.id:
                    pro_qty = uom_obj._compute_qty(cr, uid, bom_line.product_uom.id, bom_line.product_qty, bom_line.product_uom.id)
                if bom_line.product_id.bom_ids:
                    cost_of_bom += pro_qty * self.get_cost(cr, uid, bom_line.product_id,  context=context) 
                else:
                    if bom_line.product_id.cost_currency_id and product_id.bom_cost_currency_id:
                        if bom_line.product_id.cost_currency_id.id != product_id.bom_cost_currency_id.id:
                            cost_of_bom += pro_qty * cur_obj.compute(cr, uid, bom_line.product_id.cost_currency_id.id, product_id.bom_cost_currency_id.id, bom_line.product_id.standard_price, context=ctx)
                    else:
                        cost_of_bom += pro_qty * bom_line.product_id.standard_price
        else:
            if product_id.cost_currency_id and product_id.bom_cost_currency_id:
                if product_id.cost_currency_id.id != product_id.bom_cost_currency_id.id:
                    cost_of_bom = cur_obj.compute(cr, uid, product_id.cost_currency_id.id, product_id.bom_cost_currency_id.id, product_id.standard_price, context=ctx)
            else:
                cost_of_bom = product_id.standard_price
        return cost_of_bom
       
    def _get_cost_bom(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        for product_id in self.browse(cr, uid, ids, context=context):
            cost_of_bom = self.get_cost(cr, uid, product_id,  context=context) 
            res[product_id.id] = cost_of_bom
        return res
        
    _columns = {
        'sale_currency_id' : fields.property(
            type='many2one',
            relation='res.currency',
            string="Sale Currency",
            view_load=True,
            help="Select a Sale Currency"
            ),
        'cost_currency_id' : fields.property(
            type='many2one',
            relation='res.currency',
            string="Cost Currency",
            view_load=True,
            help="Select a Cost Currency"
            ),
        'net_currency_id' : fields.property(
            type='many2one',
            relation='res.currency',
            string="Net Margin Currency",
            view_load=True,
            help="Select a Net Margin Currency"
            ),
        'fal_net_margin' : fields.function(_get_net_margin, type='float', string='Net Margin',
            help="Net Margin",
            digits_compute=dp.get_precision('Account'),
            store=False
            ),
        'bom_cost_currency_id' : fields.property(
            type='many2one',
            relation='res.currency',
            string="BoM Cost Currency",
            view_load=True,
            help="Select a BoM Cost Currency"
            ),            
        'fal_bom_costs' : fields.function(_get_cost_bom, type='float', string='Cost of BoM',
            help="Cost of Raw Material",
            digits_compute=dp.get_precision('BoM Cost'),
            store=False
            ),
    }

#end of product_product()