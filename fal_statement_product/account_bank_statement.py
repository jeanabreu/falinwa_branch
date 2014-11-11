# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class account_bank_statement_line(orm.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'
    
    _columns = {
        'product_id': fields.many2one('product.product', 'Product'),
    }
    
    def onchange_product_id(self, cr, uid, ids, product_id, context=None):
        val = {'name': '', 'account_id' : False}
        if product_id:
            product = self.pool.get('product.product').browse(cr, uid, product_id, context=context)
            val['name'] = product.description or product.name
            if product.categ_id.property_account_general_id:
                val['account_id'] = product.categ_id.property_account_general_id.id or False
            if product.property_account_general_id:
                val['account_id'] = product.property_account_general_id.id or False
        return {'value': val}
    
#end of account_bank_statement_line()

class product_category(orm.Model):
    _name = 'product.category'
    _inherit = 'product.category'
    
    _columns = {
        'property_account_general_id': fields.property(
            type='many2one',
            relation='account.account',
            string="General Account",
            view_load=True,
            help="This account will be used for statement instead of the default one to value for the current product."),
    }
#end of product_category()

class product_template(orm.Model):
    _name = 'product.template'
    _inherit = 'product.template'
    
    _columns = {
        'property_account_general_id': fields.property(
            type='many2one',
            relation='account.account',
            string="General Account",
            view_load=True,
            help="This account will be used for statement instead of the default one to value for the current product."),
    }
        
#end of product_product()