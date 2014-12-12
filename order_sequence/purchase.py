# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class purchase_order(orm.Model):
    _name = "purchase.order"
    _inherit = "purchase.order"
    _order = "id desc"
    
    _columns = {
        'quotation_number' : fields.char('Quotation Number', size=64,
            readonly=True, select=True),
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(purchase_order, self).create(cr, uid, vals, context=context)
        if vals.get('quotation_number',False)==False:
            vals['quotation_number'] = vals.get('name','/')
        self.write(cr,uid,res,{'quotation_number':vals['quotation_number']})
        return res 
        
    def wkf_confirm_order(self, cr, uid, ids, context=None):
        purchase_id = self.browse(cr,uid,ids)[0]
        order_number = self.pool.get('ir.sequence').get(cr, uid, 'purchase.order.fwa') or '/'
        self.write(cr,uid,ids,{
            'name': order_number,
            'quotation_number' : purchase_id.name,
        })
        return super(purchase_order, self).wkf_confirm_order(cr, uid, ids, context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'name': '/',
            'quotation_number': False
        })
        return super(purchase_order, self).copy(cr, uid, id, default, context)
        
#end of purchase_order()