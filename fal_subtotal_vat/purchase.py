# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time


class purchase_order(orm.Model):
    _name = 'purchase.order'
    _inherit = 'purchase.order'
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
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
               discount = line.discount or 0.0
               new_price_unit = line.price_unit * (1 - discount / 100.0)
               for c in self.pool.get('account.tax').compute_all(cr, uid, line.taxes_id, new_price_unit, line.product_qty, line.product_id, order.partner_id)['taxes']:
                    val += c.get('amount', 0.0)
            res[order.id]['amount_tax']=cur_obj.round(cr, uid, cur, val)
            res[order.id]['amount_untaxed']=cur_obj.round(cr, uid, cur, val1)
            res[order.id]['amount_total']=res[order.id]['amount_untaxed'] + res[order.id]['amount_tax']
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('purchase.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
 
    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        res = super(purchase_order, self).create(cr, uid, vals, context=context)
        self.write(cr, uid, res, {'fal_refresh' : True}, context=context)
        return res
 
    _columns = {
        'amount_untaxed': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Untaxed Amount',
            store =
            {
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'fal_refresh'], 10),
                'purchase.order.line' : (_get_order, ['is_delivery_fees','discount','price_unit','product_qty','taxes_id','order_id'], 10),
            }, multi="sums", help="The amount without tax", track_visibility='onchange'),
        'amount_tax': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Taxes',
            store =
            {
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'fal_refresh'], 10),
                'purchase.order.line' : (_get_order, ['is_delivery_fees','discount','price_unit','product_qty','taxes_id','order_id'], 10),
            }, multi="sums", help="The tax amount"),
        'amount_total': fields.function(_amount_all, digits_compute= dp.get_precision('Account'), string='Total',
            store =
            {
                'purchase.order' : (lambda self, cr, uid, ids, c={}: ids, ['order_line', 'fal_refresh'], 10),
                'purchase.order.line' : (_get_order, ['is_delivery_fees','discount','price_unit','product_qty','taxes_id','order_id'], 10),
            }, multi="sums",help="The total amount"),
        'fal_refresh' : fields.boolean('refresh')
    }

class purchase_order_line(orm.Model):
    _name = 'purchase.order.line'
    _inherit = 'purchase.order.line'

    def create(self, cr, uid, vals, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        res = super(purchase_order_line, self).create(cr, uid, vals, context=context)
        purchase_id = purchase_obj.read(cr, uid, vals['order_id'], ['fal_refresh'], context=context)
        valpurchase = {} 
        if purchase_id['fal_refresh']:
            valpurchase['fal_refresh'] = False
        else:
            valpurchase['fal_refresh'] = True
        purchase_obj.write(cr, uid, vals['order_id'], valpurchase, context=context)
        return res

    def _amount_line(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            poline = self.read(cr, uid, line.id,['name'])
            if poline:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = tax_obj.compute_all(cr, uid, line.taxes_id, price, line.product_qty, line.product_id, line.order_id.partner_id)
                cur = line.order_id.pricelist_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, taxes['total'])
        return res
    
    def _amount_line_vat(self, cr, uid, ids, prop, arg, context=None):
        res = {}
        cur_obj=self.pool.get('res.currency')
        tax_obj = self.pool.get('account.tax')
        for line in self.browse(cr, uid, ids, context=context):
            poline = self.read(cr, uid, line.id,['name'])
            if poline:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = tax_obj.compute_all(cr, uid, line.taxes_id, price, line.product_qty, line.product_id, line.order_id.partner_id)
                cur = line.order_id.pricelist_id.currency_id
                res[line.id] = cur_obj.round(cr, uid, cur, taxes['total_included'])
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for order in self.pool.get('purchase.order').browse(cr, uid, ids, context=context):
            for line in order.order_line:
                result[line.id] = True
        return result.keys() 

    _columns = {
        'price_subtotal': fields.function(_amount_line,
            store=
            {
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','discount','price_unit','product_qty','taxes_id','order_id'], 20),
                'purchase.order' : (_get_order, ['order_line', 'fal_refresh'], 20),
            },
            string='Subtotal', digits_compute= dp.get_precision('Account')),
        'price_subtotal_vat': fields.function(_amount_line_vat, string='Subtotal with VAT',
            store=
            {
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','discount','price_unit','product_qty','taxes_id','order_id'], 20),
                'purchase.order' : (_get_order, ['order_line', 'fal_refresh'], 20),
            },
            digits_compute= dp.get_precision('Account')),
    }
    
#end of purchase_order_line()