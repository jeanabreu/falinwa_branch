# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                'amount_untaxed': 0.0,
                'amount_tax': 0.0,
                'amount_total': 0.0,
            }
            val = val1 = 0.0
            cur = order.pricelist_id.currency_id
            for line in order.order_line:
                val1 += line.price_subtotal
                val += self._amount_line_tax(cr, uid, line, context=context)
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed'] = cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res
    
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        if context is None:
            context = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
        
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        res = super(sale_order, self).create(cr, uid, vals, context=context)
        self.write(cr, uid, res, {'fal_refresh' : True}, context=context)
        return res
        
    _columns = {        
        'amount_untaxed': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Untaxed Amount',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','fal_refresh'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax.", track_visibility='always'),
        'amount_tax': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Taxes',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','fal_refresh'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all, digits_compute=dp.get_precision('Account'), string='Total',
            store={
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line','fal_refresh'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The total amount."),
        'fal_refresh' : fields.boolean('refresh')
    }
#end of sale_order()

class sale_order_line(orm.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        res = super(sale_order_line, self).create(cr, uid, vals, context=context)
        sale_id = sale_obj.read(cr, uid, vals['order_id'], ['fal_refresh'], context=context)
        valsale = {} 
        if sale_id['fal_refresh']:
            valsale['fal_refresh'] = False
        else:
            valsale['fal_refresh'] = True
        sale_obj.write(cr, uid, vals['order_id'], valsale, context=context)
        return res
        
    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            poline = self.read(cr, uid, line.id,['name'])
            if poline:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
                cur = line.order_id.pricelist_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res

    def _amount_line_vat(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            poline = self.read(cr, uid, line.id,['name'])
            if poline:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = tax_obj.compute_all(cr, uid, line.tax_id, price, line.product_uom_qty, line.product_id, line.order_id.partner_id)
                cur = line.order_id.pricelist_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for order in self.pool.get('sale.order').browse(cr, uid, ids, context=context):
            for line in order.order_line:
                result[line.id] = True
        return result.keys()
                
    _columns = {
        'price_subtotal': fields.function(_amount_line, string='Subtotal',
            store=
            {
                'sale.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','discount','product_uom_qty','tax_id','order_id','refresh'], 20),
                'sale.order' : (_get_order, ['order_line','fal_refresh'], 20),
            },
            digits_compute= dp.get_precision('Account')),
        'price_subtotal_vat': fields.function(_amount_line_vat, string='Subtotal with VAT',
            store=
            {
                'sale.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','discount','product_uom_qty','tax_id','order_id','refresh'], 20),
                'sale.order' : (_get_order, ['order_line','fal_refresh'], 20),
            },
            digits_compute= dp.get_precision('Account')),
    }
    
#end of sale_order_line()