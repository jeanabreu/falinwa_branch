# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class sale_order(orm.Model):
    _name = "sale.order"
    _inherit = "sale.order"
    _order = "id desc"
    
    _columns = {
        'quotation_number' : fields.char('Quotation Number', size=64,
            readonly=True, select=True),
    }
    
    def create(self, cr, uid, vals, context=None):
        res = super(sale_order, self).create(cr, uid, vals, context=context)
        if vals.get('quotation_number',False) == False :
            vals['quotation_number'] = vals.get('name','/')
        self.write(cr,uid,res,{'quotation_number':vals['quotation_number']})
        return res 
    
    def action_button_confirm(self, cr, uid, ids, context=None):
        for sale_id in self.browse(cr, uid, ids):
            order_number = self.pool.get('ir.sequence').get(cr, uid, 'sale.order.fwa') or '/'
            self.write(cr, uid, [sale_id.id], {
                'name': order_number,
                'quotation_number' : sale_id.name,
            })
        return super(sale_order, self).action_button_confirm(cr, uid, ids, context)

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default.update({
            'name': '/',
            'quotation_number': False
        })
        return super(sale_order, self).copy(cr, uid, id, default, context)
        
#end of sale_order()