from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = "account.voucher"
    _inherit = "account.voucher"

    def onchange_contract_condition_id(self, cr, uid, ids, contract_condition_id, context=None):
        if not contract_condition_id:
            return {}
        return {'value': {'narration': self.pool.get('contract.condition').browse(cr, uid, contract_condition_id, context=context).content}}
    
    _columns = {
        'contract_condition_id' : fields.many2one('contract.condition','Contract Condition'),
    }
#end of account_voucher()