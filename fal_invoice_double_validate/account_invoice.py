from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.exceptions import except_orm, Warning, RedirectWarning
import time

class account_invoice(models.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    state = fields.Selection(selection_add=[
                ('validate1','Double Validate'),
                ('validate2','Final Validate'),
                ])
             
    """
    def __init__(self, pool, cr):
        init_res = super(account_invoice, self).__init__(pool, cr)
        option1 = ('validate1','Double Validate')
        option2 = ('validate2','Final Validate')
        state_selection = self._columns['state'].selection
        if option1 not in state_selection:
            state_selection.append(option1)        
        if option2 not in state_selection:
            state_selection.append(option2)
        return init_res
    """
    
    @api.multi
    def invoice_validate1(self):
        return self.write({'state': 'validate1'})

    @api.multi
    def invoice_validate2(self):
        return self.write({'state': 'validate2'})
    
    @api.multi
    def action_backto_validate1(self):
        move_lines = self.env['account.move.line']
        ctx = {}
        for inv in self:
            if inv.move_id:
                inv.move_id.button_cancel()                
                for iml in inv.move_id.line_id:
                    if iml.reconcile_partial_id or iml.reconcile_id:
                        raise except_orm(_('Error!'), _('You cannot cancel an invoice which is partially paid. You need to unreconcile related payment entries first.'))
                    if iml.fal_second_post:
                        move_lines += iml
                move_lines.with_context({'asda':'asd'}).unlink()
                inv.move_id.post()
        self._log_event(-1.0, 'Cancel Invoice')
        return True
    
    #copy from oficial openerp method
    @api.multi
    def action_move_create1(self):
        """ Creates invoice related analytics and financial move lines """
        account_invoice_tax = self.env['account.invoice.tax']
        account_move = self.env['account.move']

        for inv in self:
            if not inv.journal_id.sequence_id:
                raise except_orm(_('Error!'), _('Please define sequence on the journal related to this invoice.'))
            if not inv.invoice_line:
                raise except_orm(_('No Invoice Lines!'), _('Please create some invoice lines.'))
            if inv.move_id:
                continue

            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            date_invoice = inv.date_invoice

            company_currency = inv.company_id.currency_id
            # create the analytical lines, one move line per invoice line
            iml = inv._get_analytic_lines()
            # check if taxes are all computed
            compute_taxes = account_invoice_tax.compute(inv)
            inv.check_tax_lines(compute_taxes)

            # I disabled the check_total feature
            if self.env['res.users'].has_group('account.group_supplier_inv_check_total'):
                if inv.type in ('in_invoice', 'in_refund') and abs(inv.check_total - inv.amount_total) >= (inv.currency_id.rounding / 2.0):
                    raise except_orm(_('Bad Total!'), _('Please verify the price of the invoice!\nThe encoded total does not match the computed total.'))

            if inv.payment_term:
                total_fixed = total_percent = 0
                for line in inv.payment_term.line_ids:
                    if line.value == 'fixed':
                        total_fixed += line.value_amount
                    if line.value == 'procent':
                        total_percent += line.value_amount
                total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
                if (total_fixed + total_percent) > 100:
                    raise except_orm(_('Error!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))

            # one move line per tax line
            # hans modify this as first validate not need to post tax
            #iml += account_invoice_tax.move_line_get(inv.id)

            if inv.type in ('in_invoice', 'in_refund'):
                ref = inv.reference
            else:
                ref = inv.number

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)

            name = inv.name or inv.supplier_invoice_number or '/'
            totlines = []
            if inv.payment_term:
                totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
            if totlines:
                res_amount_currency = total_currency
                ctx['date'] = date_invoice
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                    })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'ref': ref
                })

            date = date_invoice

            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)

            line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            if journal.centralisation:
                raise except_orm(_('User Error!'),
                        _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))

            line = inv.finalize_invoice_move_lines(line)

            move_vals = {
                'ref': inv.reference or inv.name,
                'line_id': line,
                'journal_id': journal.id,
                'date': inv.date_invoice,
                'narration': inv.comment,
                'company_id': inv.company_id.id,
            }
            ctx['company_id'] = inv.company_id.id
            period = inv.period_id
            if not period:
                period = period.with_context(ctx).find(date_invoice)[:1]
            if period:
                move_vals['period_id'] = period.id
                for i in line:
                    i[2]['period_id'] = period.id

            ctx['invoice'] = inv
            move = account_move.with_context(ctx).create(move_vals)
            # make the invoice point to that move
            vals = {
                'move_id': move.id,
                'period_id': period.id,
                'move_name': move.name,
            }
            inv.with_context(ctx).write(vals)
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            move.post()
        self._log_event()
        return True
        
    #copy from oficial openerp method    
    @api.multi
    def action_move_create2(self):
        """ Creates invoice related analytics and financial move lines """
        account_invoice_tax = self.env['account.invoice.tax']
        account_move = self.env['account.move']
        account_move_line = self.env['account.move.line']

        for inv in self:
            #hans modif in here, remove some line
            
            ctx = dict(self._context, lang=inv.partner_id.lang)

            if not inv.date_invoice:
                inv.with_context(ctx).write({'date_invoice': fields.Date.context_today(self)})
            date_invoice = inv.date_invoice

            company_currency = inv.company_id.currency_id
            # create the analytical lines, one move line per invoice line
            iml = inv._get_analytic_lines()
            
            #hans modif in here, remove some line
            #modify to AP or AR instead of product ledger account 
            for fal_move_line in iml:
                fal_move_line['name'] = '/'
                fal_move_line['account_id'] = inv.account_id.id
                fal_move_line['account_analytic_id'] = False
                fal_move_line['taxes'] = []
                fal_move_line['tax_code_id'] = False
                fal_move_line['tax_amount'] = False
                
            # check if taxes are all computed
            compute_taxes = account_invoice_tax.compute(inv)
            inv.check_tax_lines(compute_taxes)

            if inv.payment_term:
                total_fixed = total_percent = 0
                for line in inv.payment_term.line_ids:
                    if line.value == 'fixed':
                        total_fixed += line.value_amount
                    if line.value == 'procent':
                        total_percent += line.value_amount
                total_fixed = (total_fixed * 100) / (inv.amount_total or 1.0)
                if (total_fixed + total_percent) > 100:
                    raise except_orm(_('Error!'), _("Cannot create the invoice.\nThe related payment term is probably misconfigured as it gives a computed amount greater than the total invoiced amount. In order to avoid rounding issues, the latest line of your payment term must be of type 'balance'."))

            # one move line per tax line
            iml += account_invoice_tax.move_line_get(inv.id)

            if inv.type in ('in_invoice', 'in_refund'):
                ref = inv.reference
            else:
                ref = inv.number

            diff_currency = inv.currency_id != company_currency
            # create one move line for the total and possibly adjust the other lines amount
            total, total_currency, iml = inv.with_context(ctx).compute_invoice_totals(company_currency, ref, iml)

            name = inv.name or inv.supplier_invoice_number or '/'
            totlines = []
            if inv.payment_term:
                totlines = inv.with_context(ctx).payment_term.compute(total, date_invoice)[0]
            if totlines:
                res_amount_currency = total_currency
                ctx['date'] = date_invoice
                for i, t in enumerate(totlines):
                    if inv.currency_id != company_currency:
                        amount_currency = company_currency.with_context(ctx).compute(t[1], inv.currency_id)
                    else:
                        amount_currency = False

                    # last line: add the diff
                    res_amount_currency -= amount_currency or 0
                    if i + 1 == len(totlines):
                        amount_currency += res_amount_currency

                    iml.append({
                        'type': 'dest',
                        'name': name,
                        'price': t[1],
                        'account_id': inv.account_id.id,
                        'date_maturity': t[0],
                        'amount_currency': diff_currency and amount_currency,
                        'currency_id': diff_currency and inv.currency_id.id,
                        'ref': ref,
                    })
            else:
                iml.append({
                    'type': 'dest',
                    'name': name,
                    'price': total,
                    'account_id': inv.account_id.id,
                    'date_maturity': inv.date_due,
                    'amount_currency': diff_currency and total_currency,
                    'currency_id': diff_currency and inv.currency_id.id,
                    'ref': ref,
                })

            date = date_invoice

            part = self.env['res.partner']._find_accounting_partner(inv.partner_id)


            for falml in iml:
                falml['fal_second_post'] = 1
                
            line = [(0, 0, self.line_get_convert(l, part.id, date)) for l in iml]
            line = inv.group_lines(iml, line)

            journal = inv.journal_id.with_context(ctx)
            if journal.centralisation:
                raise except_orm(_('User Error!'),
                        _('You cannot create an invoice on a centralized journal. Uncheck the centralized counterpart box in the related journal from the configuration menu.'))
            print line
            line = inv.finalize_invoice_move_lines(line)
            
            
            inv.move_id.button_cancel()
            inv.move_id.write({'line_id':line})
            
            #Hans edit in here, remove some line
            #reconcile on allow reconciliation
            temp_iml_reconcile = []
            temp_reconcile_amount = 0.00
            
            for iml in inv.move_id.line_id:
                print iml.fal_second_post
                if iml.account_id.reconcile and iml.fal_second_post:
                    temp_iml_reconcile.append(iml.id)
                    temp_reconcile_amount += iml.credit
                    temp_reconcile_amount -= iml.debit
            
            if temp_iml_reconcile:
                aml_reconcile_ids = account_move_line.browse(temp_iml_reconcile)
                if temp_reconcile_amount == 0:
                    #full reconcile
                    aml_reconcile_ids.reconcile()
                else:
                    #partial reconcile
                    print temp_iml_reconcile
                    aml_reconcile_ids.reconcile_partial()
            # Pass invoice in context in method post: used if you want to get the same
            # account move reference when creating the same invoice after a cancelled one:
            inv.move_id.post()
        self._log_event()
        return True

    @api.model
    def line_get_convert(self, line, part, date):
        res = super(account_invoice, self).line_get_convert(line, part, date)
        res['fal_second_post']= line.get('fal_second_post', False)
        return res
        
#end of account_invoice()

class account_move_line(models.Model):
    _name = "account.move.line"
    _inherit = "account.move.line"
    
    fal_second_post = fields.Boolean("Second Post")
    
#end of account_move_line()