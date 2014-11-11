from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
        
    def _amount_balance_date(self, cr, uid, ids, name, args, context=None):
        """Function of the field residua. It computes the residual amount (balance) for each invoice"""
        if context is None:
            context = {}
        ctx = context.copy()
        result = {}
        currency_obj = self.pool.get('res.currency')
        for invoice in self.browse(cr, uid, ids, context=context):
            amount_paids = 0.00
            for payment in invoice.payment_ids:
                if context.get('wizard_data_date',False) and payment.date <= context.get('wizard_data_date',False):                    
                    amount_paid = 0.00
                    if invoice.type in ['out_invoice','in_refund']:
                        amount_paid = payment.credit
                    else:
                        amount_paid = payment.debit
                    if payment.currency_id and payment.currency_id.id == invoice.currency_id.id:
                        amount_paid = abs(payment.amount_currency)
                    else:
                        ctx['date'] = payment.date
                        amount_paid = currency_obj.compute(cr, uid, payment.company_id.currency_id.id, invoice.currency_id.id, amount_paid, context=ctx)
                    amount_paids += amount_paid
            #prevent the residual amount on the invoice to be less than 0
            result[invoice.id] = max(invoice.amount_total - amount_paids, 0.00)
        return result

    def _balance_date_search(self, cr, uid, obj, name, args, context=None):
        if context is None:
            context = {}
        ctx = context.copy()
        invoice_ids = self.search(cr, uid, [])
        currency_obj = self.pool.get('res.currency')
        temp = []
        for invoice in self.browse(cr, uid, invoice_ids, context=context):
            if invoice.state not in ['draft','cancel']:
                amount_paids = 0
                for payment in invoice.payment_ids:
                    if context.get('wizard_data_date',False) and payment.date <= context.get('wizard_data_date',False):                    
                        amount_paid = 0
                        if invoice.type in ['out_invoice','in_refund']:
                            amount_paid = payment.credit
                        else:
                            amount_paid = payment.debit
                        if payment.currency_id and payment.currency_id.id == invoice.currency_id.id:
                            amount_paid = abs(payment.amount_currency)
                        else:
                            ctx['date'] = payment.date
                            amount_paid = currency_obj.compute(cr, uid, payment.company_id.currency_id.id, invoice.currency_id.id, amount_paid, context=ctx)
                        amount_paids += amount_paid
                if max(invoice.amount_total - amount_paids, 0.0) > 0.00:
                    temp.append(invoice.id)
        return [('id', 'in', temp)]
        
    _columns = {
        'amount_balance_date': fields.function(_amount_balance_date, digits_compute=dp.get_precision('Account'), fnct_search=_balance_date_search, string='Balance on Date',
            store=False, help="The balance amount based on date.")
    }

#end of account_invoice()