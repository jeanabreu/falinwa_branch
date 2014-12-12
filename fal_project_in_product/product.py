# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class product_product(orm.Model):
    _name = "product.product"
    _inherit = "product.product"
    
    _columns = {
        'project_id': fields.many2one('account.analytic.account', 'Project', ondelete='set null'),
        'customer_code' : fields.char('Customer Code',size=128),
        'customer_ref_number' : fields.char('Customer Reference Number',size=128),
    }

#end of product_product()