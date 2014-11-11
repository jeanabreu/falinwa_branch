from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare

class project_project(orm.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    def _get_rule_fal(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('project.task.type').browse(cr, uid, ids, context=context):
            for project in line.project_ids:
                result[project.id] = True
        return result.keys()

    def _total_percentage(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for project in self.browse(cr,uid,ids,context=context):
            percentage = 0.00
            for stage in project.type_ids:
                percentage += stage.percentage
            if not (percentage == 100.00 or percentage == 0.00) :
                raise osv.except_osv(_('Warning!'), _("Total Percentage Must be 100.00 or 0!"))
            res[project.id] = percentage
        return res

    _columns = {
        'percentage' : fields.function(_total_percentage, digits_compute=dp.get_precision('Account'), string='Total Percentage(%)',
            store={
                'project.project' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
                'project.task.type' : (_get_rule_fal, ['percentage'], 20),
            }),
    }

#end of project_project()

class project_task_type(orm.Model):
    _name = 'project.task.type'
    _inherit = 'project.task.type'

    _columns = {
        'percentage' : fields.float('Percentage (%)'),
        'payment_term' : fields.many2one('account.payment.term', 'Payment Term'),
        'fal_task_history_ids' : fields.many2many('project.task', 'fal_task_stage_rel', 'fal_stage_id', 'fal_task_id', 'History Tasks'),
    }

#end of project_task_type()

class task(orm.Model):
    _name = 'project.task'
    _inherit = 'project.task'

    def _total_percentage(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for task_id in self.browse(cr,uid,ids,context=context):
            percentage = 0.00
            for stage in task_id.fal_history_milestone_invoice_ids:
                percentage += stage.percentage
            res[task_id.id] = percentage
        return res
        
    _columns = {
        'fal_sale_order_line_id' : fields.many2one('sale.order.line', 'Sale Order Line'),
        'fal_history_milestone_invoice_ids' : fields.many2many('project.task.type', 'fal_task_stage_rel', 'fal_task_id', 'fal_stage_id', 'History Invoice Milestones'),
        'fal_invoice_ids' : fields.many2many('account.invoice', 'fal_task_invoice_rel', 'fal_task_id', 'fal_invoice_id', 'Invoices'),
        'fal_invoice_percentages' : fields.function(_total_percentage, digits_compute=dp.get_precision('Account'), string='Total Percentage(%)', store=True),
    }
    
    def write(self, cr, uid, ids, vals, context=None):
        if isinstance(ids, (int, long)):
            ids = [ids]
        if 'stage_id' in vals :
            stage_obj = self.pool.get('project.task.type')
            stage = stage_obj.browse(cr, uid, vals['stage_id'], context=context)
            for task_id in self.browse(cr, uid, ids, context): 
                if task_id.fal_sale_order_line_id:
                    temp_percentage = 0.00
                    temp_milestone_history_id = []
                    if stage.percentage:
                        for milestone_history in task_id.fal_history_milestone_invoice_ids:
                            temp_percentage += milestone_history.percentage
                            temp_milestone_history_id.append(milestone_history.id)

                        if vals['stage_id'] in temp_milestone_history_id:
                            continue               
                        vals['fal_history_milestone_invoice_ids'] = [(4, vals['stage_id'])]
                        
                        invoice_create_ids = []
                        #create invoice based on milestone
                        if temp_percentage + stage.percentage == 100.00:
                            #check all task related to order that still < 100
                            task_below_ids = self.search(cr, uid, [('id','!=',task_id.id),('fal_sale_order_line_id.order_id','=',task_id.fal_sale_order_line_id.order_id.id),('fal_invoice_percentages','<',100.00)], context=context)
                            if task_below_ids:
                                 #normal create invoice
                                invoice_create_ids = self.create_invoices(cr, uid, ids, vals['stage_id'], is_final=False, context=context)
                            else:
                                #consolidation final
                                invoice_create_ids = self.create_invoices(cr, uid, ids, vals['stage_id'], is_final=True, context=context)
                        else:
                            #normal create invoice
                            invoice_create_ids = self.create_invoices(cr, uid, ids, vals['stage_id'], is_final=False, context=context)
                        
                        if invoice_create_ids:
                            temp_iids = []
                            for iids in invoice_create_ids:
                                temp_iids.append((4, iids))
                            vals['fal_invoice_ids'] = temp_iids
        return super(task, self).write(cr, uid, ids, vals, context=context)    

    def _prepare_advance_invoice_vals(self, cr, uid, ids, stage_id, context=None):
        if context is None:
            context = {}
        sale_obj = self.pool.get('sale.order')
        ir_property_obj = self.pool.get('ir.property')
        fiscal_obj = self.pool.get('account.fiscal.position')
        inv_line_obj = self.pool.get('account.invoice.line')
        account_jrnl_obj = self.pool.get('account.journal')
        stage_obj = self.pool.get('project.task.type')
        stage = stage_obj.browse(cr, uid, stage_id, context)

        result = []
        for task in self.browse(cr, uid, ids, context=context):
            res = {}
            sale = task.fal_sale_order_line_id.order_id
            # determine and check expense account
            prop = ir_property_obj.get(cr, uid,
                        'property_account_income_categ', 'product.category', context=context)
            prop_id = prop and prop.id or False
            account_id = fiscal_obj.map_account(cr, uid, sale.fiscal_position or False, prop_id)
            if not account_id:
                raise osv.except_osv(_('Configuration Error!'),
                        _('There is no expense account defined as global property.'))
            res['account_id'] = account_id

            inv_amount = task.fal_sale_order_line_id.price_subtotal * stage.percentage / 100
            if not res.get('name', False):
                res['name'] = task.fal_sale_order_line_id.name + ': ' + stage.name

            # determine taxes
            temp_tax = []
            for tax in task.fal_sale_order_line_id.tax_id:
                temp_tax.append(tax.id)
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
                'payment_term': stage.payment_term.id or sale.payment_term and sale.payment_term.id or False,
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


    def create_invoices(self, cr, uid, ids, stage_id, is_final=False, context=None):
        """ create invoices for the active sale orders """
        sale_obj = self.pool.get('sale.order')
        stage_obj = self.pool.get('project.task.type')
        inv_ids = []
        for task in self.browse(cr, uid, ids, context=context):
            if is_final:
                # create the final invoices of the active sales orders
                context['wizard_payment_term'] = stage_obj.browse(cr, uid, stage_id, context=context).payment_term.id
                inv_ids.append(sale_obj.manual_invoice_project(cr, uid, [task.fal_sale_order_line_id.order_id.id], context=context))
            else:
                for sale_id, inv_values in self._prepare_advance_invoice_vals(cr, uid, ids, stage_id, context=context):
                    inv_ids.append(self._create_invoices(cr, uid, inv_values, sale_id, context=context))
        
        return inv_ids
        
#end of task()