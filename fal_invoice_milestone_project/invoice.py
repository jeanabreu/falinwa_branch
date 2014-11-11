from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    _columns = {
        'fal_task_ids' : fields.many2many('project.task', 'fal_task_invoice_rel', 'fal_invoice_id', 'fal_task_id', 'Tasks'),
    }

#end of account_invoice()