# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'invoice_milestone_rule_line_ids': [],
        })
        return super(sale_order, self).copy(cr, uid, id, default, context=context)
        
    _columns = {
        'invoice_milestone_rule_id' : fields.many2one('fal.invoice.milestone','Invoice Milestone Rule',domain=[('active','=',True)]),
        'invoice_milestone_rule_line_ids' : fields.many2many('fal.rule.lines', 'sale_order_rule_line_rel',id1='order_id', id2='rule_id', string='Mile Stone Rule'),
        'x_quotationversioning' : fields.char('Final Quotation Number', size=512),
    }

    def action_button_confirm(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        
        for sale_id in self.browse(cr, uid, ids, context):
            if not sale_id.invoice_milestone_rule_id and sale_id.order_policy == 'manual' :
                raise orm.except_orm(_('Warning!'), _("Invoice Milestone Rule must be define..!"))
            if sale_id.invoice_milestone_rule_id and sale_id.order_policy == 'manual' :
                temp_rule_line_id = []
                for rule_line in sale_id.invoice_milestone_rule_id.rule_ids:
                    temp_rule_line_id.append(rule_line.id)
                    self.write(cr, uid, [sale_id.id], {
                        'invoice_milestone_rule_line_ids' : [(6, 0, temp_rule_line_id)],
                    } ,context)
        return super(sale_order, self).action_button_confirm(cr, uid, ids, context)

    def action_create_invoices_milestone(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for sale_id in self.browse(cr, uid, ids, context):
            if sale_id.invoice_milestone_rule_line_ids:
                return {'type': 'ir.actions.act_window',
                    'name': _('Invoice Advance management'),
                    'res_model': 'fsale.advance.payment.inv',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'target': 'new',
                    'nodestroy': True,}
            else:
                return self.action_view_invoice(cr, uid, ids, context)
        return True

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context=context)
        res['payment_term'] = context.get('wizard_payment_term',False) or order.payment_term and order.payment_term.id or False
        return res
    
    """        
    def action_create_invoices_milestone(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        ir_property_obj = self.pool.get('ir.property')
        fiscal_obj = self.pool.get('account.fiscal.position')
        inv_obj = self.pool.get('account.invoice')
        inv_line_obj = self.pool.get('account.invoice.line')
        sale_id = self.browse(cr,uid,ids)[0]
        for rule_id in sale_id.invoice_milestone_rule_id.rule_ids:
            val = inv_line_obj.product_id_change(cr, uid, [], False,
                    uom_id=False, partner_id=sale_id.partner_id.id, fposition_id=sale_id.fiscal_position.id)
            res = val['value']
            prop = ir_property_obj.get(cr, uid,
                        'property_account_income_categ', 'product.category', context=context)
            prop_id = prop and prop.id or False
            account_id = fiscal_obj.map_account(cr, uid, sale_id.fiscal_position or False, prop_id)
            if not account_id:
                raise orm.except_orm(_('Configuration Error!'),
                        _('There is no income account defined as global property.'))
            res['account_id'] = account_id
            inv_amount = sale_id.amount_total * rule_id.percentage / 100
            res['name'] = rule_id.description
            # determine taxes
            if res.get('invoice_line_tax_id'):
                res['invoice_line_tax_id'] = [(6, 0, res.get('invoice_line_tax_id'))]
            else:
                res['invoice_line_tax_id'] = False  
            # create the invoice
            inv_line_values = {
                'name': res.get('name'),
                'origin': sale_id.name,
                'account_id': res['account_id'],
                'price_unit': inv_amount,
                'quantity': 1.0,
                'discount': False,
                'uos_id': res.get('uos_id', False),
                'product_id': False,
                'invoice_line_tax_id': res.get('invoice_line_tax_id'),
                'account_analytic_id': sale_id.project_id.id or False,
            }
            inv_line_id = inv_line_obj.create(cr, uid, inv_line_values, context=context)
            inv = self._prepare_invoice(cr, uid, sale_id, [inv_line_id], context=context)
            inv_id = inv_obj.create(cr, uid, inv, context=context)
            data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
            if data.get('value', False):
                inv_obj.write(cr, uid, [inv_id], data['value'], context=context)
            inv_obj.button_compute(cr, uid, [inv_id])
            inv_obj.button_reset_taxes(cr, uid, [inv_id], context=context)
            self.write(cr, uid, sale_id.id, {'invoice_ids': [(4, inv_id)]}, context=context)
        return self.action_view_invoice( cr, uid, ids, context=context)
    """    
#end of sale_order()

class fal_invoice_milestone(orm.Model):
    _name = "fal.invoice.milestone"
    _description = "Invoice milestone rule"

    def _get_rule_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('fal.rule.lines').browse(cr, uid, ids, context=context):
            result[line.invoice_milestone_id.id] = True
        return result.keys()

    def _total_percentage(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for invoice_milestone_id in self.browse(cr,uid,ids,context=context):
            percentage = 0.00
            for rule_id in invoice_milestone_id.rule_ids:
                percentage += rule_id.percentage
            if percentage != 100.00 and invoice_milestone_id.active:
                raise orm.except_orm(_('Warning!'), _("Total Percentage Must be 100.00!"))
            res[invoice_milestone_id.id] = percentage
        return res
        
    _columns = {
        'name' : fields.char('Name',size=64,required=True),
        'description' : fields.text('Description'),
        'active' : fields.boolean('Active'),
        'rule_ids' : fields.one2many('fal.rule.lines','invoice_milestone_id','Rule Line'),
        'percentage' : fields.function(_total_percentage, digits_compute=dp.get_precision('Account'), string='Total Percentage(%)',
            store={
                'fal.invoice.milestone' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'fal.rule.lines' : (_get_rule_fal, ['percentage','description'], 20),
            }),
    }
    
    _defaults = {
        'active' : True,
    }
    
#end of fal_invoice_milestone()

class fal_rule_lines(orm.Model):
    _name = "fal.rule.lines"
    _description = "Rule Line"
    
    _columns = {
        'invoice_milestone_id' : fields.many2one('fal.invoice.milestone','Invoice Milestone Rule'),
        'percentage' : fields.float('Percentage (%)'),
        'description' : fields.char('Description', size=128, required=True),
        'payment_term' : fields.many2one('account.payment.term', 'Payment Term'),
        'sequence' : fields.integer('Sequence',required=True),
    }
    
#end of fal_rule_lines()
