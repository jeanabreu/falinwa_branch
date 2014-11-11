from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time

class fsale_advance_payment_inv(orm.TransientModel):
    _name = "fsale.advance.payment.inv"
    _description = "Sale Advance Payment Invoice"

    _columns = {
        'amount_temp': fields.float('Advance Amount', digits_compute= dp.get_precision('Account'),
            help="The amount to be invoiced in advance.",readonly=True),
        'amount': fields.float('Advance Amount', digits_compute= dp.get_precision('Account'),
            help="The amount to be invoiced in advance."),
        'is_final' : fields.boolean('Final Invoice'),
        'invoice_milestone_rule_line_id' : fields.many2one('fal.rule.lines','Invoice Milestone Line ID'),
    }

    def _get_amount(self, cr, uid, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        invoice_milestone_rule_line_obj = self.pool.get('fal.rule.lines')
        res = 0.00
        dict = {}
        if context.get('active_id',False):
            sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
            if sale_id.invoice_milestone_rule_id:
                temp_invoice_milestone_rule_id = []
                for rule_line in sale_id.invoice_milestone_rule_line_ids:
                    temp_invoice_milestone_rule_id.append(rule_line.id)
                rule_id = invoice_milestone_rule_line_obj.search(cr , uid, [('id','in',temp_invoice_milestone_rule_id)], order='sequence', context=context)
                if rule_id:
                    res = invoice_milestone_rule_line_obj.browse(cr, uid, rule_id[0]).percentage
        return res
        
    def _get_is_final(self, cr, uid, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        res = False
        if context.get('active_id',False):
            sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
            if len(sale_id.invoice_milestone_rule_line_ids) == 1:
                res = True    
        return res
        
    def _get_invoice_milestone_rule_line_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        invoice_milestone_rule_line_obj = self.pool.get('fal.rule.lines')
        res = False
        if context.get('active_id',False):
            sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
            if sale_id.invoice_milestone_rule_id:
                temp_invoice_milestone_rule_id = []
                for rule_line in sale_id.invoice_milestone_rule_line_ids:
                    temp_invoice_milestone_rule_id.append(rule_line.id)
                rule_id = invoice_milestone_rule_line_obj.search(cr , uid, [('id','in',temp_invoice_milestone_rule_id)], order='sequence', context=context)
                if rule_id:
                    res = rule_id[0]
        return res
    
    _defaults = {
        'amount': _get_amount,
        'amount_temp': _get_amount,
        'is_final' : _get_is_final,
        'invoice_milestone_rule_line_id' : _get_invoice_milestone_rule_line_id
    }
    
    def _prepare_advance_invoice_vals(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        ir_property_obj = self.pool.get('ir.property')
        fiscal_obj = self.pool.get('account.fiscal.position')
        inv_line_obj = self.pool.get('account.invoice.line')
        account_jrnl_obj = self.pool.get('account.journal')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])

        result = []
        for sale in sale_obj.browse(cr, uid, sale_ids, context=context):
            res = {}

            # determine and check expense account
            prop = ir_property_obj.get(cr, uid,
                        'property_account_income_categ', 'product.category', context=context)
            prop_id = prop and prop.id or False
            account_id = fiscal_obj.map_account(cr, uid, sale.fiscal_position or False, prop_id)
            if not account_id:
                raise osv.except_osv(_('Configuration Error!'),
                        _('There is no expense account defined as global property.'))
            res['account_id'] = account_id

            # determine invoice amount
            if wizard.amount <= 0.00:
                raise osv.except_osv(_('Incorrect Data'),
                    _('The value of Advance Amount must be positive.'))

            inv_amount = sale.amount_untaxed * wizard.amount / 100
            if not res.get('name', False):
                res['name'] = wizard.invoice_milestone_rule_line_id.description

            # determine taxes
            temp_tax = []
            for tax in sale.order_line[0].tax_id:
                temp_tax.append(tax.id)
            if sale.order_line[0].tax_id and sale.order_line[0].tax_id[0].price_include:
                inv_amount = sale.amount_total * wizard.amount / 100
            res['invoice_line_tax_id'] = temp_tax
            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [(6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False
            
            #search journal
            journal_id = self.pool.get('account.journal').search(cr, uid,
                [('type', '=', 'sale'), ('company_id', '=', sale.company_id.id)],
                limit=1)
            journal_id = journal_id and journal_id[0] or False
            
            # create the invoice
            inv_line_values = {
                'name': res.get('name'),
                'origin': sale.name,
                'account_id': res['account_id'],
                'price_unit': inv_amount,
                'quantity': 1.0,
                'discount': False,
                'uos_id': res.get('uos_id', False),
                'product_id': False,
                'invoice_line_tax_id': res.get('invoice_line_tax_id'),
                'account_analytic_id': sale.project_id.id or False,
            }
            inv_values = {
                'name': sale.client_order_ref or sale.name or '',
                'origin': sale.name,
                'type': 'out_invoice',
                'reference': sale.client_order_ref or sale.name or '',
                'account_id': sale.partner_id.property_account_receivable.id,
                'partner_id': sale.partner_id.id,
                'invoice_line': [(0, 0, inv_line_values)],
                'currency_id': sale.pricelist_id.currency_id.id,
                'comment': sale.note or '',
                'payment_term': wizard.invoice_milestone_rule_line_id.payment_term and  wizard.invoice_milestone_rule_line_id.payment_term.id or sale.payment_term and sale.payment_term.id or False,
                'fiscal_position': sale.fiscal_position.id or sale.partner_id.property_account_position.id or False,
                'journal_id' : journal_id,
                'date_invoice': context.get('date_invoice', False),
                'company_id': sale.company_id.id,
                'user_id': sale.user_id and sale.user_id.id or False,
                'final_quotation_number' : sale.x_quotationversioning,
            }
            result.append((sale.id, inv_values))
        return result

    def _create_invoices(self, cr, uid, inv_values, sale_id, context=None):
        inv_obj = self.pool.get('account.invoice')
        sale_obj = self.pool.get('sale.order')
        inv_id = inv_obj.create(cr, uid, inv_values, context=context)
        inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
        res = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv_values['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
        # add the invoice to the sale order's invoices
        sale_obj.write(cr, uid, sale_id, {
            'invoice_ids' : [(4, inv_id)],
        }, context=context)
        inv_obj.write(cr, uid, [inv_id], res['value'], context=context)
        return inv_id


    def create_invoices(self, cr, uid, ids, context=None):
        """ create invoices for the active sale orders """
        sale_obj = self.pool.get('sale.order')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        sale_ids = context.get('active_ids', [])

        sale_obj.write(cr, uid, sale_ids[0], {
            'invoice_milestone_rule_line_ids' : [(3, wizard.invoice_milestone_rule_line_id.id)],
        }, context=context)
        
        inv_ids = []
        if wizard.is_final:
            # create the final invoices of the active sales orders
            context['wizard_payment_term'] = wizard.invoice_milestone_rule_line_id.payment_term and  wizard.invoice_milestone_rule_line_id.payment_term.id
            res = sale_obj.manual_invoice(cr, uid, sale_ids, context)
            if context.get('open_invoices', False):
                return res
            return {'type': 'ir.actions.act_window_close'}
        else:    
            for sale_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
                inv_ids.append(self._create_invoices(cr, uid, inv_values, sale_id, context=context))
        
        if context.get('open_invoices', False):
            return self.open_invoices( cr, uid, ids, inv_ids, context=context)
        return {'type': 'ir.actions.act_window_close'}

    def open_invoices(self, cr, uid, ids, invoice_ids, context=None):
        """ open a view on one of the given invoice_ids """
        ir_model_data = self.pool.get('ir.model.data')
        form_res = ir_model_data.get_object_reference(cr, uid, 'account', 'invoice_form')
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
            'context': "{'type': 'out_invoice'}",
            'type': 'ir.actions.act_window',
        }

#end of fsale_advance_payment_inv()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
