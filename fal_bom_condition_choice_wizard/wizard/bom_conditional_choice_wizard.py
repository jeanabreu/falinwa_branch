# -*- coding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.exceptions import except_orm, Warning, RedirectWarning
import openerp.addons.decimal_precision as dp

class bom_conditional_choice_wizard(models.TransientModel):
    _name = "bom.conditional.choice.wizard"
    _description = "BOM Conditional of Choice Wizard"

    #fields start here    
    fal_serie_name_id = fields.Many2one('fal.serie.name','Serie Name')
    fal_serie_name_id_name = fields.Char(related='fal_serie_name_id.name', string="Serie Name", readonly=True)
    fal_serie_name_id_type = fields.Selection(related='fal_serie_name_id.type', string="Serie Name Type", readonly=True)
    fal_ordering_code_id = fields.Many2one('fal.ordering.code','Ordering Code', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_bore_diameter_id = fields.Many2one('fal.bore.diameter','Bore Diameter (mm)', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_rod_diameter_id = fields.Many2one('fal.rod.diameter','Rod Diameter (mm)', domain="[('fal_bore_list_ids','=',fal_bore_diameter_id)]")
    fal_main_option_id = fields.Many2one('fal.main.option','Main Option', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_main_option_code = fields.Char(related='fal_main_option_id.code', string="Main Option Code", readonly=True)
    fal_rod_end_id = fields.Many2one('fal.rod.end','Rod End', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_rod_end_option_id = fields.Many2one('fal.rod.end.option','Rod End Option')
    fal_seal_kit_id = fields.Many2one('fal.seal.kit','Seal Kit', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_mounting_id = fields.Many2one('fal.mounting','Mounting', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]")
    fal_mounting_id_code = fields.Char(related='fal_mounting_id.code', string="Main Option Code", readonly=True)
    fal_purge = fields.Boolean('Purge(PG)?')
    fal_brace_ring = fields.Boolean('Brace Ring?')
    fal_counter_bores = fields.Boolean('Counter Bores(LV)?')
    fal_for_handling = fields.Boolean('For Handling(TA)?')
    fal_microrupteur = fields.Boolean('Micro Rupteur?')
    fal_magnet_sensor = fields.Boolean('Magnet Sensor?')
    fal_xcma = fields.Boolean('XCMA 110?')
    fal_cote_x = fields.Integer('COTE X', required=True)
    fal_magnet_sensor_position_id = fields.Many2one('fal.magnet.position', 'Magnet Sensor Position')
    fal_seal_location = fields.Char('Seal Location', size=128)
    fal_full_reference = fields.Char('Full Reference',size=256)
    fal_sale_reference = fields.Char('Sale Reference', size=256)
    fal_ref_for_stroke_option = fields.Char('Ref For Stroke Option', size=128)
    fal_by_stroke_option = fields.Char('By Stroke Option', size=128)
    fal_bom_reference = fields.Char('BOM Reference',size=128)
    fal_ref_priced_option = fields.Char('Ref Priced Option',size=128)
    fal_ref_free_option = fields.Char('Ref Free Option',size=128)
    fal_standard_stroke_id = fields.Many2one('fal.standard.stroke', string='Standard Stroke(MM)')
    fal_piston_seal = fields.Selection([('D','D - Double acting seal'), ('P','P - Compound Seal')], string='Piston Seal')
    fal_rod_seal = fields.Selection([('J','J - Single lip seal'), ('P','P - Compound Seal')], string='Rod Seal')
    fal_ports = fields.Selection([('G','G - Internal Thread Gaz')], string='Ports')
    fal_position_ports_head = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Head')
    fal_position_ports_bottom = fields.Selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Bottom')
    fal_value_xv = fields.Float('Value for XV (for MT4?DT4 only)')
    fal_single_or_double_rod = fields.Char(related='fal_mounting_id.sr_or_dr',string='Single or Double Rod', readonly=True)
    fal_stroke = fields.Integer('Stroke (mm)')
    fal_special = fields.Boolean('Special')
    fal_y = fields.Float('Y')
    fal_w = fields.Float('W')
    fal_comment_for_vh = fields.Text('Comment')
    product_id = fields.Many2one('product.product', 'Finished Product', ondelete='restrict')
    fal_product_template_id = fields.Many2one(related='product_id.product_tmpl_id' , comodel_name='product.template', string='Finished Template Product', ondelete='restrict')
    fal_bom_id = fields.Many2one('mrp.bom', 'BoM', help="BoM of the product.")
    #end here

    @api.multi
    def onchange_product(self, product_id):
        res = {}
        bom_obj = self.env['mrp.bom']
        if product_id:
            product_template_id = self.env['product.product'].browse(product_id).product_tmpl_id
            bom_ids = bom_obj.search([('product_tmpl_id', '=', product_template_id.id)],limit=1)
            if bom_ids:
                res['value'] = { 'fal_bom_id':bom_ids[0].id}
        return res
        
    @api.model
    def get_by_stroke_option(self, ref, fal_stroke):                  

        return self.env['sale.order.line'].get_by_stroke_option(ref, fal_stroke)
        
    @api.multi
    def onchange_conditional(self, 
        fal_serie_name_id, fal_bore_diameter_id, fal_rod_diameter_id, fal_stroke, fal_main_option_id, fal_rod_end_id, fal_rod_end_option_id, fal_seal_kit_id, fal_mounting_id, 
        fal_purge, fal_counter_bores, fal_for_handling, fal_microrupteur, fal_magnet_sensor, fal_cote_x, fal_magnet_sensor_position_id, fal_seal_location, fal_ordering_code_id, 
        fal_standard_stroke_id, fal_piston_seal, fal_rod_seal, fal_ports, fal_brace_ring, fal_position_ports_head, fal_position_ports_bottom, fal_value_xv, flag=False):

        return self.env['sale.order.line'].onchange_conditional( 
        fal_serie_name_id, fal_bore_diameter_id, fal_rod_diameter_id, fal_stroke, fal_main_option_id, fal_rod_end_id, fal_rod_end_option_id, fal_seal_kit_id, fal_mounting_id, 
        fal_purge, fal_counter_bores, fal_for_handling, fal_microrupteur, fal_magnet_sensor, fal_cote_x, fal_magnet_sensor_position_id, fal_seal_location, fal_ordering_code_id, 
        fal_standard_stroke_id, fal_piston_seal, fal_rod_seal, fal_ports, fal_brace_ring, fal_position_ports_head, fal_position_ports_bottom, fal_value_xv, flag)

    @api.multi
    def onchange_bomref(self, fal_bom_reference):

        return self.env['sale.order.line'].onchange_bomref(fal_bom_reference)

    @api.multi
    def search_bom(self): 
        mrp_obj = self.env['mrp.production']
        product_obj = self.env['product.product']
        product_id = False
        if self.product_id.id:
            product_id = self.product_id.id
        else:
            raise except_orm(_("Warning!"), _("Please Provide the Information to search!"))
        
        if not self.fal_bom_id:
            raise except_orm(_("Warning!"), _("BoM doesnt exist!"))
        ctx = self.env.context.copy()
        ctx['fal_serie_name_id'] = self.fal_serie_name_id.id
        ctx['fal_ordering_code_id'] = self.fal_ordering_code_id.id
        ctx['fal_bore_diameter_id'] = self.fal_bore_diameter_id.id
        ctx['fal_rod_diameter_id'] = self.fal_rod_diameter_id.id
        ctx['fal_main_option_id'] = self.fal_main_option_id.id
        ctx['fal_rod_end_id'] = self.fal_rod_end_id.id
        ctx['fal_rod_end_option_id'] = self.fal_rod_end_option_id.id
        ctx['fal_seal_kit_id'] = self.fal_seal_kit_id.id
        ctx['fal_mounting_id'] = self.fal_mounting_id.id
        ctx['fal_purge'] = self.fal_purge
        ctx['fal_brace_ring'] = self.fal_brace_ring
        ctx['fal_counter_bores'] = self.fal_counter_bores
        ctx['fal_for_handling'] = self.fal_for_handling
        ctx['fal_microrupteur'] = self.fal_microrupteur
        ctx['fal_magnet_sensor'] = self.fal_magnet_sensor
        ctx['fal_xcma'] = self.fal_xcma
        ctx['fal_cote_x'] = self.fal_cote_x
        ctx['fal_magnet_sensor_position_id'] = self.fal_magnet_sensor_position_id.id
        ctx['fal_seal_location'] = self.fal_seal_location
        ctx['fal_full_reference'] = self.fal_full_reference
        ctx['fal_sale_reference'] = self.fal_sale_reference
        ctx['fal_ref_for_stroke_option'] = self.fal_ref_for_stroke_option
        ctx['fal_by_stroke_option'] = self.fal_by_stroke_option
        ctx['fal_bom_reference'] = self.fal_bom_reference
        ctx['fal_ref_priced_option'] = self.fal_ref_priced_option
        ctx['fal_ref_free_option'] = self.fal_ref_free_option
        ctx['fal_by_stroke_option'] = self.fal_by_stroke_option
        ctx['fal_stroke'] = self.fal_stroke
        ctx['fal_standard_stroke_id'] = self.fal_standard_stroke_id.id
        ctx['fal_piston_seal'] = self.fal_piston_seal
        ctx['fal_rod_seal'] = self.fal_rod_seal
        ctx['fal_ports'] = self.fal_ports
        ctx['fal_position_ports_head'] = self.fal_position_ports_head
        ctx['fal_position_ports_bottom'] = self.fal_position_ports_bottom
        ctx['fal_value_xv'] = self.fal_value_xv
        ctx['fal_special'] = self.fal_special
        ctx['fal_y'] = self.fal_y
        ctx['fal_w'] = self.fal_w
        ctx['fal_comment_for_vh'] = self.fal_comment_for_vh
        return {
            'type': 'ir.actions.act_window',
            'name': self.product_id.name,
            'res_model': 'mrp.bom.line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'view_id': self.env['ir.model.data'].get_object_reference('mrp', 'mrp_bom_tree_view')[1],
            'domain' : '[("bom_id","=",'+str(self.fal_bom_id.id)+')]',
            'target': 'new',
            'context': ctx,
             }
             
#end of bom_reader_wizard()

class bom_create_record_wizard(models.TransientModel):
    _name = "bom.create.record.wizard"
    _description = "BOM Create Record Wizard"

    @api.model
    def _default_product_id(self):
        bom_line_obj = self.env['mrp.bom.line']
        product_id = bom_line_obj.browse(self.env.context['active_id']).product_id.id
        return product_id

    @api.model
    def _default_product_uom_id(self):
        bom_line_obj = self.env['mrp.bom.line']
        uom_id = bom_line_obj.browse(self.env.context['active_id']).product_id.uom_id.id
        return uom_id
        
    fal_product_id = fields.Many2one('product.product', 'Finished Product', default=_default_product_id, ondelete='restrict', required=1)
    fal_qty = fields.Float('Qty', digits_compute=dp.get_precision('Product Unit of Measure'), default=1)
    fal_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure', required=True, default=_default_product_uom_id)
    fal_type = fields.Selection([('sale.order','Sale Order'),('mrp.production','Manufacture order'),('mrp.repair','Repair Order')], 'Type', required=1)
    fal_partner_id = fields.Many2one('res.partner', 'Customer')
    fal_existed_quotation = fields.Many2one('sale.order', 'Existing Quotation', domain="[('state','=','draft'), ('partner_id','=',fal_partner_id)]") 

    @api.multi
    def make_record(self):
        last_wizard_id = False
        temp_val = {}
        temp_val['fal_serie_name_id'] = self.env.context.get('fal_serie_name_id', False)
        temp_val['fal_ordering_code_id'] = self.env.context.get('fal_ordering_code_id', False)
        temp_val['fal_bore_diameter_id'] = self.env.context.get('fal_bore_diameter_id', False)
        temp_val['fal_rod_diameter_id'] = self.env.context.get('fal_rod_diameter_id', False)
        temp_val['fal_main_option_id'] = self.env.context.get('fal_main_option_id', False)
        temp_val['fal_rod_end_id'] = self.env.context.get('fal_rod_end_id', False)
        temp_val['fal_rod_end_option_id'] = self.env.context.get('fal_rod_end_option_id', False)
        temp_val['fal_seal_kit_id'] = self.env.context.get('fal_seal_kit_id', False)
        temp_val['fal_mounting_id'] = self.env.context.get('fal_mounting_id', False)
        temp_val['fal_purge'] = self.env.context.get('fal_purge', False)
        temp_val['fal_brace_ring'] = self.env.context.get('fal_brace_ring', False)
        temp_val['fal_counter_bores'] = self.env.context.get('fal_counter_bores', False)
        temp_val['fal_for_handling'] = self.env.context.get('fal_for_handling', False)
        temp_val['fal_microrupteur'] = self.env.context.get('fal_microrupteur', False)
        temp_val['fal_magnet_sensor'] = self.env.context.get('fal_magnet_sensor', False)
        temp_val['fal_xcma'] = self.env.context.get('fal_xcma', False)
        temp_val['fal_cote_x'] = self.env.context.get('fal_cote_x', False)
        temp_val['fal_magnet_sensor_position_id'] = self.env.context.get('fal_magnet_sensor_position_id', False)
        temp_val['fal_seal_location'] = self.env.context.get('fal_seal_location', False)
        temp_val['fal_full_reference'] = self.env.context.get('fal_full_reference', False)
        temp_val['fal_sale_reference'] = self.env.context.get('fal_sale_reference', False)
        temp_val['fal_ref_for_stroke_option'] = self.env.context.get('fal_ref_for_stroke_option', False)
        temp_val['fal_by_stroke_option'] = self.env.context.get('fal_by_stroke_option', False)
        temp_val['fal_bom_reference'] = self.env.context.get('fal_bom_reference', False)
        temp_val['fal_ref_priced_option'] = self.env.context.get('fal_ref_priced_option', False)
        temp_val['fal_ref_free_option'] = self.env.context.get('fal_ref_free_option', False)
        temp_val['fal_by_stroke_option'] = self.env.context.get('fal_by_stroke_option', False)
        temp_val['fal_stroke'] = self.env.context.get('fal_stroke', False)
        temp_val['fal_standard_stroke_id'] = self.env.context.get('fal_standard_stroke_id', False)
        temp_val['fal_piston_seal'] = self.env.context.get('fal_piston_seal', False)
        temp_val['fal_rod_seal'] = self.env.context.get('fal_rod_seal', False)
        temp_val['fal_ports'] = self.env.context.get('fal_ports', False)
        temp_val['fal_position_ports_head'] = self.env.context.get('fal_position_ports_head', False)
        temp_val['fal_position_ports_bottom'] = self.env.context.get('fal_position_ports_bottom', False)
        temp_val['fal_value_xv'] = self.env.context.get('fal_value_xv', False)
        temp_val['fal_special'] = self.env.context.get('fal_special', False)
        temp_val['fal_y'] = self.env.context.get('fal_y', False)
        temp_val['fal_w'] = self.env.context.get('fal_w', False)
        temp_val['fal_comment_for_vh'] = self.env.context.get('fal_comment_for_vh', False)

        temp_val['product_id'] = self.fal_product_id.id
        temp_val['product_uom_qty'] = self.fal_qty
        temp_val['product_uom'] = self.fal_uom_id.id
        if self.fal_type == 'sale.order':
            sale_obj = self.env['sale.order']
            sale_line_obj = self.env['sale.order.line']

            temp_val['name'] = self.fal_product_id.description or self.fal_product_id.name
            
            if self.fal_existed_quotation:
                #merged existing quotation
                self.fal_existed_quotation.write({
                    'order_line': [(0 , False, temp_val)],
                })
                sale_id = self.fal_existed_quotation
            else:
                sale_id = sale_obj.create({
                    'partner_id' : self.fal_partner_id.id,
                    'order_line': [(0 , False, temp_val)],
                })
            return {
                'type': 'ir.actions.act_window',
                'name': _('Sale Order Form'),
                'res_model': 'sale.order',
                'view_type': 'form',
                'view_mode': 'form,tree',
                #'views': [(self.env['ir.model.data'].get_object_reference('sale', 'view_order_form')[1],'form')],
                'context': self.env.context,
                'nodestroy': True,
                'res_id': sale_id.id,
            }
        if self.fal_type == 'mrp.production':
            if not self.fal_product_id.bom_ids:
                raise except_orm(_('Error!'), _("Product Does not have BoM"))
            mrp_obj = self.env['mrp.production']
            temp_val['bom_id'] = self.fal_product_id.bom_ids[0].id
            mrp_id = mrp_obj.create(temp_val)
            return {
                'type': 'ir.actions.act_window',
                'name': _('MRP Form'),
                'res_model': 'mrp.production',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'context': self.env.context,
                'nodestroy': True,
                'res_id': mrp_id.id,
            }
        if self.fal_type == 'mrp.repair':
            repair_obj = self.env['mrp.repair']
            warehouse_id = self.env['stock.warehouse'].search([])[0]
            temp_val['location_dest_id'] = warehouse_id.in_type_id.default_location_dest_id.id
            temp_val['partner_id'] = self.fal_partner_id.id
            repair_id = repair_obj.create(temp_val)

            return {
                'type': 'ir.actions.act_window',
                'name': _('Repair Form'),
                'res_model': 'mrp.repair',
                'view_type': 'form',
                'view_mode': 'form,tree',
                'context': self.env.context,
                'nodestroy': True,
                'res_id': repair_id.id,
            }
        return {'type': 'ir.actions.act_window_close'}
        
#end of bom_create_record_wizard()