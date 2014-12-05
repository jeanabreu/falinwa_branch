# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _defaults = {
        'company_id' : False,
    }

#end of res_partner()