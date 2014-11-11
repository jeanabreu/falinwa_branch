from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
import time

class purchase_advance_payment_inv(orm.TransientModel):
    _name = "purchase.advance.payment.inv"
    _inherit = "purchase.advance.payment.inv"

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
        purchase_obj = self.pool.get('purchase.order')
        invoice_milestone_rule_line_obj = self.pool.get('fal.rule.lines')
        res = 0.00
        dict = {}
        if context.get('active_id',False):
            purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
            if purchase_id.invoice_milestone_rule_id:
                temp_invoice_milestone_rule_id = []
                for rule_line in purchase_id.invoice_milestone_rule_line_ids:
                    temp_invoice_milestone_rule_id.append(rule_line.id)
                rule_id = invoice_milestone_rule_line_obj.search(cr , uid, [('id','in',temp_invoice_milestone_rule_id)], order='sequence', context=context)
                if rule_id:
                    res = invoice_milestone_rule_line_obj.browse(cr, uid, rule_id[0]).percentage
        return res
        
    def _get_is_final(self, cr, uid, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        res = False
        if context.get('active_id',False):
            purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
            if len(purchase_id.invoice_milestone_rule_line_ids) == 1:
                res = True    
        return res
        
    def _get_invoice_milestone_rule_line_id(self, cr, uid, context=None):
        if context is None:
            context = {}
        purchase_obj = self.pool.get('purchase.order')
        invoice_milestone_rule_line_obj = self.pool.get('fal.rule.lines')
        res = False
        if context.get('active_id',False):
            purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
            if purchase_id.invoice_milestone_rule_id:
                temp_invoice_milestone_rule_id = []
                for rule_line in purchase_id.invoice_milestone_rule_line_ids:
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
                raise osv.except_osv(_('Configuration Error!'),
                        _('There is no expense account defined as global property.'))
            res['account_id'] = account_id

            # determine invoice amount
            if wizard.amount <= 0.00:
                raise osv.except_osv(_('Incorrect Data'),
                    _('The value of Advance Amount must be positive.'))

            inv_amount = purchase.amount_untaxed * wizard.amount / 100
            if not res.get('name'):
                res['name'] = wizard.invoice_milestone_rule_line_id.description

            # determine taxes
            temp_tax = []
            for tax in purchase.order_line[0].taxes_id:
                temp_tax.append(tax.id)
            if purchase.order_line[0].taxes_id and purchase.order_line[0].taxes_id[0].price_include:
                inv_amount = purchase.amount_total * wizard.amount / 100
            res['invoice_line_tax_id'] = temp_tax
            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [(6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False
            
            #search journal
            journal_id = self.pool.get('account.journal').search(cr, uid,
                [('type', '=', 'purchase'), ('company_id', '=', purchase.company_id.id)],
                limit=1)
            journal_id = journal_id and journal_id[0] or False
            
            # create the invoice
            inv_line_values = {
                'name': res.get('name'),
                'origin': purchase.name,
                'account_id': res['account_id'],
                'price_unit': inv_amount,
                'quantity': 1.0,
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
                'payment_term': wizard.invoice_milestone_rule_line_id.payment_term and wizard.invoice_milestone_rule_line_id.payment_term.id or purchase.payment_term_id and purchase.payment_term_id.id or False,
                'fiscal_position': purchase.fiscal_position.id or purchase.partner_id.property_account_position.id or False,
                'journal_id' : journal_id,
                'date_invoice': context.get('date_invoice', False),
                'company_id': purchase.company_id and purchase.company_id.id or False,
            }
            result.append((purchase.id, inv_values))
        return result

    def _create_invoices(self, cr, uid, inv_values, purchase_id, context=None):
        inv_obj = self.pool.get('account.invoice')
        result = super(purchase_advance_payment_inv, self)._create_invoices(cr, uid, inv_values, purchase_id, context=context)
        res = inv_obj.onchange_payment_term_date_invoice(cr, uid, [result], inv_values['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
        inv_obj.write(cr, uid, [result], res['value'], context=context)
        return result
        
    def create_invoices(self, cr, uid, ids, context=None):
        """ create invoices for the active purchases orders """
        purchase_obj = self.pool.get('purchase.order')
        act_window = self.pool.get('ir.actions.act_window')
        wizard = self.browse(cr, uid, ids[0], context)
        purchase_ids = context.get('active_ids', [])
        
        purchase_obj.write(cr, uid, purchase_ids[0], {
            'invoice_milestone_rule_line_ids' : [(3, wizard.invoice_milestone_rule_line_id.id)],
        }, context=context)
        
        inv_ids = []        
        if wizard.is_final:
            # create the final invoices of the active sales orders
            context['wizard_payment_term'] = wizard.invoice_milestone_rule_line_id.payment_term and  wizard.invoice_milestone_rule_line_id.payment_term.id
            res = purchase_obj.manual_invoice(cr, uid, purchase_ids, context)
            if context.get('open_invoices', False):
                return res
            return {'type': 'ir.actions.act_window_close'}
        else:    
            for purchase_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, context=context):
                inv_ids.append(self._create_invoices(cr, uid, inv_values, purchase_id, context=context))

        if context.get('open_invoices', False):
            return self.open_invoices( cr, uid, ids, inv_ids, context=context)
        return {'type': 'ir.actions.act_window_close'}

#end of purchase_advance_payment_inv()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
