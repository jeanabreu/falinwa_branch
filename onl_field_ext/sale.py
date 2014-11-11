# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"

    _columns = {
        'x_quotationversioning' : fields.char('Final Quotation Number', size=512),
        'project_id': fields.many2one('account.analytic.account', 'Project Number', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}, help="The analytic account related to a sales order."),
    }

    def _prepare_invoice(self, cr, uid, order, lines, context=None):
        res = super(sale_order, self)._prepare_invoice(cr, uid, order, lines, context)
        res['final_quotation_number'] = order and order.x_quotationversioning or order.quotation_number or order.name
        return res

#end of sale_order()