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
                if product_id.sale_currency_id and product_id.net_currency_id:
                    sale_price_currency = product_id.sale_currency_id.id
                    user = user_obj.browse(cr, uid, uid)
                    net_price_currency = product_id.net_currency_id.id
                    company_currency = product_id.company_id.currency_id.id or user.company_id.currency_id.id
                    ctx.update({'date': time.strftime('%Y-%m-%d')})
                    sale_price_in_net_currency = cur_obj.compute(cr, uid, sale_price_currency, net_price_currency, product_id.list_price, context=ctx)
                    bomcost_price_in_net_currency = cur_obj.compute(cr, uid, company_currency, net_price_currency, product_id.fal_bom_costs, context=ctx)
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
        
    _columns = {
        'sale_currency_id' : fields.many2one('res.currency', 'Sale Currency', help="Select a Sale Currency"),
        'cost_currency_id' : fields.many2one('res.currency', 'Cost Currency', help="Select a Cost Currency"),
        'net_currency_id' : fields.many2one('res.currency', 'Net Margin Currency', help="Select a Net Margin Currency"),
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