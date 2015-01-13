# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice_line(orm.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'
    
    def _get_default_project(self, cr, uid, context=None):
        project_id = False
        if context.get('partner', False):            
            partner_id = self.pool.get('res.partner').browse(cr, uid, context['partner'], context)
            project_id = partner_id.fal_project_id.id
        return project_id
        
    _defaults = {
        'account_analytic_id' : _get_default_project,
    }
    
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice',
            partner_id=False, fposition_id=False, price_unit=False, currency_id=False,
            company_id=None, context=None):
        
        if context is None:
            context = {}       
        
        res = super(account_invoice_line, self).product_id_change(cr ,uid, ids, product, uom_id, qty, name, type,
            partner_id, fposition_id, price_unit, currency_id,
            company_id, context=context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr, uid, partner_id, context)
            if partner.fal_project_id:
                res['value']['account_analytic_id'] = partner.fal_project_id.id
                return res
        if product:
            product_id = self.pool.get('product.product').browse(cr ,uid, product, context)
            res['value']['account_analytic_id'] = product_id.project_id.id
        return res
 
    
#end of account_invoice_line()

class account_bank_statement_line(orm.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
    }
    
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        res = super(account_bank_statement_line, self).onchange_product_id(cr, uid, ids, product_id, context=context)
        if product_id:
            product = self.pool.get('product.product').browse(cr ,uid, product_id)
            if product.project_id:
                res['value']['analytic_account_id'] = product.project_id.id
        return res

    def onchange_partner_id(self, cr, uid, ids, partner_id, context=None):
        res = super(account_bank_statement_line, self).onchange_partner_id(cr, uid, ids, partner_id, context=context)
        if partner_id:
            partner = self.pool.get('res.partner').browse(cr ,uid, partner_id)
            if partner.fal_project_id:
                res['value']['analytic_account_id'] = partner.fal_project_id.id
        return res
        
        
#end of account_bank_statement_line()