# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    _sql_constraints = [
        ('ref_uniq', 'unique(ref)', 'Reference must be unique!'),
    ]

#end of res_partner()