from openerp import tools
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
        'is_final_customer' : fields.boolean('Final Customer')
    }
#end of res_partner()