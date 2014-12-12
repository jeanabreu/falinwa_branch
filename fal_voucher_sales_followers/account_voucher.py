from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = 'account.voucher'
    _inherit = 'account.voucher'
   
    def create(self, cr, uid, vals, context=None):
        res = super(account_voucher, self).create(cr, uid, vals, context=context)
        if vals.get('partner_id', False):  
            partner = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'])
            if partner.user_id and partner.user_id.partner_id and partner.user_id.partner_id.id:
                self.message_subscribe(cr, uid, [res], [partner.user_id.partner_id.id], context=context)
        return res
   
#end of account_voucher()