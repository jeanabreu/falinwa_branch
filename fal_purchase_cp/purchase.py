# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    
    _columns = {
        'fal_partner_contact_person_id' : fields.many2one('res.partner', 'Contact Person'),
        'fal_user_id' : fields.many2one('res.users', 'Purchasesperson', select=True, track_visibility='onchange'),
    }
    
    _defaults = {
        'fal_user_id': lambda obj, cr, uid, context: uid,
    }
    
    def onchange_partner_id(self, cr, uid, ids, partner_id):
        res = super(purchase_order, self).onchange_partner_id(cr, uid, ids, partner_id)
        partner = self.pool.get('res.partner').browse(cr, uid, partner_id)
        res['value']['fal_partner_contact_person_id'] = partner.child_ids and partner.child_ids[0].id or False
        print res
        return res
        
#end of purchase_order()