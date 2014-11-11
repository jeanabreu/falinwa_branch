from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_voucher(orm.Model):
    _name = "account.voucher"
    _inherit = "account.voucher"
    
    def _amount_all_hkd(self, cr, uid, ids, field_name, arg, context=None):
        cur_obj = self.pool.get('res.currency')
        res = {}
        ctx = context.copy()
        for voucher in self.browse(cr, uid, ids, context=context):
            ctx.update({'date': voucher.date})
            rate_ids = cur_obj.search(cr, uid,[('symbol', '=', 'HK$'),('company_id','=',voucher.company_id.id)] , context=ctx, limit=1)
            temp = voucher.amount
            cur = voucher.currency_id
            for rate_id in cur_obj.browse(cr, uid, rate_ids, ctx):
                if cur != rate_id:
                    temp = cur_obj.compute(cr, uid, cur.id, rate_id.id, temp, context=ctx)
            res[voucher.id] = cur_obj.round(cr, uid, cur, temp)
        return res

    _columns = {
        'amount_total_hkd': fields.function(_amount_all_hkd, digits_compute=dp.get_precision('Account'), string='Total (HKD)',
            store=True, help="The total amount in HKD."),
    }

#end of account_voucher()