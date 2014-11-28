# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"

    _columns = {
        'fal_parent_company' : fields.many2one('res.partner','Parent Company'),
        'voucher_ids': fields.one2many('account.voucher', 'partner_id', 'Voucher', readonly=True),
        'purchase_order_ids': fields.one2many('purchase.order','partner_id','Purchase Order')
    }

#end of res_partner()