# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class project_update_wizard(orm.TransientModel):
    _name = "project.update.wizard"
    _description = "Order Revised Wizard"
    
    _columns = {
        'project_id' : fields.many2one('account.analytic.account', 'Analytic Account', domain=[('parent_id', '!=', False)]),
        'partner_id' : fields.many2one('res.partner', 'Partner', required=True),
        'partner_invoice_id' : fields.many2one('res.partner', 'Invoice Address'),
        'partner_shipping_id' : fields.many2one('res.partner', 'Delivery Address'),
        'partner_ref' : fields.char('Reference',size=64),
        'pricelist_id': fields.many2one('product.pricelist', 'Pricelist', required=True),
        'date_order' : fields.date('Order Date', required=True),
    }
    
    def _get_default_project(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.project_id:
                    res = sale_id.project_id.id
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.order_line and purchase_id.order_line[0].account_analytic_id:
                    res = purchase_id.order_line[0].account_analytic_id.id
        return res 
        
    def _get_default_partner(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.partner_id:
                    res = sale_id.partner_id.id
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.partner_id:
                    res = purchase_id.partner_id.id
        return res 
        
    def _get_default_partner_invoice(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.partner_id:
                    res = sale_id.partner_invoice_id.id
        #elif context.get('active_model',False) == 'purchase.order':
        #    purchase_obj = self.pool.get('purchase.order')
        #    if context.get('active_id',False):
        #        purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
        #        if purchase_id.partner_id:
        #            res = purchase_id.partner_id.id
        return res 
        
    def _get_default_partner_shipping(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.partner_id:
                    res = sale_id.partner_shipping_id.id
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.partner_id:
                    res = purchase_id.dest_address_id.id
        return res 
        
    def _get_default_partner_ref(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = ''
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.client_order_ref:
                    res = sale_id.client_order_ref
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.partner_ref:
                    res = purchase_id.partner_ref
        return res 
        
    def _get_default_pricelist(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = ''
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.pricelist_id:
                    res = sale_id.pricelist_id.id
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.pricelist_id:
                    res = purchase_id.pricelist_id.id
        return res 
        
    def _get_default_date_order(self, cr, uid, context=None):
        if context is None:
            context = {}
        res = False
        if context.get('active_model',False) == 'sale.order':
            sale_obj = self.pool.get('sale.order')
            if context.get('active_id',False):
                sale_id  = sale_obj.browse(cr, uid, context.get('active_id',False))
                if sale_id.date_order:
                    res = sale_id.date_order
        elif context.get('active_model',False) == 'purchase.order':
            purchase_obj = self.pool.get('purchase.order')
            if context.get('active_id',False):
                purchase_id  = purchase_obj.browse(cr, uid, context.get('active_id',False))
                if purchase_id.date_order:
                    res = purchase_id.date_order
        return res 
    
    _defaults = {
        'project_id' : _get_default_project,
        'partner_id' : _get_default_partner,
        'partner_invoice_id' : _get_default_partner_invoice,
        'partner_shipping_id' : _get_default_partner_shipping,
        'partner_ref' : _get_default_partner_ref,
        'pricelist_id' :  _get_default_pricelist,
        'date_order' : _get_default_date_order,
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
            sale_order_obj.write(cr, uid, context.get('active_id',False), {
                'project_id' : data_wizard.project_id and data_wizard.project_id.id,
                'partner_id' : data_wizard.partner_id.id,
                'partner_invoice_id' : data_wizard.partner_invoice_id.id,
                'partner_shipping_id' : data_wizard.partner_shipping_id.id,
                'client_order_ref' : data_wizard.partner_ref,
                'pricelist_id' : data_wizard.pricelist_id.id,
                'date_order' : data_wizard.date_order,
                
            })
            #update project in invoice
            for invoice_id in sale_order_obj.browse(cr, uid, context.get('active_id',False)).invoice_ids:
                for invoice_line_id in invoice_id.invoice_line:
                    invoice_line_obj.write(cr, uid, invoice_line_id.id, {
                        'account_analytic_id' : data_wizard.project_id.id,
                    })
            #update project in journal entries
                if invoice_id.move_id:
                    for move_line_id in invoice_id.move_id.line_id:
                        if move_line_id.credit:
                            move_line_obj.write(cr, uid, move_line_id.id, {
                                'analytic_account_id' : data_wizard.project_id.id,
                            })
        elif context.get('active_model',False) == 'purchase.order':
            purchase_order_obj.write(cr, uid, context.get('active_id',False), {
                'partner_id' : data_wizard.partner_id.id,
                'dest_address_id' : data_wizard.partner_shipping_id.id,
                'partner_ref' : data_wizard.partner_ref,
                'pricelist_id' : data_wizard.pricelist_id.id,
                'date_order' : data_wizard.date_order,
            })            
            #update project in orderline
            for order_line_id in purchase_order_obj.browse(cr, uid, context.get('active_id',False)).order_line:                    
                purchase_order_line_obj.write(cr, uid, order_line_id.id, {
                    'account_analytic_id' : data_wizard.project_id.id,                
                })
            #update project in invoice
            for invoice_id in purchase_order_obj.browse(cr, uid, context.get('active_id',False)).invoice_ids:                
                for invoice_line_id in invoice_id.invoice_line:
                    invoice_line_obj.write(cr, uid, invoice_line_id.id, {
                        'account_analytic_id' : data_wizard.project_id and data_wizard.project_id.id,
                    })
            #update project in journal entries
                if invoice_id.move_id:
                    for move_line_id in invoice_id.move_id.line_id:
                        if move_line_id.debit:
                            move_line_obj.write(cr, uid, move_line_id.id, {
                                'analytic_account_id' : data_wizard.project_id.id,
                            })            
        return True

#end of project_update_wizard()