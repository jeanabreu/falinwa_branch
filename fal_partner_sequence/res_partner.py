# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _

class res_partner(orm.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    
    def create(self, cr, uid, vals, context=None):
        if not vals.get('ref', False):
            if vals.get('is_company',False):
                if vals.get('customer',False):
                    vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'customer.code.fwa') or '/'
                elif vals.get('supplier',False):
                    vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'supplier.code.fwa') or '/'
                else:
                    vals['ref'] = self.pool.get('ir.sequence').get(cr, uid, 'sc.code.fwa') or '/'
        return super(res_partner, self).create(cr, uid, vals, context=context)
        
#end of res_partner()