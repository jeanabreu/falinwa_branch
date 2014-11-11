# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import netsvc

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
   
    _columns = {
        'order_policy': fields.selection([
                ('manual', 'On Demand'),
                ('picking', 'On Delivery Order'),
                ('prepaid', 'Before Delivery'),
                ('project', 'Project Milestone'),
            ], 'Create Invoice', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
            help="""On demand: A draft invoice can be created from the sales order when needed. \nOn delivery order: A draft invoice can be created from the delivery order when the products have been delivered. \nBefore delivery: A draft invoice is created from the sales order and must be paid before the products can be delivered."""),
    }
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_button_confirm(cr, uid, ids, context=context)
        task_obj = self.pool.get('project.task')
        project_obj = self.pool.get('project.project')
        for sale in self.browse(cr, uid, ids, context=context):
            for line in sale.order_line:
                if line.product_id and line.product_id.categ_id.isfal_tools:
                    date_planned = self._get_date_planned(cr, uid, sale, line, sale.date_order, context=context)
                    project_ids = project_obj.search(cr, uid, [('analytic_account_id', '=', line.order_id.project_id.id)])
                    task_obj.create(cr, uid, {
                        'name': '%s:%s' % (line.order_id.name or '', line.name),
                        'date_deadline': date_planned,
                        'planned_hours': 0.00,
                        'remaining_hours': 0.00,
                        'partner_id': line.order_id.partner_id.id or False,
                        'user_id': line.product_id.product_manager.id,
                        'description': line.order_id.name + '\n' + (line.order_id.origin or ''),
                        'project_id':  project_ids and project_ids[0] or False,
                        'fal_sale_order_line_id': line.id or False,
                        'company_id': line.order_id.company_id.id or False,
                    },context=context)  
        
        return res

    def manual_invoice_project(self, cr, uid, ids, context=None):
        """ create invoices for the given sales orders (ids)
        """
        mod_obj = self.pool.get('ir.model.data')
        wf_service = netsvc.LocalService("workflow")

        # create invoices through the sales orders' workflow
        inv_ids0 = set(inv.id for sale in self.browse(cr, uid, ids, context) for inv in sale.invoice_ids)
        for id in ids:
            wf_service.trg_validate(uid, 'sale.order', id, 'manual_invoice', cr)
        inv_ids1 = set(inv.id for sale in self.browse(cr, uid, ids, context) for inv in sale.invoice_ids)
        # determine newly created invoices
        new_inv_ids = list(inv_ids1 - inv_ids0)

        res = mod_obj.get_object_reference(cr, uid, 'account', 'invoice_form')
        res_id = res and res[1] or False,
        return new_inv_ids and new_inv_ids[0] or False
        
#end of sale_order()

class product_category(orm.Model):
    _name = "product.category"
    _inherit = "product.category"
    
    _columns = {
        'isfal_tools' : fields.boolean('Tools'),
    }
    
#end of product_category()
