from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

class account_analytic_account(orm.Model):
    _name = 'account.analytic.account'
    _inherit = 'account.analytic.account'
    
    _columns = {
        'fal_is_business' :  fields.boolean('Is Business?'),
    }
    
#end of account_analytic_account()

class sale_order(orm.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
        'project_fal_is_business' :  fields.related('project_id','fal_is_business', type='boolean', string='Is Business?'),
    }
    
    def fal_refresh(self, cr, uid, ids, context=None):
        return True
    
#end of sale_order()

