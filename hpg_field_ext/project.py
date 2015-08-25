from datetime import datetime, date, timedelta
from lxml import etree
import time

from openerp import SUPERUSER_ID
from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

class account_analytic_account(orm.Model):
    _name = "account.analytic.account"
    _inherit = "account.analytic.account"

    def _check_name_unique_insesitive(self, cr ,uid, ids, context=None):
        for project_id in self.browse(cr, uid, ids, context=context):
            if project_id.name:
                project_exist = self.search(cr ,uid ,[('name', '=ilike', project_id.name)], context=context)
                if len(project_exist) != 1:
                    return False
        return True

    _constraints = [
        (_check_name_unique_insesitive, 'Error! Project must have unique name', ['name'])
    ]
    
#end of account_analytic_account()