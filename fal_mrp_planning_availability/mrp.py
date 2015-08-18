# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import SUPERUSER_ID
from openerp import workflow

class mrp_production(models.Model):
    _name = 'mrp.production'
    _inherit = 'mrp.production'
    
    @api.one
    @api.depends('move_lines')
    def _fal_moves_check_stock(self):
        is_ready = True
        for move_line in self.move_lines:
            if move_line.state != 'assigned':
                if  move_line.product_qty > move_line.availability:
                    is_ready = False
        self.fal_component_ready = is_ready
    
    #field start here    
    state = fields.Selection(selection_add=[
                ('Component Ready','Component Ready'),
                ])
    fal_floating_production_date = fields.Date("Floating Production Date", readonly=True, states=dict.fromkeys(['draft', 'confirmed'], [('readonly', False)]), copy=False)
    fal_fixed_production_date = fields.Date("Fixed Production Date", readonly=True, states=dict.fromkeys(['draft', 'confirmed', 'Component Ready'], [('readonly', False)]), copy=False)
    fal_component_ready = fields.Boolean(compute='_fal_moves_check_stock', string='Component Ready')
    #end here

    @api.multi
    def action_assign(self):
        for production in self:
            if production.fal_component_ready and production.fal_floating_production_date:
                production.write({
                    'state': 'Component Ready',
                    })
            elif not production.fal_component_ready and production.fal_floating_production_date:
                production.write({
                    'state': 'confirmed'
                    })
        super(mrp_production, self).action_assign()

    @api.multi
    def _production_fixed(self):
        for mrp_id in self:
            if mrp_id.fal_floating_production_date:
                mrp_id.write({'fal_fixed_production_date': mrp_id.fal_floating_production_date})
        return True

    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        result = super(mrp_production, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if toolbar:
            toclean = ('report_sxw_content', 'report_rml_content', 'report_sxw', 'report_rml', 'report_sxw_content_data', 'report_rml_content_data')
            def clean(x):
                x = x[2]
                for key in toclean:
                    x.pop(key, None)
                return x
            ir_values_obj = self.pool.get('ir.values')
            resaction = ir_values_obj.get(cr, uid, 'action', 'client_action_multi', [(self._name, False)], False, context)
            resaction = [clean(action) for action in resaction if view_type in ['tree','calendar'] or not action[2].get('multi')]
            result['toolbar']['action'] = resaction
        return result
        
#end of mrp_production()

class stock_move(models.Model):
    _name = "stock.move"
    _inherit = "stock.move"
    
    @api.multi
    def action_assign(self):
        #check the stock for floating
        floating_ready_self = floating_ready_self = self.filtered('raw_material_production_id.fal_floating_production_date' and r.raw_material_production_id.fal_fixed_production_date == False and r.raw_material_production_id.state == 'confirmed' and r.raw_material_production_id.fal_component_ready)
        print floating_ready_self
        for move_ready in floating_ready_self:
            move_ready.raw_material_production_id.write({
                'state': 'Component Ready'
            })
        floating_notready_self = self.filtered(lambda r: r.raw_material_production_id.state == 'Component Ready' and r.raw_material_production_id.fal_component_ready == False)
        for move_not_ready in floating_notready_self:
            move_not_ready.raw_material_production_id.write({
                'state': 'confirmed'
            })
        print floating_notready_self
        new_self = self.filtered(lambda r: r.procure_method == 'make_to_order' or r.raw_material_production_id == False or r.raw_material_production_id.fal_fixed_production_date and r.raw_material_production_id.state in ['confirmed', 'Component Ready']).sorted(key=lambda r: r.raw_material_production_id.fal_fixed_production_date)
        for rec in new_self:        
            if rec.raw_material_production_id:
                print str(rec.raw_material_production_id) + ':' + rec.raw_material_production_id.name
        super(stock_move, new_self).action_assign()

    @api.multi
    def write(self, vals):
        res = super(stock_move, self).write(vals)
        if vals.get('state') == 'assigned':
            orders = list(set([x.raw_material_production_id for x in self if x.raw_material_production_id and x.raw_material_production_id.state == 'Component Ready']))
            for order_id in orders:
                if order_id.test_ready():
                    workflow.trg_validate(self.env.uid, 'mrp.production', order_id.id, 'moves_ready', self.env.cr)
        return res
        
#end of stock_move()