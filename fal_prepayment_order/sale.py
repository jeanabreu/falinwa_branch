# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    _columns = {
        'fal_prepayment_voucher_ids' : fields.one2many('account.voucher', 'fal_sale_id', string='Prepayment Order', readonly=True)
    }

    def invoice_pay_preorder(self, cr, uid, ids, context=None):
        if not ids: return []
        dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'fal_prepayment_order', 'view_vendor_receipt_dialog_form_fal_prepayment_order')

        sale = self.browse(cr, uid, ids[0], context=context)
        return {
            'name':_("PrePayment Order"),
            'view_mode': 'form',
            'view_id': view_id,
            'view_type': 'form',
            'res_model': 'account.voucher',
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {
                'payment_expected_currency': sale.currency_id.id,
                'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(sale.partner_id).id,
                'default_amount': sale.amount_total,
                'default_reference': sale.name,
                'default_fal_sale_id': sale.id,
                'default_use_prepayment_account': True,
                'close_after_process': True,
                'invoice_type': False,
                'invoice_id': False,
                'default_type': 'receipt',
                'type': 'receipt',
            }
        }
        
#end of sale_order()