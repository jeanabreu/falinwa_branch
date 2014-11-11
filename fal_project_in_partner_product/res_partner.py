# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'fal_project_id' : fields.many2one('account.analytic.account','Project Number'),
    }
    
#end of res_partner()