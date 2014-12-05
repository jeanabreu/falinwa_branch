from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
        res = super(purchase_order, self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        res['is_delivery_fees'] = order_line.is_delivery_fees
        res['fal_manual_delivery_fee'] = order_line.fal_manual_delivery_fee
        return res

#end of purchase_order()

class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
        
    def _get_fapiao_unit_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        purchase_order_line = self.pool.get('purchase.order.line')
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for order_line_id in self.browse(cr, uid, ids, context=context):
            poline = purchase_order_line.read(cr, uid, order_line_id.id,['name'])
            if poline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = order_line_id.price_subtotal_vat
                subtotal_delivery_fee = 0.00
                unit_price = order_line_id.price_unit * (1-(order_line_id.discount or 0.0)/100.0)
                qty = order_line_id.product_qty
                tin = []
                manual = False
                for tax_id in order_line_id.taxes_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if order_line_id.order_id:
                    for order_line_id_in_order in order_line_id.order_id.order_line:
                        if order_line_id_in_order.is_delivery_fees:
                            subtotal_delivery_fee += order_line_id_in_order.price_subtotal_vat
                        total += order_line_id_in_order.price_subtotal_vat
                        if order_line_id_in_order.fal_manual_delivery_fee:
                            manual = True
                    if order_line_id.fal_manual_delivery_fee or manual:
                         if not order_line_id.is_delivery_fees :
                            if subtotal:
                                if tin:
                                    fapiao_unit_price = unit_price + order_line_id.fal_manual_delivery_fee / qty
                                else:
                                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, order_line_id.taxes_id, order_line_id.fal_manual_delivery_fee, 1, None, order_line_id.order_id.partner_id)
                                    cur_delivery_fee = order_line_id.order_id.pricelist_id.currency_id
                                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                                    fapiao_unit_price = order_line_id.price_subtotal_vat / qty + delivery_fee_with_vat / qty
                    else:
                        if not order_line_id.is_delivery_fees :
                            if subtotal:
                                if tin:
                                    fapiao_unit_price = unit_price + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                                else:
                                    fapiao_unit_price = order_line_id.price_subtotal_vat / qty + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                res[order_line_id.id] = fapiao_unit_price
        return res
        
    def _get_fapiao_sub_total(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        purchase_order_line = self.pool.get('purchase.order.line')
        if not ids:
            return res
        for order_line_id in self.browse(cr, uid, ids, context=context):
            polline = purchase_order_line.read(cr, uid, order_line_id.id,['name'])
            if polline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = order_line_id.price_subtotal
                subtotal_delivery_fee = 0.00
                unit_price = order_line_id.price_unit * (1-(order_line_id.discount or 0.0)/100.0)
                qty = order_line_id.product_qty
                manual = False
                if order_line_id.order_id:
                    for order_line_id_in_order in order_line_id.order_id.order_line:
                        if order_line_id_in_order.is_delivery_fees:
                            subtotal_delivery_fee += order_line_id_in_order.price_subtotal
                        total += order_line_id_in_order.price_subtotal
                        if order_line_id_in_order.fal_manual_delivery_fee:
                            manual = True
                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, order_line_id.taxes_id, order_line_id.fal_manual_delivery_fee, 1, None, order_line_id.order_id.partner_id)
                    cur_delivery_fee = order_line_id.order_id.pricelist_id.currency_id
                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                    if order_line_id.fal_manual_delivery_fee or manual:
                         if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = unit_price + order_line_id.fal_manual_delivery_fee / qty
                    else:
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = unit_price + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                totalex = fapiao_unit_price * qty
                tin = []
                for tax_id in order_line_id.taxes_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if tin :
                    if order_line_id.fal_manual_delivery_fee:
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = order_line_id.price_subtotal + order_line_id.fal_manual_delivery_fee
                    else:
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = order_line_id.price_subtotal + subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee)
                res[order_line_id.id] = totalex
        return res

    def _get_fapiao_sub_total_vat(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        purchase_order_line = self.pool.get('purchase.order.line')
        if not ids:
            return res
        for order_line_id in self.browse(cr, uid, ids, context=context):
            polline = purchase_order_line.read(cr, uid, order_line_id.id,['name'])
            if polline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = order_line_id.price_subtotal_vat
                subtotal_delivery_fee = 0.00
                unit_price = order_line_id.price_unit * (1-(order_line_id.discount or 0.0)/100.0)
                qty = order_line_id.product_qty
                manual = False
                if order_line_id.order_id:
                    for order_line_id_in_order in order_line_id.order_id.order_line:
                        if order_line_id_in_order.is_delivery_fees:
                            subtotal_delivery_fee += order_line_id_in_order.price_subtotal_vat
                        total += order_line_id_in_order.price_subtotal_vat
                        if order_line_id_in_order.fal_manual_delivery_fee:
                            manual = True
                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, order_line_id.taxes_id, order_line_id.fal_manual_delivery_fee, 1, None, order_line_id.order_id.partner_id)
                    cur_delivery_fee = order_line_id.order_id.pricelist_id.currency_id
                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                    if order_line_id.fal_manual_delivery_fee or manual:
                         if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = order_line_id.price_subtotal_vat / qty + delivery_fee_with_vat / qty
                    else: 
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = order_line_id.price_subtotal_vat / qty + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                totalex = fapiao_unit_price * qty
                tin = []
                for tax_id in order_line_id.taxes_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if tin :
                    if order_line_id.fal_manual_delivery_fee:
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = order_line_id.price_subtotal_vat + delivery_fee_with_vat
                    else:
                        if not order_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = order_line_id.price_subtotal_vat + subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee)
                res[order_line_id.id] = totalex
        return res
        
    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for order in self.pool.get('purchase.order').browse(cr, uid, ids, context=context):
            for line in order.order_line:
                result[line.id] = True
        return result.keys()
        
    _columns = {
        'fal_manual_delivery_fee' : fields.float('Delivery Fee',digits_compute=dp.get_precision('Account')),
        'is_delivery_fees' : fields.boolean('Is Delivery fees'),
        'fapiao_unit_price_vat' : fields.function(_get_fapiao_unit_price, type='float', string='Fapiao Unit Price',
            help="Fapiao Unit Price",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','fal_manual_delivery_fee','discount','price_unit','product_qty','taxes_id','order_id'], 20),
                'purchase.order' : (_get_order, ['order_line'], 20),
            },
            ),
        'fapiao_subtotal' : fields.function(_get_fapiao_sub_total, type='float', string='Fapiao Subtotal',
            help="Fapiao Subtotal",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','fal_manual_delivery_fee','discount','price_unit','product_qty','taxes_id','order_id'], 20),
                'purchase.order' : (_get_order, ['order_line'], 20),
            },
            ),
        'fapiao_subtotal_vat' : fields.function(_get_fapiao_sub_total_vat, type='float', string='Fapiao Subtotal VAT Included',
            help="Fapiao Subtotal Vat Included",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'purchase.order.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','fal_manual_delivery_fee','discount','price_unit','product_qty','taxes_id','order_id'], 20),
                'purchase.order' : (_get_order, ['order_line'], 20),
            },
            ),
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(purchase_order_line, self).create(cr, uid, vals, context=context)
        order_line_id = self.browse(cr, uid, res)
        manual = 0
        delivery_fee = 0
        total_manual_delivery_fee = 0.00
        for line in order_line_id.order_id.order_line:
            total_manual_delivery_fee += line.fal_manual_delivery_fee
            if line.fal_manual_delivery_fee:
                manual = 1
            if line.is_delivery_fees:
                delivery_fee = 1
                line_delivery_id = line.id
        if delivery_fee and manual:
            self.write(cr, uid, line_delivery_id, {'price_unit': total_manual_delivery_fee}, context=context) 
        return res
        
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        res = super(purchase_order_line, self).write(cr, uid, ids, vals, context=context)
        for order_line_id in self.browse(cr, uid, ids):
            manual = 0
            delivery_fee = 0
            total_manual_delivery_fee = 0.00
            for line in order_line_id.order_id.order_line:
                total_manual_delivery_fee += line.fal_manual_delivery_fee
                if line.fal_manual_delivery_fee:
                    manual = 1
                if line.is_delivery_fees:
                    delivery_fee = 1
                    line_delivery_id = line.id
            if delivery_fee and manual and not order_line_id.is_delivery_fees:
                self.write(cr, uid, line_delivery_id, {'price_unit': total_manual_delivery_fee}, context=context) 
        return res

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for order_line_id in self.browse(cr, uid, ids):
            manual = 0
            delivery_fee = 0
            total_manual_delivery_fee = 0.00
            for line in order_line_id.order_id.order_line:
                if order_line_id.id != line.id:
                    total_manual_delivery_fee += line.fal_manual_delivery_fee
                if line.fal_manual_delivery_fee:
                    manual = 1
                if line.is_delivery_fees:
                    delivery_fee = 1
                    line_delivery_id = line.id
            if delivery_fee and manual and not order_line_id.is_delivery_fees:
                self.write(cr, uid, line_delivery_id, {'price_unit': total_manual_delivery_fee}, context=context) 
        return super(purchase_order_line, self).unlink(cr, uid, ids, context=context)
        
#end of purchase_order_line()