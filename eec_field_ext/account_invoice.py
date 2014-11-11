from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class account_invoice(orm.Model):
    _name = "account.invoice"
    _inherit = "account.invoice"
        
    _columns = {
        'origin' : fields.char('Source Document', size=256, help="Reference of the document that produced this invoice.", readonly=True, states={'draft':[('readonly',False)]}),
    }

#end of account_invoice()

class account_bank_statement_line(orm.Model):
    _name = 'account.bank.statement.line'
    _inherit = 'account.bank.statement.line'
    _columns = {
        'is_fapiao_exists': fields.boolean('Fapiao Exists'),
    }
#end of account_bank_statement_line()