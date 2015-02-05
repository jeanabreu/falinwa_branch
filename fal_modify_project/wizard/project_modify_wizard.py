# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp import SUPERUSER_ID

class project_modify_wizard(orm.TransientModel):
    _name = "project.modify.wizard"
    _description = "Project Modify Wizard"
    
    _columns = {
        'project_id' : fields.many2one('account.analytic.account', 'Analytic Account', domain=[('type', '!=', 'view')]),
    }
    
    def _get_default_project(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, SUPERUSER_ID, context.get('active_id',False))
                if sale_id.project_id:
                    res = sale_id.project_id.id
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, SUPERUSER_ID, context.get('active_id',False))
                if purchase_id.order_line and purchase_id.order_line[0].account_analytic_id:
                    res = purchase_id.order_line[0].account_analytic_id.id
        return res 
    
    _defaults = {
        'project_id' : _get_default_project,
    }
    
    def update_project_id(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data_wizard = self.browse(cr, uid, ids, context)[0] 
        purchase_order_obj = self.pool.get('purchase.order')
        purchase_order_line_obj = self.pool.get('purchase.order.line')
        sale_order_obj = self.pool.get('sale.order')
        invoice_obj = self.pool.get('account.invoice')
        invoice_line_obj = self.pool.get('account.invoice.line')
        move_line_obj = self.pool.get('account.move.line')
        if context.get('active_model',False) == 'sale.order':
            #update project in order
            sale_order_obj.write(cr, SUPERUSER_ID, context.get('active_id',False), {
                'project_id' : data_wizard.project_id and data_wizard.project_id.id,
                
            })
            #update project in invoice
            for invoice_id in sale_order_obj.browse(cr, SUPERUSER_ID, context.get('active_id',False)).invoice_ids:
                for invoice_line_id in invoice_id.invoice_line:
                    invoice_line_obj.write(cr, SUPERUSER_ID, invoice_line_id.id, {
                        'account_analytic_id' : data_wizard.project_id.id,
                    })
            #update project in journal entries
                if invoice_id.move_id:
                    for move_line_id in invoice_id.move_id.line_id:
                        if move_line_id.credit:
                            move_line_obj.write(cr, SUPERUSER_ID, move_line_id.id, {
                                'analytic_account_id' : data_wizard.project_id.id,
                            })
        elif context.get('active_model',False) == 'purchase.order':          
            #update project in orderline
            for order_line_id in purchase_order_obj.browse(cr, SUPERUSER_ID, context.get('active_id',False)).order_line:                    
                purchase_order_line_obj.write(cr, SUPERUSER_ID, order_line_id.id, {
                    'account_analytic_id' : data_wizard.project_id.id,                
                })
            #update project in invoice
            for invoice_id in purchase_order_obj.browse(cr, SUPERUSER_ID, context.get('active_id',False)).invoice_ids:                
                for invoice_line_id in invoice_id.invoice_line:
                    invoice_line_obj.write(cr, SUPERUSER_ID, invoice_line_id.id, {
                        'account_analytic_id' : data_wizard.project_id and data_wizard.project_id.id,
                    })
            #update project in journal entries
                if invoice_id.move_id:
                    for move_line_id in invoice_id.move_id.line_id:
                        if move_line_id.debit:
                            move_line_obj.write(cr, SUPERUSER_ID, move_line_id.id, {
                                'analytic_account_id' : data_wizard.project_id.id,
                            })            
        return True

#end of project_modify_wizard()