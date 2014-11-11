# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp import pooler
from openerp.tools.translate import _

class purchase_config_settings(orm.TransientModel):
    _name = 'purchase.config.settings'
    _inherit = 'purchase.config.settings'

    _columns = {
        'default_invoice_method': fields.selection(
            [('manual', 'Based on purchase order lines'),
             ('picking', 'Based on receptions'),
             ('order', 'Pre-generate draft invoices based on purchase orders'),
             ('demand', 'On Demand'),
            ], 'Default invoicing control method', required=True, default_model='purchase.order'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
