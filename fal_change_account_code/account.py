from openerp import fields, models, api
from openerp.tools.translate import _

class account_account(models.Model):
    _name = "account.account"
    _inherit = "account.account"
    
    
    @api.multi
    def _check_allow_code_change(self):
        res = True
        if not res:
            res = super(account_account, self)._check_allow_code_change()
        return res
    
#end of account_account()