from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

from openerp.addons.resource.faces import task as Task

class account_analytic_account(orm.Model):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'
    
    _columns = {
        'fal_sale_order_ids' : fields.one2many('sale.order', 'project_id', 'Sale Orders', readonly=True),
        'fal_purchase_order_line_ids' : fields.one2many('purchase.order.line', 'account_analytic_id', 'Purchase Orders Line', readonly=True),
        'fal_invoice_line_ids' : fields.one2many('account.invoice.line', 'account_analytic_id', 'Invoice Line', readonly=True),
    }
    
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'fal_sale_order_ids':[],
            'fal_purchase_order_line_ids':[],
            'fal_invoice_line_ids':[],
        })        
        return super(account_analytic_account, self).copy(cr, uid, id, default, context)
    
#end of account_analytic_account()