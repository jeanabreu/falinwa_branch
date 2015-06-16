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
        return {
            'type': 'ir.actions.act_window',
            'name': self.product_id.name,
            'res_model': 'mrp.bom.line',
            'view_mode': 'tree',
            'view_type': 'tree',
            'view_id': self.env['ir.model.data'].get_object_reference('mrp', 'mrp_bom_tree_view')[1],
            'domain' : '[("bom_id","=",'+str(self.fal_bom_id.id)+')]',
            'target': 'new',
             }
             
#end of bom_reader_wizard()

class bom_create_record_wizard(models.TransientModel):
    _name = "bom.create.record.wizard"
    _description = "BOM Create Record Wizard"
    
    fal_product_id = fields.Many2one('product.product', 'Finished Product', ondelete='restrict')
    fal_qty = fields.Float('Qty', digits_compute=dp.get_precision('Product Unit of Measure'), default=1)
    fal_uom_id = fields.Many2one('product.uom', 'Product Unit of Measure', required=True)
    fal_type = fields.Selection([('sale.order','Sale Order'),('mrp.production','Manufacture order'),('mrp.repair','Repair Order')], 'Type')
    fal_existed_quotation = fields.Many2one('sale.order', 'Existing Quotation', domain="[('state','=','draft')]") 

    @api.multi
    def make_record(self):
        return True
        
#end of bom_create_record_wizard()