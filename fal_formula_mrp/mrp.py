# -*- coding: utf-8 -*-
import time
from datetime import datetime

import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, orm
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools import float_compare
from openerp.tools.translate import _
from openerp import netsvc
from openerp import tools
from openerp import SUPERUSER_ID
from openerp.addons.product import _common

class mrp_production(osv.Model):
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
                bom_id = bom_obj._bom_find(cr, uid, production.product_id.id, production.product_uom.id, properties)
                if bom_id:
                    bom_point = bom_obj.browse(cr, uid, bom_id)
                    routing_id = bom_point.routing_id.id or False
                    self.write(cr, uid, [production.id], {'bom_id': bom_id, 'routing_id': routing_id})
    
            if not bom_id:
                raise osv.except_osv(_('Error!'), _("Cannot find a bill of material for this product."))
    
            # get components and workcenter_lines from BoM structure
            factor = uom_obj._compute_qty(cr, uid, production.product_uom.id, production.product_qty, bom_point.product_uom.id)            
            res = bom_obj._bom_explode(cr, uid, bom_point, factor / bom_point.product_qty, properties, routing_id=production.routing_id.id)            
            
            results = res[0] # product_lines
            results2 = res[1] # workcenter_lines
            
            #modify start here
            stroke = production.sale_order_line_formula_id and production.sale_order_line_formula_id.fal_stroke or 0.00
            for r1 in results:
                if r1.get('product_id',False):
                    product_id = product_obj.browse(cr, uid, r1.get('product_id',False), context)
                    if product_id.categ_id.isfal_formula:
                        #print r1['product_qty']
                        #print stroke
                        extra_length = product_id.fal_formula_parameter1
                        saw_thickness = product_id.fal_formula_parameter2
                        if not product_id.fal_formula_parameter1:
                            extra_length = product_id.categ_id.fal_formula_parameter_categ1
                        if not product_id.fal_formula_parameter2:
                            saw_thickness = product_id.categ_id.fal_formula_parameter_categ2
                        r1['product_qty'] = r1['product_qty'] * ( stroke + product_id.fal_formula_parameter0 + extra_length + saw_thickness ) or r1['product_qty']
            #end here
            #note: should workcenter be formulized too?
            #print results
            #print '======================================================================================='
            #print results2
            
            # reset product_lines in production order
            for line in results:
                line['production_id'] = production.id
                prod_line_obj.create(cr, uid, line)
    
            #reset workcenter_lines in production order
            for line in results2:
                line['production_id'] = production.id
                workcenter_line_obj.create(cr, uid, line)
        return results
        
    #overide real openerp method
    def _make_production_line_procurement(self, cr, uid, production_line, shipment_move_id, context=None):
        wf_service = netsvc.LocalService("workflow")
        procurement_order = self.pool.get('procurement.order')
        production = production_line.production_id
        location_id = production.location_src_id.id
        date_planned = production.date_planned
        procurement_name = (production.origin or '').split(':')[0] + ':' + production.name
        procurement_id = procurement_order.create(cr, uid, {
                    #modify start here
                    'sale_order_line_formula_id' : production.sale_order_line_formula_id.id,
                    #end here
                    'name': procurement_name,
                    'origin': procurement_name,
                    'date_planned': date_planned,
                    'product_id': production_line.product_id.id,
                    'product_qty': production_line.product_qty,
                    'product_uom': production_line.product_uom.id,
                    'product_uos_qty': production_line.product_uos and production_line.product_qty or False,
                    'product_uos': production_line.product_uos and production_line.product_uos.id or False,
                    'location_id': location_id,
                    'procure_method': production_line.product_id.procure_method,
                    'move_id': shipment_move_id,
                    'company_id': production.company_id.id,
                })
        self._hook_create_post_procurement(cr, uid, production, procurement_id, context=context)
        wf_service.trg_validate(uid, procurement_order._name, procurement_id, 'button_confirm', cr)
        return procurement_id
        
mrp_production()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
