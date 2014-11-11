from openerp import tools
from openerp.osv import fields, osv
from openerp.tools.translate import _

class res_partner(osv.osv):
    _name = "res.partner"
    _inherit = "res.partner"
    _columns = {
        'is_final_customer' : fields.boolean('Final Customer')
    }
res_partner()