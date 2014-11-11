from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class contract_condition_falinwa(orm.Model):
    _name = "contract.condition"
    
    _columns = {
        'name' : fields.char('Name',size=64, select=True, required=True),
        'content' : fields.text('Content', select=True, required=True),
    }

#end of contract_condition_falinwa()