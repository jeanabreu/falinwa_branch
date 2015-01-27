# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    
    def _check_ref_unique_insesitive(self, cr ,uid, ids, context=None):
        for partner in self.browse(cr, uid, ids, context=context):
            if partner.ref:
                ref_exist = self.search(cr ,uid ,[('ref', '=ilike', partner.ref)], context=context)
                if len(ref_exist) != 1:
                    return False
        return True
            
    _sql_constraints = [
        ('ref_uniq', 'unique(ref)', 'Reference must be unique!'),
    ]
    
    _constraints = [
        (_check_ref_unique_insesitive, 'Ref already exists', ['ref']),
    ]

#end of res_partner()