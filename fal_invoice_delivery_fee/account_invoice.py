from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import netsvc

class account_invoice_line(orm.Model):
    _name = "account.invoice.line"
    _inherit = "account.invoice.line"
        
    def _get_fapiao_unit_price(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        if not ids:
            return res
        account_invoice_line = self.pool.get('account.invoice.line')
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        for invoice_line_id in self.browse(cr, uid, ids, context=context):
            acline = account_invoice_line.read(cr, uid, invoice_line_id.id,['name'])
            if acline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = invoice_line_id.price_subtotal_vat
                subtotal_delivery_fee = 0.00
                unit_price = invoice_line_id.price_unit * (1-(invoice_line_id.discount or 0.0)/100.0)
                qty = invoice_line_id.quantity
                tin = []
                manual = False
                for tax_id in invoice_line_id.invoice_line_tax_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if invoice_line_id.invoice_id:
                    for invoice_lie_id_in_invoice in invoice_line_id.invoice_id.invoice_line:
                        if invoice_lie_id_in_invoice.is_delivery_fees:
                            subtotal_delivery_fee += invoice_lie_id_in_invoice.price_subtotal_vat
                        total += invoice_lie_id_in_invoice.price_subtotal_vat
                        if invoice_lie_id_in_invoice.fal_manual_delivery_fee:
                            manual = True
                    if invoice_line_id.fal_manual_delivery_fee or manual:
                         if not invoice_line_id.is_delivery_fees :
                            if subtotal:
                                if tin:
                                    fapiao_unit_price = unit_price + invoice_line_id.fal_manual_delivery_fee / qty
                                else:
                                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, invoice_line_id.invoice_line_tax_id, invoice_line_id.fal_manual_delivery_fee, 1, None, invoice_line_id.invoice_id.partner_id)
                                    cur_delivery_fee = invoice_line_id.invoice_id.currency_id
                                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                                    fapiao_unit_price = invoice_line_id.price_subtotal_vat / qty + delivery_fee_with_vat / qty
                    else:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal:                            
                                if tin:
                                    fapiao_unit_price = unit_price + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                                else:
                                    fapiao_unit_price = invoice_line_id.price_subtotal_vat / qty + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                res[invoice_line_id.id] = fapiao_unit_price
        return res
        
    def _get_fapiao_sub_total(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        account_invoice_line = self.pool.get('account.invoice.line')
        if not ids:
            return res
        for invoice_line_id in self.browse(cr, uid, ids, context=context):
            acline = account_invoice_line.read(cr, uid, invoice_line_id.id,['name'])
            if acline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = invoice_line_id.price_subtotal
                subtotal_delivery_fee = 0.00
                unit_price = invoice_line_id.price_unit * (1-(invoice_line_id.discount or 0.0)/100.0)
                qty = invoice_line_id.quantity
                manual = False
                if invoice_line_id.invoice_id:
                    for invoice_lie_id_in_invoice in invoice_line_id.invoice_id.invoice_line:
                        if invoice_lie_id_in_invoice.is_delivery_fees:
                            subtotal_delivery_fee += invoice_lie_id_in_invoice.price_subtotal
                        total += invoice_lie_id_in_invoice.price_subtotal
                        if invoice_lie_id_in_invoice.fal_manual_delivery_fee:
                            manual = True
                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, invoice_line_id.invoice_line_tax_id, invoice_line_id.fal_manual_delivery_fee, 1, None, invoice_line_id.invoice_id.partner_id)
                    cur_delivery_fee = invoice_line_id.invoice_id.currency_id
                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                    if invoice_line_id.fal_manual_delivery_fee or manual:
                         if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = unit_price + invoice_line_id.fal_manual_delivery_fee / qty
                    else:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = unit_price + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                totalex = fapiao_unit_price * qty
                tin = []
                for tax_id in invoice_line_id.invoice_line_tax_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if tin :
                    if invoice_line_id.fal_manual_delivery_fee:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = invoice_line_id.price_subtotal + invoice_line_id.fal_manual_delivery_fee
                    else:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = invoice_line_id.price_subtotal + subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee)
                res[invoice_line_id.id] = totalex
        return res
        
    def _get_fapiao_sub_total_vat(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        account_invoice_line = self.pool.get('account.invoice.line')
        if not ids:
            return res
        for invoice_line_id in self.browse(cr, uid, ids, context=context):
            acline = account_invoice_line.read(cr, uid, invoice_line_id.id,['name'])
            if acline:
                fapiao_unit_price = 0.00
                total = 0.00
                subtotal = invoice_line_id.price_subtotal_vat
                subtotal_delivery_fee = 0.00
                unit_price = invoice_line_id.price_unit * (1-(invoice_line_id.discount or 0.0)/100.0)
                qty = invoice_line_id.quantity
                manual = False
                if invoice_line_id.invoice_id:
                    for invoice_lie_id_in_invoice in invoice_line_id.invoice_id.invoice_line:
                        if invoice_lie_id_in_invoice.is_delivery_fees:
                            subtotal_delivery_fee += invoice_lie_id_in_invoice.price_subtotal_vat
                        total += invoice_lie_id_in_invoice.price_subtotal_vat
                        if invoice_lie_id_in_invoice.fal_manual_delivery_fee:
                            manual = True
                    taxes_delivery_fee = tax_obj.compute_all(cr, uid, invoice_line_id.invoice_line_tax_id, invoice_line_id.fal_manual_delivery_fee, 1, None, invoice_line_id.invoice_id.partner_id)
                    cur_delivery_fee = invoice_line_id.invoice_id.currency_id
                    delivery_fee_with_vat = cur_obj.round(cr, uid, cur_delivery_fee, taxes_delivery_fee['total_included'])
                    if invoice_line_id.fal_manual_delivery_fee or manual:
                         if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = invoice_line_id.price_subtotal_vat / qty + delivery_fee_with_vat / qty
                    else: 
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                fapiao_unit_price = invoice_line_id.price_subtotal_vat / qty + (subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee) / qty)
                else:
                    fapiao_unit_price = unit_price
                totalex = fapiao_unit_price * qty
                tin = []
                for tax_id in invoice_line_id.invoice_line_tax_id:
                    if tax_id.price_include:
                        tin.append(tax_id)
                if tin :
                    if invoice_line_id.fal_manual_delivery_fee:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = invoice_line_id.price_subtotal_vat + delivery_fee_with_vat
                    else:
                        if not invoice_line_id.is_delivery_fees :
                            if subtotal and total:
                                totalex = invoice_line_id.price_subtotal_vat + subtotal_delivery_fee * subtotal / (total - subtotal_delivery_fee)
                res[invoice_line_id.id] = totalex
        return res

    def _get_invoice(self, cr, uid, ids, context=None):
        result = {}
        for invoice in self.pool.get('account.invoice').browse(cr, uid, ids, context=context):
            for line in invoice.invoice_line:
                result[line.id] = True
        return result.keys()
        
    _columns = {
        'fal_manual_delivery_fee' : fields.float('Delivery Fee',digits_compute=dp.get_precision('Account')),
        'is_delivery_fees' : fields.boolean('Is Delivery fees'),
        'fapiao_unit_price_vat' : fields.function(_get_fapiao_unit_price, type='float', string='Fapiao Unit Price VAT Included',
            help="Fapiao Unit Price",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'account.invoice.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','quantity','invoice_line_tax_id','discount','invoice_id'], 20),
                'account.invoice' : (_get_invoice, ['invoice_line'], 20),
            },
            ),
        'fapiao_subtotal' : fields.function(_get_fapiao_sub_total, type='float', string='Fapiao Subtotal',
            help="Fapiao Subtotal",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'account.invoice.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','quantity','invoice_line_tax_id','discount','invoice_id'], 20),
                'account.invoice' : (_get_invoice, ['invoice_line'], 20),
            },
            ),
        'fapiao_subtotal_vat' : fields.function(_get_fapiao_sub_total_vat, type='float', string='Fapiao Subtotal VAT Included',
            help="Fapiao Subtotal VAT Included",
            digits_compute=dp.get_precision('Account'),
            store=
            {
                'account.invoice.line' : (lambda self, cr, uid, ids, c={}: ids, ['is_delivery_fees','price_unit','quantity','invoice_line_tax_id','discount','invoice_id'], 20),
                'account.invoice' : (_get_invoice, ['invoice_line'], 20),
            },
            ),
    }

    def invoice_print(self, cr, uid, ids, context=None):
        '''
        This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
        '''
        assert len(ids) == 1, 'This option should only be used for a single id at a time.'
        self.write(cr, uid, ids, {'sent': True}, context=context)
        datas = {
             'ids': ids,
             'model': 'account.invoice',
             'form': self.read(cr, uid, ids[0], context=context)
        }
        return {
            'type': 'ir.actions.report.xml',
            'report_name': 'account.invoice.fal',
            'datas': datas,
            'nodestroy' : True
        }
        
    def create(self, cr, uid, vals, context=None):
        res = super(account_invoice_line, self).create(cr, uid, vals, context=context)
        invoice_line_id = self.browse(cr, uid, res)
        manual = 0
        delivery_fee = 0
        total_manual_delivery_fee = 0.00
        if invoice_line_id.invoice_id:
            for line in invoice_line_id.invoice_id.invoice_line:
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
        res = super(account_invoice_line, self).write(cr, uid, ids, vals, context=context)
        for invoice_line_id in self.browse(cr, uid, ids):
            manual = 0
            delivery_fee = 0
            total_manual_delivery_fee = 0.00
            for line in invoice_line_id.invoice_id.invoice_line:
                total_manual_delivery_fee += line.fal_manual_delivery_fee
                if line.fal_manual_delivery_fee:
                    manual = 1
                if line.is_delivery_fees:
                    delivery_fee = 1
                    line_delivery_id = line.id
            if delivery_fee and manual and not invoice_line_id.is_delivery_fees:
                self.write(cr, uid, line_delivery_id, {'price_unit': total_manual_delivery_fee}, context=context) 
        return res

    def unlink(self, cr, uid, ids, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        for invoice_line_id in self.browse(cr, uid, ids):
            manual = 0
            delivery_fee = 0
            total_manual_delivery_fee = 0.00
            for line in invoice_line_id.invoice_id.invoice_line:
                if invoice_line_id.id != line.id:
                    total_manual_delivery_fee += line.fal_manual_delivery_fee
                if line.fal_manual_delivery_fee:
                    manual = 1
                if line.is_delivery_fees:
                    delivery_fee = 1
                    line_delivery_id = line.id
            if delivery_fee and manual and not invoice_line_id.is_delivery_fees:
                self.write(cr, uid, line_delivery_id, {'price_unit': total_manual_delivery_fee}, context=context) 
        return super(account_invoice_line, self).unlink(cr, uid, ids, context=context)
        
#end of account_invoice_line()