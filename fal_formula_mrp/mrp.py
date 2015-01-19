# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production(orm.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'

    _columns = {
        'sale_order_line_formula_id': fields.many2one('sale.order.line','Sale Order Line for MRP Formula'),        
    }
    
    #overide real openerp method
    def _action_compute_lines(self, cr, uid, ids, properties=None, context=None):
        """ Compute product_lines and workcenter_lines from BoM structure
        @return: product_lines
        """
        if properties is None:
            properties = []
        results = []
        bom_obj = self.pool.get('mrp.bom')
        uom_obj = self.pool.get('product.uom')
        prod_line_obj = self.pool.get('mrp.production.product.line')
        workcenter_line_obj = self.pool.get('mrp.production.workcenter.line')
        product_obj = self.pool.get('product.product')
        for production in self.browse(cr, uid, ids, context=context):
            #unlink product_lines
            prod_line_obj.unlink(cr, SUPERUSER_ID, [line.id for line in production.product_lines], context=context)
            #unlink workcenter_lines
            workcenter_line_obj.unlink(cr, SUPERUSER_ID, [line.id for line in production.workcenter_lines], context=context)
            # search BoM structure and route
            bom_point = production.bom_id
            bom_id = production.bom_id.id
            if not bom_point:
                bom_id = bom_obj._bom_find(cr, uid, product_id=production.product_id.id, properties=properties, context=context)
                if bom_id:
                    bom_point = bom_obj.browse(cr, uid, bom_id)
                    routing_id = bom_point.routing_id.id or False
                    self.write(cr, uid, [production.id], {'bom_id': bom_id, 'routing_id': routing_id})
    
            if not bom_id:
                raise osv.except_osv(_('Error!'), _("Cannot find a bill of material for this product."))

            # get components and workcenter_lines from BoM structure
            factor = uom_obj._compute_qty(cr, uid, production.product_uom.id, production.product_qty, bom_point.product_uom.id)
            # product_lines, workcenter_lines
            results, results2 = bom_obj._bom_explode(cr, uid, bom_point, production.product_id, factor / bom_point.product_qty, properties, routing_id=production.routing_id.id, context=context)

            #modify start here
            #results is product_line
            #results2 is workcenter_line
            stroke = production.fal_stroke
            for r1 in results:
                if r1.get('product_id',False):
                    product_id = product_obj.browse(cr, uid, r1.get('product_id',False), context)
                    if production.product_id.categ_id.isfal_formula:
                        extra_length = production.product_id.fal_formula_parameter1
                        saw_thickness = production.product_id.fal_formula_parameter2
                        number_cut = 1
                        if production.product_qty > 1:
                            number_cut = production.product_qty - 1
                        else:
                            number_cut = 1
                        if not production.product_id.fal_formula_parameter1:
                            extra_length = production.product_id.categ_id.fal_formula_parameter_categ1
                        if not production.product_id.fal_formula_parameter2:
                            saw_thickness = production.product_id.categ_id.fal_formula_parameter_categ2
                        r1['product_qty'] = ((production.product_qty * (stroke + production.product_id.fal_formula_parameter0 + extra_length)) + (saw_thickness * number_cut)) or r1['product_qty']
            #end here
            
            
            # reset product_lines in production order
            for line in results:
                line['production_id'] = production.id
                prod_line_obj.create(cr, uid, line)

            #reset workcenter_lines in production order
            for line in results2:
                #modify start here
                if line.get('fal_is_manufacture',False):
                    operation_id = operation_obj.browse(cr, uid, line['fal_operation_id'])
                    wc = operation_id.workcenter_id
                    d, m = divmod(factor, operation_id.workcenter_id.capacity_per_cycle)
                    mult = (d + (m and 1.0 or 0.0))
                    line['cycle'] = production.product_qty * (mult * (operation_id.fal_minimum_cycle_time + stroke * operation_id.fal_stroke_cycle_time_ref))
                    line['hour'] = float(operation_id.hour_nbr*mult + (line['cycle']*(wc.time_cycle or 0.0)) * (wc.time_efficiency or 1.0))
                #end here
                line['production_id'] = production.id
                workcenter_line_obj.create(cr, uid, line)
        return results
        
        
#end of mrp_production()

class stock_move(orm.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    def _prepare_procurement_from_move(self, cr, uid, move, context=None):
        res = super(stock_move, self)._prepare_procurement_from_move(cr, uid, move, context)
        res['sale_order_line_formula_id'] = move.raw_material_production_id.sale_order_line_formula_id.id
        res['fal_stroke'] = move.raw_material_production_id.fal_stroke
        return res
        
#end of stock_move

class mrp_bom(orm.Model):
    _name = 'mrp.bom'
    _inherit = 'mrp.bom'
    
    def _get_product_dima(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids, context=context):
            res[bom.id] = bom.product_id.fal_formula_parameter0
        return res
        
    def _get_extra_length(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids, context=context):
            res[bom.id] = bom.product_id.fal_formula_parameter1 or bom.product_id.categ_id.fal_formula_parameter_categ1
        return res
        
    def _get_saw_thickness(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom in self.browse(cr, uid, ids, context=context):
            res[bom.id] = bom.product_id.fal_formula_parameter2 or bom.product_id.categ_id.fal_formula_parameter_categ2
        return res
    
    _columns = {
        'fal_product_dima' : fields.function(_get_product_dima, string="DimA", type="float", store=False),
        'fal_product_extra_length' : fields.function(_get_extra_length, string="Extra Length", type="float", store=False),
        'fal_product_saw_thickness' : fields.function(_get_saw_thickness, string="Saw Thickness", type="float", store=False),
    }
    
#end of mrp_bom()

class mrp_bom_line(orm.Model):
    _name = 'mrp.bom.line'
    _inherit = 'mrp.bom.line'

    def _get_product_dima(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom_line in self.browse(cr, uid, ids, context=context):
            res[bom_line.id] = bom_line.product_id.fal_formula_parameter0
        return res
        
    def _get_extra_length(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom_line in self.browse(cr, uid, ids, context=context):
            res[bom_line.id] = bom_line.product_id.fal_formula_parameter1 or bom_line.product_id.categ_id.fal_formula_parameter_categ1
        return res
        
    def _get_saw_thickness(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for bom_line in self.browse(cr, uid, ids, context=context):
            res[bom_line.id] = bom_line.product_id.fal_formula_parameter2 or bom_line.product_id.categ_id.fal_formula_parameter_categ2
        return res
        
    _columns = {
        'fal_product_dima' : fields.function(_get_product_dima, string="DimA", type="float", store=False),
        'fal_product_extra_length' : fields.function(_get_extra_length, string="Extra Length", type="float", store=False),
        'fal_product_saw_thickness' : fields.function(_get_saw_thickness, string="Saw Thickness", type="float", store=False),
    }    
    
 #end of mrp_bom_line()  
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
