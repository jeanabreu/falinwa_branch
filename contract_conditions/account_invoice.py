from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    def onchange_contract_condition_id(self, cr, uid, ids, contract_condition_id, context=None):
        if not contract_condition_id:
            return {}
        return {'value': {'comment': self.pool.get('contract.condition').browse(cr, uid, contract_condition_id, context=context).content}}
    
    _columns = {
        'contract_condition_id' : fields.many2one('contract.condition','Contract Condition'),
    }

#end of account_invoice()