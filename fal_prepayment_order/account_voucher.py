from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import netsvc


class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
    
    _columns = {
        'fal_sale_id' : fields.many2one('sale.order', 'Sale Order', ondelete="cascade"),
    }

    def button_pay_prepayment(self, cr, uid, ids, context=None):
        context = context or {}
        wf_service = netsvc.LocalService("workflow")
        self.write(cr, uid, ids, {'state' : 'validated'}, context)
        return {'type': 'ir.actions.act_window_close'}
        
#end of account_voucher()