# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _columns = {
        'fal_project_id' : fields.property(
            type='many2one',
            relation='account.analytic.account',
            string='Project', 
            view_load=True,
            ondelete='set null'),
    }
    
#end of res_partner()