# -*- coding: utf-8 -*-
from openerp.osv import fields, orm, osv
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp import api

class sale_order(orm.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'
    
    _columns = {
        'client_order_ref': fields.char('Customer PO Number', size=64),
    }
        
    def _prepare_order_line_procurement(self, cr, uid, order, line, group_id=False, context=None):
        res = super(sale_order, self)._prepare_order_line_procurement(cr, uid, order, line, group_id=group_id, context=context)
        res['fal_remark'] = line.fal_remark
        res['fal_client_order_ref'] = order.client_order_ref
        return res
    
#end of sale_order()

class sale_order_line(orm.Model):
    _name = 'sale.order.line'
    _inherit = 'sale.order.line'
    
    def compute_unit_price_after_discount(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}

        res = {}        
        if not ids:
            return res
        for order_line in self.browse(cr, uid, ids, context=context):
            res[order_line.id] = float(order_line.price_unit * (100.00 - order_line.discount) / 100.00)        
        return res
        
    _columns = {
        'unit_price_after_discount' : fields.function(compute_unit_price_after_discount, type='float',string='Unit Price (After Discount)',
            store={
                'sale.order.line' : (lambda self, cr, uid, ids, c={}: ids, None, 20),
            }
        ),
        'fal_full_reference' : fields.char('Full Reference',size=128),
        'fal_remark' : fields.char('Remark', size=64),
    }
        
#end of sale_order_line()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'
        
    _columns = {
        'fal_remark' : fields.char('Remark', size=64),
        'fal_client_order_ref': fields.char('Customer PO Number', size=64),
    }
    
    def _run_move_create(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._run_move_create(cr, uid, procurement, context=context)
        res['fal_remark'] = procurement.fal_remark
        res['fal_client_order_ref'] = procurement.fal_client_order_ref
        return res
        
#end of procurement_order()

class fal_res_partner_category(orm.Model):

    def name_get(self, cr, uid, ids, context=None):
        """ Return the categories' display name, including their direct
            parent by default.

            If ``context['partner_category_display']`` is ``'short'``, the short
            version of the category name (without the direct parent) is used.
            The default is the long version.
        """
        if not isinstance(ids, list):
            ids = [ids]
        if context is None:
            context = {}

        if context.get('partner_category_display') == 'short':
            return super(res_partner_category, self).name_get(cr, uid, ids, context=context)

        res = []
        for category in self.browse(cr, uid, ids, context=context):
            names = []
            current = category
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((category.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        categories = self.search(args, limit=limit)
        return categories.name_get()

    @api.multi
    def _name_get_fnc(self, field_name, arg):
        return dict(self.name_get())

    _description = 'Customer Industrial Area'
    _name = 'fal.res.partner.category'
    _columns = {
        'name': fields.char('Category Name', required=True, translate=True),
        'parent_id': fields.many2one('res.partner.category', 'Parent Category', select=True, ondelete='cascade'),
        'complete_name': fields.function(_name_get_fnc, type="char", string='Full Name'),
        'child_ids': fields.one2many('res.partner.category', 'parent_id', 'Child Categories'),
        'active': fields.boolean('Active', help="The active field allows you to hide the category without removing it."),
        'parent_left': fields.integer('Left parent', select=True),
        'parent_right': fields.integer('Right parent', select=True),
        'partner_ids': fields.many2many('res.partner', id1='category_id', id2='partner_id', string='Partners'),
    }
    _constraints = [
        (osv.osv._check_recursion, 'Error ! You can not create recursive categories.', ['parent_id'])
    ]
    _defaults = {
        'active': 1,
    }
    _parent_store = True
    _parent_order = 'name'
    _order = 'parent_left'
    
#end of fal_res_partner_category()

class res_partner(orm.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
        
    _columns = {
        'fal_category_id': fields.many2many('fal.res.partner.category', id1='partner_id', id2='category_id', string='Customer Industrial Area'),
    }
    
        
#end of res_partner()    