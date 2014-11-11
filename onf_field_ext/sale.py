# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    
    _columns = {
        'project_id': fields.many2one('account.analytic.account', 'Project Number', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order."),
    }

#end of sale_order()

class product_category(orm.Model):
    _name = "product.category"
    _inherit = "product.category"

    _defaults = {
        'property_account_income_categ' : False,
        'property_account_expense_categ' : False,
    }
    
#end of product_category()