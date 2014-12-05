from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"

    _columns = {
        'final_quotation_number' : fields.char('Final Quotation Number',size=64),
    }

#end of account_invoice()