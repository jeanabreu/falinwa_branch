# -*- encoding: utf-8 -*-
import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, orm
import openerp.addons.decimal_precision as dp
from openerp.tools.translate import _

class account_analytic_line(orm.Model):
    _name = 'account.analytic.line'
    _inherit = 'account.analytic.line'

    _columns = {
        'fal_invoice_partner_id' : fields.related('invoice_id','partner_id', type='many2one', relation='res.partner', string='Partner', store=True, readonly=True), 
    }
    
#end of account_analytic_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
