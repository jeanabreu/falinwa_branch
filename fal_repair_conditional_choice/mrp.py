# -*- coding: utf-8 -*-
from openerp.osv import fields, orm
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP, float_compare
from openerp import SUPERUSER_ID

class mrp_repair(orm.Model):
    _name = 'mrp.repair'    
    _inherit = 'mrp.repair'      
        
    _columns = {
        'fal_serie_name_id' : fields.many2one('fal.serie.name','Serie Name'),
        'fal_serie_name_id_name' : fields.related('fal_serie_name_id', 'name', string="Serie Name", type='char', readonly=True),
        'fal_serie_name_id_type' : fields.related('fal_serie_name_id', 'type', string="Serie Name Type", type='char', readonly=True),
        'fal_ordering_code_id' : fields.many2one('fal.ordering.code','Ordering Code', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_bore_diameter_id' : fields.many2one('fal.bore.diameter','Bore Diameter (mm)', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_rod_diameter_id' : fields.many2one('fal.rod.diameter','Rod Diameter (mm)', domain="[('fal_bore_list_ids','=',fal_bore_diameter_id)]"),
        'fal_main_option_id' : fields.many2one('fal.main.option','Main Option', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_main_option_code' : fields.related('fal_main_option_id', 'code', string="Main Option Code", type='char', readonly=True),
        'fal_rod_end_id' : fields.many2one('fal.rod.end','Rod End', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_rod_end_option_id' : fields.many2one('fal.rod.end.option','Rod End Option'),
        'fal_seal_kit_id' : fields.many2one('fal.seal.kit','Seal Kit', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_mounting_id' : fields.many2one('fal.mounting','Mounting', domain="[('fal_serie_list_ids','=',fal_serie_name_id)]"),
        'fal_mounting_id_code' : fields.related('fal_mounting_id', 'code', string="Main Option Code", type='char', readonly=True),
        'fal_purge' : fields.boolean('Purge(PG)?'),
        'fal_brace_ring' : fields.boolean('Brace Ring?'),
        'fal_counter_bores' : fields.boolean('Counter Bores(LV)?'),
        'fal_for_handling' : fields.boolean('For Handling(TA)?'),
        'fal_microrupteur' : fields.boolean('Micro Rupteur?'),
        'fal_magnet_sensor' : fields.boolean('Magnet Sensor?'),
        'fal_xcma' : fields.boolean('XCMA 110?'),
        'fal_cote_x' : fields.integer('COTE X', required=True),
        'fal_magnet_sensor_position_id' : fields.many2one('fal.magnet.position', 'Magnet Sensor Position'),
        'fal_seal_location' : fields.char('Seal Location', size=128),
        'fal_full_reference' : fields.char('Full Reference',size=256),
        'fal_sale_reference' : fields.char('Sale Reference', size=256),
        'fal_ref_for_stroke_option' : fields.char('Ref For Stroke Option', size=128),
        'fal_by_stroke_option' : fields.char('By Stroke Option', size=128),
        'fal_bom_reference' : fields.char('BOM Reference',size=128),
        'fal_ref_priced_option' : fields.char('Ref Priced Option',size=128),
        'fal_ref_free_option' : fields.char('Ref Free Option',size=128),
        'fal_standard_stroke_id' : fields.many2one('fal.standard.stroke', string='Standard Stroke(MM)'),
        'fal_piston_seal': fields.selection([('D','D - Double acting seal'), ('P','P - Compound Seal')], string='Piston Seal'),
        'fal_rod_seal': fields.selection([('J','J - Single lip seal'), ('P','P - Compound Seal')], string='Rod Seal'),
        'fal_ports': fields.selection([('G','G - Internal Thread Gaz')], string='Ports'),
        'fal_position_ports_head': fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Head'),
        'fal_position_ports_bottom': fields.selection([('1','1'),('2','2'),('3','3'),('4','4'),], string='Position of Ports - Bottom'),
        'fal_value_xv' : fields.float('Value for XV (for MT4?DT4 only)'),
        'fal_single_or_double_rod' : fields.related('fal_mounting_id','sr_or_dr',type='char', string='Single or Double Rod', readonly=True),
        'fal_stroke' : fields.integer('Stroke (mm)'),
        'fal_special' : fields.boolean('Special'),
        'fal_y' : fields.float('Y'),
        'fal_w' : fields.float('W'),
        'fal_comment_for_vh' : fields.text('Comment'),
    }

    def get_by_stroke_option(self, cr, uid, ref, fal_stroke):                  

        return self.pool.get('sale.order.line').get_by_stroke_option(cr, uid, ref, fal_stroke)
        
    def onchange_conditional(self, cr, uid, ids, 
        fal_serie_name_id, fal_bore_diameter_id, fal_rod_diameter_id, fal_stroke, fal_main_option_id, fal_rod_end_id, fal_rod_end_option_id, fal_seal_kit_id, fal_mounting_id, 
        fal_purge, fal_counter_bores, fal_for_handling, fal_microrupteur, fal_magnet_sensor, fal_cote_x, fal_magnet_sensor_position_id, fal_seal_location, fal_ordering_code_id, 
        fal_standard_stroke_id, fal_piston_seal, fal_rod_seal, fal_ports, fal_brace_ring, fal_position_ports_head, fal_position_ports_bottom, fal_value_xv, flag=False):

        return self.pool.get('sale.order.line').onchange_conditional(cr, uid, ids, 
        fal_serie_name_id, fal_bore_diameter_id, fal_rod_diameter_id, fal_stroke, fal_main_option_id, fal_rod_end_id, fal_rod_end_option_id, fal_seal_kit_id, fal_mounting_id, 
        fal_purge, fal_counter_bores, fal_for_handling, fal_microrupteur, fal_magnet_sensor, fal_cote_x, fal_magnet_sensor_position_id, fal_seal_location, fal_ordering_code_id, 
        fal_standard_stroke_id, fal_piston_seal, fal_rod_seal, fal_ports, fal_brace_ring, fal_position_ports_head, fal_position_ports_bottom, fal_value_xv, flag)

    def onchange_bomref(self, cr, uid, ids, fal_bom_reference):

        return self.pool.get('sale.order.line').onchange_bomref(cr, uid, ids, fal_bom_reference)
        
#end of mrp_repair()