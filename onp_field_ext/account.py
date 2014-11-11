# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = 'account.invoice'
    _inherit = 'account.invoice'
    _columns = {
        'fal_risk_level'  : fields.integer('Risk Level', size= 1, help="Risk Level Code define in number 1 - 9"),
        'fal_risk_level_name'  : fields.char('Risk Level Name', size= 64, help="Risk Level Name"),
    }
#end of account_invoice()