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
    
    def _make_production_line_procurement(self, cr, uid, production_line, shipment_move_id, context=None):
        res = super(mrp_production,self)._make_production_line_procurement(cr, uid, production_line, shipment_move_id, context)
        procurement_order_obj = self.pool.get('procurement.order')
        procurement_order_obj.write(cr, uid, [res], {
            'fal_of_number' : production_line.production_id.fal_of_number,
            'fal_parent_mo_id' : production_line.production_id.id,
        })
        return res
        
#end of mrp_production()

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
    
    def _mo_prepare_val(self, cr, uid, procurement, res_id, newdate, context=None):
        res = super(procurement_order, self)._mo_prepare_val(cr, uid, procurement, res_id, newdate, context)
        res['fal_of_number'] =  procurement.fal_of_number
        res['fal_parent_mo_id'] =  procurement.fal_parent_mo_id.id
        return res
        
    def make_mo(self, cr, uid, ids, context=None):
        mrp_obj = self.pool.get('mrp.production')
        res = super(procurement_order, self).make_mo(cr, uid, ids, context)
        for po in self.browse(cr, uid, ids):
            if po.fal_of_number and po.fal_parent_mo_id.id:
                mrp_obj.write(cr, uid, res[po.id], {'fal_of_number': po.fal_of_number, 'fal_parent_mo_id': po.fal_parent_mo_id.id})
        return res
        
#end of procurement_order()