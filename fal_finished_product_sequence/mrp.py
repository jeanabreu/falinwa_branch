# -*- coding: utf-8 -*-
from openerp.osv import fields, orm

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    _columns = {
        'fal_of_number' : fields.char('OF Number',size=64,help="Sequence for Finished Product"),
        'fal_parent_mo_id' : fields.many2one('mrp.production', 'Parent MO'),
        'fal_mo_line_ids' : fields.one2many('mrp.production', 'fal_parent_mo_id', 'Manufacture Order Lines'),
    }
    
    def action_confirm(self, cr, uid, ids, context=None):
        for production in self.browse(cr, uid, ids,context=context):
            if production.product_id.categ_id.isfal_finished_product and not production.fal_of_number:
                finished_product_number = self.pool.get('ir.sequence').get(cr, uid, 'finished.product.fwa') or '/'
                self.write(cr, uid, [production.id], {'fal_of_number': finished_product_number}, context=context)
        return super(mrp_production, self).action_confirm(cr, uid, ids, context=context)
    
    def copy(self, cr, uid, id, default=None, context=None):
        default = default or {}
        default.update({
            'fal_mo_line_ids':[],
        })        
        return super(mrp_production, self).copy(cr, uid, id, default, context)
    
#end of mrp_production()

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def _prepare_procurement_from_move(self, cr, uid, move, context=None):
        res = super(stock_move, self)._prepare_procurement_from_move(cr, uid, move, context)

        res['fal_of_number'] = move.raw_material_production_id.fal_of_number
        res['fal_parent_mo_id'] = move.raw_material_production_id.id
        return res
        
#end of stock_move

class product_category(orm.Model):
    _name = "product.category"
    _inherit = "product.category"
    
    _columns = {
        'isfal_finished_product' : fields.boolean('Finished Product'),
    }
#end of product_category()

class procurement_order(orm.Model):
    _name = 'procurement.order'
    _inherit = 'procurement.order'
    _columns = {
        'fal_of_number' : fields.char('OF Number',size=64,help="Sequence for Finished Product"),
        'fal_parent_mo_id': fields.many2one('mrp.production', 'Parent Manufacturing Order'),
    }
    
    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        res = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context)
        res['fal_of_number'] =  procurement.fal_of_number
        res['fal_parent_mo_id'] =  procurement.fal_parent_mo_id.id
        return res
    
    """    
    def make_mo(self, cr, uid, ids, context=None):
        mrp_obj = self.pool.get('mrp.production')
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        for po in self.browse(cr, uid, ids):
            if po.fal_of_number and po.fal_parent_mo_id.id:
                mrp_obj.write(cr, uid, res[po.id], {'fal_of_number': po.fal_of_number, 'fal_parent_mo_id': po.fal_parent_mo_id.id})
        return res
    """    
#end of procurement_order()