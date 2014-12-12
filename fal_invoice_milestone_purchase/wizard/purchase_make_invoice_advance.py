from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class purchase_advance_payment_inv(orm.TransientModel):
    _name = "purchase.advance.payment.inv"
    _description = "Purchase Advance Payment Invoice"

    _columns = {
        'amount': fields.float('Advance Amount', digits_compute= dp.get_precision('Account'),
            help="The amount to be invoiced in advance."),
    }

    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        ir_property_obj = self.pool.get('ir.property')
        fiscal_obj = self.pool.get('account.fiscal.position')
        inv_line_obj = self.pool.get('account.invoice.line')
        account_jrnl_obj = self.pool.get('account.journal')
        wizard = self.browse(cr, uid, ids[0], context)
        purchase_ids = context.get('active_ids', [])

        result = []
        for purchase in purchase_obj.browse(cr, uid, purchase_ids, context=context):
            res = {}

            # determine and check expense account
            prop = ir_property_obj.get(cr, uid,
                        'property_account_expense_categ', 'product.category', context=context)
            prop_id = prop and prop.id or False
            account_id = fiscal_obj.map_account(cr, uid, purchase.fiscal_position or False, prop_id)
            if not account_id:
                raise orm.except_orm(_('Configuration Error!'),
                        _('There is no expense account defined as global property.'))
            res['account_id'] = account_id

            # determine invoice amount
            if wizard.amount <= 0.00:
                raise orm.except_orm(_('Incorrect Data'),
                    _('The value of Advance Amount must be positive.'))

            inv_amount = purchase.amount_total * wizard.amount / 100
            if not res.get('name'):
                res['name'] = _("Advance of %s %%") % (wizard.amount)

            # determine taxes
            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [(6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False
            
            #search journal
            journal_id = account_jrnl_obj.search(cr, uid, [('type', '=', 'purchase')], context=None)
            journal_id = journal_id and journal_id[0] or False
            
            # create the invoice
            inv_line_values = {
                'name': res.get('name'),
                'origin': purchase.name,
                'account_id': res['account_id'],
                'price_unit': inv_amount,
                'quantity': 1.0,
                'discount': False,
                'uos_id': res.get('uos_id', False),
                'product_id': False,
                'invoice_line_tax_id': res.get('invoice_line_tax_id'),
                'account_analytic_id': purchase.order_line[0].account_analytic_id.id or False,
            }
            inv_values = {
                'name': purchase.partner_ref or purchase.name or '',
                'origin': purchase.name,
                'type': 'in_invoice',
                'reference': purchase.partner_ref or purchase.name or '',
                'account_id': purchase.partner_id.property_account_payable.id,
                'partner_id': purchase.partner_id.id,
                'invoice_line': [(0, 0, inv_line_values)],
                'currency_id': purchase.pricelist_id.currency_id.id,
                'comment': purchase.notes or '',
                'payment_term': purchase.payment_term_id and purchase.payment_term_id.id or False,
                'fiscal_position': purchase.fiscal_position.id or purchase.partner_id.property_account_position.id or False,
                'journal_id' : journal_id,
                'date_invoice': context.get('date_invoice', False),
                'company_id': purchase.company_id and purchase.company_id.id or False,
            }
            result.append((purchase.id, inv_values))
        return result

    def _create_invoices(self, cr, uid, inv_values, purchase_id, context=None):
        inv_obj = self.pool.get('account.invoice')
        purchase_obj = self.pool.get('purchase.order')
        inv_id = inv_obj.create(cr, uid, inv_values, context=context)
        inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
        # add the invoice to the purchase order's invoices
        purchase_obj.write(cr, uid, purchase_id, {'invoice_ids': [(4, inv_id)]}, context=context)
        return inv_id


    def create_invoices(self, cr, uid, ids, context=None):
        """ create invoices for the active purchases orders """
        purchase_obj = self.pool.get('purchase.order')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        purchase_ids = context.get('active_ids', [])
        
        inv_ids = []        

        for purchase_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
            inv_ids.append(self._create_invoices(cr, uid, inv_values, purchase_id, context=context))

        if context.get('open_invoices', False):
            return self.open_invoices( cr, uid, ids, inv_ids, context=context)
        return {'type': 'ir.actions.act_window_close'}

    def open_invoices(self, cr, uid, ids, invoice_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'account', 'invoice_supplier_form')
        form_id = form_res and form_res[1] or False
        tree_res = ir_model_data.get_object_reference(cr, uid, 'account', 'invoice_tree')
        tree_id = tree_res and tree_res[1] or False

        return {
            'name': _('Advance Invoice'),
            'view_type': 'form',
            'view_mode': 'form,tree',
            'res_model': 'account.invoice',
            'res_id': invoice_ids[0],
            'view_id': False,
            'views': [(form_id, 'form'), (tree_id, 'tree')],
            'context': "{'type': 'in_invoice'}",
            'type': 'ir.actions.act_window',
        }

#end of purchase_advance_payment_inv()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
