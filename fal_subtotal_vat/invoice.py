# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice_line(orm.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
        
    def _amount_line_vat(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}
        cur = False
        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            poline = self.read(cr, uid, line.id,['name'])
            if poline:
                price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
                taxes = tax_obj.compute_all(cr, uid, line.invoice_line_tax_id, price, line.quantity, line.product_id, line.invoice_id.partner_id)
                res[line.id] = taxes['total_included']
                if line.invoice_id:
                    cur = line.invoice_id.currency_id
                    res[line.id] = cur_obj.round(cr, uid, cur, res[line.id])
        return res

    def _get_invoice(self, cr, uid, ids, context=None):
        result = {}
        for invoice in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):
            for line in invoice.invoice_line:
                result[line.id] = True
        return result.keys()
        
    _columns = {
        'price_subtotal_vat': fields.function(_amount_line_vat,
            store=
            {
                'account.invoice.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','discount','quantity','invoice_line_tax_id','discount','invoice_id'], 20),
                'account.invoice' : (_get_invoice, ['invoice_line'], 20),
            },
            string='Subtotal with VAT', digits_compute= dp.get_precision('Account')),
    }
    
#end of account_invoice_line()