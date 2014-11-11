# -*- coding: utf-8 -*-

from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'invoice_reminder' : fields.boolean('Invoice Reminder')
    }

    _defaults = {
        'invoice_reminder': 1,
    }
#end of res_partner()