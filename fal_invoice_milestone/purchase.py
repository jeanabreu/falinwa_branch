# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        default.update({
            'invoice_milestone_rule_line_ids': [],
        })
        return super(purchase_order, self).copy(cr, uid, id, default, context=context)
        
    _columns = {
        'invoice_milestone_rule_id' : fields.many2one('fal.invoice.milestone','Invoice Milestone Rule',domain=[('active','=',True)]),
        'invoice_milestone_rule_line_ids' : fields.many2many('fal.rule.lines', 'purchase_order_rule_line_rel',id1='order_id', id2='rule_id', string='Mile Stone Rule'),
        'invoice_method': fields.selection([('manual','Based on Purchase Order lines'),('order','Based on generated draft invoice'),('picking','Based on incoming shipments'),('demand','On Demand')], 'Invoicing Control', required=True,
                    readonly=True, states={'draft':[('readonly',False)], 'sent':[('readonly',False)]},
                    help="Based on Purchase Order lines: place individual lines in 'Invoice Control > Based on P.O. lines' from where you can selectively create an invoice.\n" \
                        "Based on generated invoice: create a draft invoice you can validate later.\n" \
                        "Bases on incoming shipments: let you create an invoice when receptions are validated.\n" \
                        "Based on Demand: Let you create an invoice based on percentage"
                ),
    }
    
    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        """Prepare the dict of values to create the new invoice for a
           purchase order. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record order: purchase.order record to invoice
           :param list(int) line: list of invoice line IDs that must be
                                  attached to the invoice
           :return: dict of value to create() the invoice
        """
        if context is None:
            context = {}
        journal_ids = self.pool.get('account.journal').search(cr, uid,
            [('type', '=', 'purchase'), ('company_id', '=', order.company_id.id)],
            limit=1)
        if not journal_ids:
            raise osv.except_osv(_('Error!'),
                _('Please define purchase journal for this company: "%s" (id:%d).') % (order.company_id.name, order.company_id.id))
        invoice_vals = {
            'name': order.partner_ref or order.name or '',
            'origin': order.name,
            'type': 'in_invoice',
            'reference': order.partner_ref or order.name or '',
            'account_id': order.partner_id.property_account_payable.id,
            'partner_id': order.partner_id.id,
            'journal_id': journal_ids[0],
            'invoice_line': [(6, 0, lines)],
            'currency_id': order.pricelist_id.currency_id.id,
            'comment': order.notes,
            'payment_term': context.get('wizard_payment_term',False) or order.payment_term_id and order.payment_term_id.id or False,
            'fiscal_position': order.fiscal_position.id or order.partner_id.property_account_position.id,
            'date_invoice': context.get('date_invoice', False),
            'company_id': order.company_id.id,
        }

        return invoice_vals

    def _make_invoice(self, cr, uid, order, lines, context=None):
        inv_obj = self.pool.get('account.invoice')
        obj_invoice_line = self.pool.get('account.invoice.line')
        if context is None:
            context = {}
        invoiced_purchase_line_ids = self.pool.get('purchase.order.line').search(cr, uid, [('order_id', '=', order.id), ('invoiced', '=', True)], context=context)
        from_line_invoice_ids = []
        for invoiced_purchase_line_id in self.pool.get('purchase.order.line').browse(cr, uid, invoiced_purchase_line_ids, context=context):
            for invoice_line_id in invoiced_purchase_line_id.invoice_lines:
                if invoice_line_id.invoice_id.id not in from_line_invoice_ids:
                    from_line_invoice_ids.append(invoice_line_id.invoice_id.id)
        for preinv in order.invoice_ids:
            if preinv.state not in ('cancel',) and preinv.id not in from_line_invoice_ids:
                for preline in preinv.invoice_line:
                    inv_line_id = obj_invoice_line.copy(cr, uid, preline.id, {'invoice_id': False, 'price_unit': -preline.price_unit})
                    lines.append(inv_line_id)
        inv = self._prepare_invoice(cr, uid, order, lines, context=context)
        inv_id = inv_obj.create(cr, uid, inv, context=context)
        data = inv_obj.onchange_payment_term_date_invoice(cr, uid, [inv_id], inv['payment_term'], time.strftime(DEFAULT_SERVER_DATE_FORMAT))
        if data.get('value', False):
            inv_obj.write(cr, uid, [inv_id], data['value'], context=context)
        inv_obj.button_compute(cr, uid, [inv_id])
        return inv_id

    def manual_invoice(self, cr, uid, ids, context=None):
        """ create invoices for the given purchase orders (ids), and open the form
            view of one of the newly created invoices
        """
        mod_obj = self.pool.get('ir.model.data')

        # create invoices through the purchase orders' workflow
        inv_ids0 = set(inv.id for purchase in self.browse(cr, uid, ids, context) for inv in purchase.invoice_ids)
        for id in ids:
            self.action_invoice_create_fal(cr, uid, ids, context=context)
        inv_ids1 = set(inv.id for purchase in self.browse(cr, uid, ids ,context) for inv in purchase.invoice_ids)
        # determine newly created invoices
        new_inv_ids = list(inv_ids1 - inv_ids0)

        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_supplier_form')
        res_id = res and res[1] or False,

        return {
            'name': _('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [res_id],
            'res_model': 'account.invoice',
            'context': "{'type':'in_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': new_inv_ids and new_inv_ids[0] or False,
        }
        
    def action_invoice_create_fal(self, cr, uid, ids, grouped=False, states=None, date_invoice = False, context=None):
        if states is None:
            states = ['confirmed', 'done']
        res = False
        invoices = {}
        invoice_ids = []
        invoice = self.pool.get('account.invoice')
        obj_purchase_order_line = self.pool.get('purchase.order.line')
        partner_currency = {}
        if context is None:
            context = {}
        # If date was specified, use it as date invoiced, usefull when invoices are generated this month and put the
        # last day of the last month as invoice date
        if date_invoice:
            context['date_invoice'] = date_invoice
        for o in self.browse(cr, uid, ids, context=context):
            currency_id = o.pricelist_id.currency_id.id
            if (o.partner_id.id in partner_currency) and (partner_currency[o.partner_id.id] <> currency_id):
                raise osv.except_osv(
                    _('Error!'),
                    _('You cannot group purchases having different currencies for the same partner.'))

            partner_currency[o.partner_id.id] = currency_id
            lines = []
            for line in o.order_line:
                if line.invoiced:
                    continue
                elif (line.state in states):
                    lines.append(line.id)
            
            created_lines = obj_purchase_order_line.invoice_line_create(cr, uid, lines)
            if created_lines:
                invoices.setdefault(o.partner_id.id, []).append((o, created_lines))
        if not invoices:
            for o in self.browse(cr, uid, ids, context=context):
                for i in o.invoice_ids:
                    if i.state == 'draft':
                        return i.id
        for val in invoices.values():
            if grouped:
                res = self._make_invoice(cr, uid, val[0][0], reduce(lambda x, y: x + y, [l for o, l in val], []), context=context)
                invoice_ref = ''
                for o, l in val:
                    invoice_ref += o.name + '|'
                    self.write(cr, uid, [o.id], {'state': 'approved'})
                    cr.execute('insert into purchase_invoice_rel (purchase_id,invoice_id) values (%s,%s)', (o.id, res))
                #remove last '|' in invoice_ref
                if len(invoice_ref) >= 1: 
                    invoice_ref = invoice_ref[:-1]
                invoice.write(cr, uid, [res], {'origin': invoice_ref, 'name': invoice_ref})
            else:
                for order, il in val:
                    res = self._make_invoice(cr, uid, order, il, context=context)
                    invoice_ids.append(res)
                    self.write(cr, uid, [order.id], {'state': 'approved'})
                    cr.execute('insert into purchase_invoice_rel (purchase_id,invoice_id) values (%s,%s)', (order.id, res))
        return res
        
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        todo = []
        for po in self.browse(cr, uid, ids, context=context):
            if not po.invoice_milestone_rule_id and po.invoice_method == 'demand' :
                raise osv.except_osv(_('Warning!'), _("Invoice Milestone Rule must be define..!"))
            if po.invoice_milestone_rule_id and po.invoice_method == 'demand' :
                temp_rule_line_id = []
                for rule_line in po.invoice_milestone_rule_id.rule_ids:
                    temp_rule_line_id.append(rule_line.id)
                    self.write(cr, uid, po.id, {
                        'invoice_milestone_rule_line_ids' : [(6, 0, temp_rule_line_id)],
                    } ,context)
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)
    
    def view_invoice(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        wizard_obj = self.pool.get('purchase.order.line_invoice')
        for po in self.browse(cr, uid, ids, context=context):
            if po.invoice_method == 'demand':
                if not po.invoice_ids and not po.invoice_milestone_rule_id:
                    context.update({'active_ids' :  [line.id for line in po.order_line]})
                    wizard_obj.makeInvoices(cr, uid, [], context=context)
                if po.invoice_milestone_rule_line_ids: 
                    return {
                        'type': 'ir.actions.act_window',
                        'name': _('Invoice Advance management'),
                        'res_model': 'purchase.advance.payment.inv',
                        'view_type': 'form',
                        'view_mode': 'form',
                        'target': 'new',
                        'nodestroy': True,
                    }
                else:
                    return self.invoice_open(cr, uid ,ids, context)
        return super(purchase_order, self).view_invoice(cr, uid, ids, context)
        
#end of purchase_order()

class purchase_order_line(orm.Model):
    _name = "purchase.order.line"
    _inherit = "purchase.order.line"
    
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Prepare the dict of values to create the new invoice line for a
           purchase order line. This method may be overridden to implement custom
           invoice generation (making sure to call super() to establish
           a clean extension chain).

           :param browse_record line: purchase.order.line record to invoice
           :param int account_id: optional ID of a G/L account to force
               (this is used for returning products including service)
           :return: dict of values to create() the invoice line
        """
        res = {}
        if not line.invoiced:
            if not account_id:
                if line.product_id:
                    account_id = line.product_id.property_account_expense.id
                    if not account_id:
                        account_id = line.product_id.categ_id.property_account_expense_categ.id
                    if not account_id:
                        raise osv.except_osv(_('Error!'),
                                _('Please define expense account for this product: "%s" (id:%d).') % \
                                    (line.product_id.name, line.product_id.id,))
                else:
                    prop = self.pool.get('ir.property').get(cr, uid,
                            'property_account_expense_categ', 'product.category',
                            context=context)
                    account_id = prop and prop.id or False
            pu = 0.0
            fpos = line.order_id.fiscal_position or False
            account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
            if not account_id:
                raise osv.except_osv(_('Error!'),
                            _('There is no Fiscal Position defined or Expense category account defined for default properties of Product categories.'))
            
            res = self.pool.get('purchase.order')._prepare_inv_line(cr, uid, account_id, line, context=None)
        return res
        
    def invoice_line_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}

        create_ids = []
        purchases = set()
        for line in self.browse(cr, uid, ids, context=context):
            vals = self._prepare_order_line_invoice_line(cr, uid, line, False, context)
            if vals:
                inv_id = self.pool.get('account.invoice.line').create(cr, uid, vals, context=context)
                self.write(cr, uid, [line.id], {'invoice_lines': [(4, inv_id)]}, context=context)
                purchases.add(line.order_id.id)
                create_ids.append(inv_id)
        return create_ids
        
#end of purchase_order_line()