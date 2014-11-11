# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    def _get_partner(self, cr, uid, ids, context=None):
        result = {}
        for partner in self.pool.get('res.partner').browse(cr, uid, ids, context):
            for order_id in partner.sale_order_ids:
                result[order_id.id] = True
        return result.keys()

    _columns = {
        'commercial_partner_id': fields.related('partner_id', 'commercial_partner_id', string='Commercial Entity', type='many2one',
                                                relation='res.partner', store=True, readonly=True,
                                                help="The commercial entity that will be used on Journal Entries for this invoice"),
        'fal_parent_company' : fields.related('partner_id', 'fal_parent_company', string='Parent Company', type='many2one',
                                                relation='res.partner', 
                                                store={
                                                    'res.partner' : (_get_partner,['fal_parent_company'],20),
                                                }, readonly=True,
                                                help="The Parent Company for group"),
    }

#end of sale_order()